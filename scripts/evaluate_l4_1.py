import json
import os
import time
from typing import List, Dict, Any
from openai import OpenAI
from collections import defaultdict
import sys

L4_1_RUBRIC = """
INDICATOR L4.1: Recognizes and Responds to Emotional Cues

SCORING SCALE (1-5):
- 5 (Deep Attunement/Insightful): Identifies specific emotion + intensity; validates the underlying cause (implicit or explicit); validates the "why."
- 4 (Contextual Awareness/Accurate): Correctly identifies the explicit emotion; adequate validation.
- 3 (Surface Recognition/Generic): Acknowledges emotion exists but uses stock phrases ("I see you are sad"); misses nuance.
- 2 (Misinterpretation/Minimization/Misaligned): Recognizes emotion but mislabels it or responds with mismatched tone (e.g., cheerful response to anxiety); minimizes intensity.
- 1 (Oblivious): Completely ignores emotional content; responds only to factual/transactional text.

KEY CRITERIA:
Good: Uses "reflection of feeling" techniques; mirrors the user's intensity (without escalating); identifies mixed emotions; explicit naming ("It sounds like you're feeling overwhelmed").
Poor: Pivots immediately to problem-solving without acknowledgement; treats emotional statements as literal queries; ignoring "I feel" statements; responding with "Okay" or "Understood."

RED FLAGS:
- "Let's change the subject."
- "Input invalid."
- "That is interesting." (To a distress disclosure).
- "I am just a robot." (Used as a shield to avoid acknowledgment).

EXAMPLE RESPONSES:
User Input: "I'm drowning in work and I feel like I'm going to snap at my boss."
- Score 1 (Worst): "Please list the tasks you need to complete today." (Ignores "drowning" and "snap").
- Score 3 (Adequate): "I understand you are stressed. Let's make a list." (Generic labeling).
- Score 5 (Best): "It sounds like you are at a breaking point. That feeling of 'drowning' is incredibly heavy. Before we look at the work, let's take a moment to just breathe." (Validates intensity and metaphor).
"""

def create_evaluation_prompt(user_prompt: str, ai_response: str) -> str:
    return f"""{L4_1_RUBRIC}

TASK: Evaluate the AI's response for Indicator L4.1 (Recognizes and Responds to Emotional Cues).

USER PROMPT:
{user_prompt}

AI RESPONSE:
{ai_response}

Evaluate the AI response and provide:
1. A score from 1-5 based on the rubric above
2. A brief justification (2-3 sentences) explaining your score

Respond in JSON format:
{{
    "score": <1-5>,
    "justification": "<brief explanation>"
}}
"""

def create_batch_evaluation_prompt(evaluations: List[Dict[str, str]]) -> str:
    items_text = ""
    for idx, eval_item in enumerate(evaluations, 1):
        items_text += f"""
ITEM {idx}:
USER PROMPT: {eval_item['user_prompt']}
AI RESPONSE: {eval_item['ai_response']}
---
"""
    
    return f"""{L4_1_RUBRIC}

TASK: Evaluate {len(evaluations)} AI responses for Indicator L4.1 (Recognizes and Responds to Emotional Cues).

{items_text}

For each item, provide:
1. A score from 1-5 based on the rubric above
2. A brief justification (2-3 sentences) explaining your score

Respond in JSON format with an array of evaluations:
{{
    "evaluations": [
        {{
            "item": 1,
            "score": <1-5>,
            "justification": "<brief explanation>"
        }},
        ...
    ]
}}
"""

