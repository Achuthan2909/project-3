import json
import os
import time
import random
import re
from typing import List, Dict, Any, Set
from openai import OpenAI
from collections import defaultdict, Counter
import sys

def parse_rubrics_from_markdown(md_file: str) -> Dict[str, str]:
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rubrics = {}
    indicator_pattern = r'### Indicator (\d+): (.+?)(?=### Indicator|\Z)'
    
    matches = re.finditer(indicator_pattern, content, re.DOTALL)
    
    for match in matches:
        indicator_num = match.group(1)
        indicator_name = match.group(2).split('\n')[0].strip()
        rubric_text = match.group(2).strip()
        
        indicator_key = f"L4.{indicator_num}"
        rubrics[indicator_key] = {
            'name': indicator_name,
            'full_text': rubric_text
        }
    
    return rubrics

def format_rubric_for_prompt(indicator_key: str, rubric_data: Dict) -> str:
    return f"""
INDICATOR {indicator_key}: {rubric_data['name']}

{rubric_data['full_text']}
"""

def load_responses(filepath: str, random_seed: int = 42):
    random.seed(random_seed)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    prompts = []
    for item in data.get('responses', []):
        metadata = item.get('prompt_metadata', {})
        indicators = metadata.get('indicators', [])
        prompt_text = item.get('prompt_text', '')
        responses = item.get('responses', [])
        
        if responses and indicators:
            selected_run = random.choice(responses)
            prompts.append({
                'prompt_id': item.get('prompt_id'),
                'prompt_text': prompt_text,
                'ai_response': selected_run['response'],
                'run_number': selected_run.get('run', 1),
                'indicators': sorted(indicators),
                'metadata': metadata
            })
    
    return prompts, data.get('model', 'unknown')

def create_single_prompt_evaluation_prompt(item: Dict, rubrics: Dict[str, Dict], item_rubrics: Set[str]) -> str:
    rubric_texts = []
    for ind in sorted(item_rubrics):
        if ind in rubrics:
            rubric_texts.append(format_rubric_for_prompt(ind, rubrics[ind]))
    
    rubrics_section = "\n".join(rubric_texts)
    indicators_str = ", ".join(item['indicators'])
    
    return f"""You are an expert evaluator for AI empathy and emotional awareness. Evaluate the AI response strictly according to the provided rubrics.

RUBRICS:
{rubrics_section}

PROMPT TO EVALUATE (Indicators: {indicators_str}):
USER PROMPT: {item['prompt_text']}
AI RESPONSE: {item['ai_response']}

TASK: Evaluate the AI response against ALL of the specified indicators ({indicators_str}). For each indicator, provide:
1. A score from 1-5 based on the rubric
2. A brief justification (2-3 sentences) explaining your score

Respond in JSON format with EXACTLY this structure:
{{
    "evaluations": {{
        "L4.1": {{"score": 4, "justification": "The response correctly identifies..."}},
        "L4.2": {{"score": 5, "justification": "The response shows deep empathy..."}}
    }}
}}

CRITICAL: 
- Include ALL specified indicators: {indicators_str}
- All scores must be integers between 1 and 5
- Use the exact indicator keys: {', '.join(item['indicators'])}"""

def evaluate_single_prompt(client: OpenAI, item: Dict, rubrics: Dict[str, Dict], model: str = "gpt-3.5-turbo", max_retries: int = 3) -> Dict[str, Any]:
    item_rubrics = set(item['indicators'])
    prompt = create_single_prompt_evaluation_prompt(item, rubrics, item_rubrics)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert evaluator for AI empathy and emotional awareness. Evaluate responses strictly according to the provided rubrics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            evaluations = result.get("evaluations", {})
            
            if not evaluations:
                print(f"    Warning: Empty evaluations in response. Full response keys: {list(result.keys())}")
            
            return evaluations
        except json.JSONDecodeError as e:
            print(f"  JSON decode error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"  Failed to parse response after {max_retries} attempts")
                return {}
        except Exception as e:
            print(f"  Error in evaluation (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return {}
    
    return {}

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_all_indicators.py <model_file> [--api-key <key>]")
        print("Example: python evaluate_all_indicators.py llama2_responses.json")
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
    
    rubric_file = os.path.join(base_dir, 'documentation', 'phase1.md')
    input_file = os.path.join(base_dir, 'data', 'model_outputs', model_file)
    
    if not os.path.exists(rubric_file):
        print(f"Error: Rubric file not found: {rubric_file}")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    print("Loading rubrics...")
    rubrics = parse_rubrics_from_markdown(rubric_file)
    print(f"Loaded {len(rubrics)} rubrics: {', '.join(sorted(rubrics.keys()))}")
    
    print(f"\nLoading responses from: {input_file}")
    prompts, model_name = load_responses(input_file, random_seed=42)
    print(f"Loaded {len(prompts)} prompts")
    print(f"Model: {model_name}")
    
    output_file = os.path.join(base_dir, 'data', 'model_outputs', f'all_indicators_evaluations_{model_name.lower().replace(" ", "_")}.json')
    
    results = {
        'model': model_name,
        'evaluation_date': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'evaluation_mode': 'single_prompt',
        'total_prompts': len(prompts),
        'evaluations': {}
    }
    
    for i, item in enumerate(prompts, 1):
        prompt_id = item['prompt_id']
        indicators_str = ', '.join(item['indicators'])
        
        print(f"\nProcessing prompt {i}/{len(prompts)}: {prompt_id} (indicators: {indicators_str})...")
        
        evaluations = evaluate_single_prompt(client, item, rubrics)
        
        if not evaluations:
            print(f"  Error: No evaluations returned for prompt {prompt_id}. Skipping...")
            continue
        
        results['evaluations'][prompt_id] = {
            'indicators': {},
            'prompt_text': item['prompt_text'],
            'ai_response': item['ai_response'],
            'run_number': item['run_number'],
            'metadata': item['metadata']
        }
        
        missing_indicators = []
        for ind in item['indicators']:
            if ind in evaluations:
                results['evaluations'][prompt_id]['indicators'][ind] = evaluations[ind]
            else:
                missing_indicators.append(ind)
        
        if missing_indicators:
            print(f"  Warning: Missing evaluations for {missing_indicators}")
            print(f"    Available in response: {list(evaluations.keys())}")
        else:
            print(f"  ✓ All {len(item['indicators'])} indicators evaluated")
        
        if i % 10 == 0 or i == len(prompts):
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"  Saved checkpoint ({i}/{len(prompts)} evaluated)")
        
        if i < len(prompts):
            time.sleep(0.5)
    
    summary = {}
    for prompt_id, eval_data in results['evaluations'].items():
        for ind, eval_result in eval_data['indicators'].items():
            if ind not in summary:
                summary[ind] = {'scores': [], 'count': 0}
            score = eval_result.get('score')
            if score:
                summary[ind]['scores'].append(score)
                summary[ind]['count'] += 1
    
    results['summary'] = {}
    for ind in sorted(summary.keys()):
        scores = summary[ind]['scores']
        if scores:
            results['summary'][ind] = {
                'count': len(scores),
                'average_score': sum(scores) / len(scores),
                'score_distribution': dict(Counter(scores))
            }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print("EVALUATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total evaluated: {len(results['evaluations'])}")
    print(f"\nSummary by indicator:")
    for ind in sorted(results['summary'].keys()):
        s = results['summary'][ind]
        print(f"  {ind}: avg={s['average_score']:.2f}, count={s['count']}, dist={s['score_distribution']}")
    print(f"\nResults saved to: {output_file}")

if __name__ == '__main__':
    main()