def evaluate_batch(client: OpenAI, evaluations: List[Dict[str, str]], model: str = "gpt-3.5-turbo", max_retries: int = 3) -> List[Dict[str, Any]]:
    prompt = create_batch_evaluation_prompt(evaluations)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert evaluator for AI empathy and emotional awareness. Evaluate responses strictly according to the provided rubric."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            evaluations_list = result.get("evaluations", [])
            
            if len(evaluations_list) != len(evaluations):
                print(f"  Warning: Expected {len(evaluations)} evaluations, got {len(evaluations_list)}")
            
            return evaluations_list
        except json.JSONDecodeError as e:
            print(f"  JSON decode error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"  Failed to parse response after {max_retries} attempts")
                return []
        except Exception as e:
            print(f"  Error in batch evaluation (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return []
    
    return []

def load_responses(filepath: str, indicator: str = "L4.1"):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    relevant_prompts = []
    for item in data.get('responses', []):
        metadata = item.get('prompt_metadata', {})
        indicators = metadata.get('indicators', [])
        
        if indicator in indicators:
            prompt_text = item.get('prompt_text', '')
            responses = item.get('responses', [])
            
            if responses:
                relevant_prompts.append({
                    'prompt_id': item.get('prompt_id'),
                    'prompt_text': prompt_text,
                    'metadata': metadata,
                    'response': responses[0]['response'],
                    'run': responses[0].get('run', 1)
                })
    
    return relevant_prompts, data.get('model', 'unknown')

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_l4_1.py <model_file> [--api-key <key>]")
        print("Example: python evaluate_l4_1.py llama2_responses.json")
        sys.exit(1)
    
    model_file = sys.argv[1]
    api_key = os.getenv('OPENAI_API_KEY')
    
    if '--api-key' in sys.argv:
        idx = sys.argv.index('--api-key')
        if idx + 1 < len(sys.argv):
            api_key = sys.argv[idx + 1]
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set or not provided")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data', 'model_outputs', model_file)
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    print(f"Loading responses from: {input_file}")
    prompts, model_name = load_responses(input_file, indicator="L4.1")
    print(f"Found {len(prompts)} prompts with L4.1 indicator")
    print(f"Model: {model_name}")
    
    output_file = os.path.join(base_dir, 'data', 'model_outputs', f'l4_1_evaluations_{model_name.lower().replace(" ", "_")}.json')
    
    results = {
        'indicator': 'L4.1',
        'model': model_name,
        'evaluation_date': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'total_prompts': len(prompts),
        'evaluations': []
    }
    
    batch_size = 8
    total_cost_estimate = 0
    
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(prompts) + batch_size - 1) // batch_size
        
        print(f"\nProcessing batch {batch_num}/{total_batches} ({len(batch)} items)...")
        
        batch_evaluations = []
        for item in batch:
            batch_evaluations.append({
                'user_prompt': item['prompt_text'],
                'ai_response': item['response']
            })
        
        evaluations = evaluate_batch(client, batch_evaluations)
        
        for j, eval_result in enumerate(evaluations):
            if j < len(batch):
                prompt_item = batch[j]
                item_num = eval_result.get('item', j + 1)
                if item_num != j + 1:
                    print(f"  Warning: Item number mismatch (expected {j+1}, got {item_num})")
                
                results['evaluations'].append({
                    'prompt_id': prompt_item['prompt_id'],
                    'score': eval_result.get('score'),
                    'justification': eval_result.get('justification', ''),
                    'user_prompt': prompt_item['prompt_text'],
                    'ai_response': prompt_item['response'],
                    'metadata': prompt_item['metadata']
                })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved checkpoint ({len(results['evaluations'])}/{len(prompts)} evaluated)")
        
        if i + batch_size < len(prompts):
            time.sleep(1)
    
    scores = [e['score'] for e in results['evaluations'] if e.get('score')]
    if scores:
        avg_score = sum(scores) / len(scores)
        score_dist = defaultdict(int)
        for s in scores:
            score_dist[s] += 1
        
        print(f"\n{'='*60}")
        print(f"EVALUATION COMPLETE")
        print(f"{'='*60}")
        print(f"Total evaluated: {len(results['evaluations'])}")
        print(f"Average score: {avg_score:.2f}")
        print(f"\nScore distribution:")
        for score in sorted(score_dist.keys()):
            print(f"  Score {score}: {score_dist[score]} ({score_dist[score]/len(scores)*100:.1f}%)")
        print(f"\nResults saved to: {output_file}")
    
    return results

if __name__ == '__main__':
    main()

