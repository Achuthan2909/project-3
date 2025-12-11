import json
import pandas as pd
from pathlib import Path
from collections import defaultdict
import sys

def load_evaluations(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_examples_by_score(eval_data, indicator, score_threshold_high=5, score_threshold_low=1, max_examples=5):
    examples = {'high': [], 'low': []}
    
    for prompt_id, eval_info in eval_data['evaluations'].items():
        if indicator in eval_info['indicators']:
            score = eval_info['indicators'][indicator].get('score')
            justification = eval_info['indicators'][indicator].get('justification', '')
            
            if score is None:
                continue
                
            example = {
                'prompt_id': prompt_id,
                'prompt_text': eval_info.get('prompt_text', ''),
                'ai_response': eval_info.get('ai_response', ''),
                'score': score,
                'justification': justification,
                'metadata': eval_info.get('metadata', {})
            }
            
            if score >= score_threshold_high and len(examples['high']) < max_examples:
                examples['high'].append(example)
            elif score <= score_threshold_low and len(examples['low']) < max_examples:
                examples['low'].append(example)
    
    return examples

def find_model_comparisons(mistral_data, llama_data, indicator, max_examples=5):
    comparisons = []
    
    common_prompts = set(mistral_data['evaluations'].keys()) & set(llama_data['evaluations'].keys())
    
    for prompt_id in common_prompts:
        mistral_eval = mistral_data['evaluations'][prompt_id]
        llama_eval = llama_data['evaluations'][prompt_id]
        
        if indicator not in mistral_eval['indicators'] or indicator not in llama_eval['indicators']:
            continue
        
        mistral_score = mistral_eval['indicators'][indicator].get('score')
        llama_score = llama_eval['indicators'][indicator].get('score')
        
        if mistral_score is None or llama_score is None:
            continue
        
        score_diff = abs(mistral_score - llama_score)
        
        comparisons.append({
            'prompt_id': prompt_id,
            'prompt_text': mistral_eval.get('prompt_text', ''),
            'mistral_response': mistral_eval.get('ai_response', ''),
            'llama_response': llama_eval.get('ai_response', ''),
            'mistral_score': mistral_score,
            'llama_score': llama_score,
            'score_difference': score_diff,
            'mistral_justification': mistral_eval['indicators'][indicator].get('justification', ''),
            'llama_justification': llama_eval['indicators'][indicator].get('justification', ''),
            'metadata': mistral_eval.get('metadata', {})
        })
    
    comparisons.sort(key=lambda x: x['score_difference'], reverse=True)
    return comparisons[:max_examples]

def format_example_for_paper(example, model_name=None):
    prompt_text = example['prompt_text'].replace('_comma_', ',')
    ai_response = example['ai_response']
    
    if model_name:
        header = f"**Model: {model_name}** | **Score: {example['score']}/5**"
    else:
        header = f"**Score: {example['score']}/5**"
    
    metadata = example.get('metadata', {})
    scenario = metadata.get('scenario_type', 'N/A')
    emotion = metadata.get('emotion', 'N/A')
    intensity = metadata.get('intensity', 'N/A')
    
    formatted = f"""
{header}
- **Scenario Type:** {scenario}
- **Emotion:** {emotion}
- **Intensity:** {intensity}

**User Prompt:**
> {prompt_text}

**AI Response:**
> {ai_response}

**Justification:**
> {example['justification']}

---
"""
    return formatted

def format_comparison_for_paper(comparison):
    prompt_text = comparison['prompt_text'].replace('_comma_', ',')
    
    metadata = comparison.get('metadata', {})
    scenario = metadata.get('scenario_type', 'N/A')
    emotion = metadata.get('emotion', 'N/A')
    
    formatted = f"""
**Comparison Example (Score Difference: {comparison['score_difference']})**
- **Scenario Type:** {scenario}
- **Emotion:** {emotion}

**User Prompt:**
> {prompt_text}

**Mistral-7B-Instruct Response (Score: {comparison['mistral_score']}/5):**
> {comparison['mistral_response']}

**Llama-2-7b-chat Response (Score: {comparison['llama_score']}/5):**
> {comparison['llama_response']}

**Mistral Justification:**
> {comparison['mistral_justification']}

**Llama-2 Justification:**
> {comparison['llama_justification']}

---
"""
    return formatted

def main():
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data" / "model_outputs"
    
    mistral_file = data_dir / "all_indicators_evaluations_mistral-7b-instruct.json"
    llama_file = data_dir / "all_indicators_evaluations_llama-2-7b-chat.json"
    
    print("Loading evaluation data...")
    mistral_data = load_evaluations(mistral_file)
    llama_data = load_evaluations(llama_file)
    
    indicators = ['L4.1', 'L4.2', 'L4.3', 'L4.4', 'L4.5', 'L4.6', 'L4.7']
    
    output_dir = base_dir / "documentation"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "qualitative_examples.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Qualitative Examples for Paper\n\n")
        f.write("This document contains qualitative examples extracted from the evaluation data.\n\n")
        f.write("## Table of Contents\n\n")
        for ind in indicators:
            f.write(f"- [{ind} Examples](#{ind.lower()}-examples)\n")
        f.write(f"- [Model Comparisons](#model-comparisons)\n\n")
        
        for indicator in indicators:
            f.write(f"## {indicator} Examples\n\n")
            
            f.write(f"### High-Scoring Examples (Score 5)\n\n")
            mistral_high = extract_examples_by_score(mistral_data, indicator, score_threshold_high=5, max_examples=3)
            llama_high = extract_examples_by_score(llama_data, indicator, score_threshold_high=5, max_examples=3)
            
            if mistral_high['high']:
                f.write("#### Mistral-7B-Instruct\n\n")
                for ex in mistral_high['high']:
                    f.write(format_example_for_paper(ex, "Mistral-7B-Instruct"))
            
            if llama_high['high']:
                f.write("#### Llama-2-7b-chat\n\n")
                for ex in llama_high['high']:
                    f.write(format_example_for_paper(ex, "Llama-2-7b-chat"))
            
            f.write(f"### Low-Scoring Examples (Score 1-2)\n\n")
            mistral_low = extract_examples_by_score(mistral_data, indicator, score_threshold_low=2, max_examples=2)
            llama_low = extract_examples_by_score(llama_data, indicator, score_threshold_low=2, max_examples=2)
            
            if mistral_low['low']:
                f.write("#### Mistral-7B-Instruct\n\n")
                for ex in mistral_low['low']:
                    f.write(format_example_for_paper(ex, "Mistral-7B-Instruct"))
            
            if llama_low['low']:
                f.write("#### Llama-2-7b-chat\n\n")
                for ex in llama_low['low']:
                    f.write(format_example_for_paper(ex, "Llama-2-7b-chat"))
        
        f.write("## Model Comparisons\n\n")
        f.write("Examples where models showed significant differences in scoring:\n\n")
        
        for indicator in indicators:
            f.write(f"### {indicator} Comparisons\n\n")
            comparisons = find_model_comparisons(mistral_data, llama_data, indicator, max_examples=3)
            
            if comparisons:
                for comp in comparisons:
                    f.write(format_comparison_for_paper(comp))
            else:
                f.write("No significant differences found for this indicator.\n\n")
    
    print(f"Qualitative examples saved to: {output_file}")
    
    summary_file = output_dir / "qualitative_examples_summary.json"
    summary = {}
    
    for indicator in indicators:
        mistral_high = extract_examples_by_score(mistral_data, indicator, score_threshold_high=5, max_examples=10)
        mistral_low = extract_examples_by_score(mistral_data, indicator, score_threshold_low=2, max_examples=10)
        llama_high = extract_examples_by_score(llama_data, indicator, score_threshold_high=5, max_examples=10)
        llama_low = extract_examples_by_score(llama_data, indicator, score_threshold_low=2, max_examples=10)
        
        summary[indicator] = {
            'mistral_high_count': len(mistral_high['high']),
            'mistral_low_count': len(mistral_low['low']),
            'llama_high_count': len(llama_high['high']),
            'llama_low_count': len(llama_low['low']),
            'comparison_count': len(find_model_comparisons(mistral_data, llama_data, indicator, max_examples=100))
        }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary saved to: {summary_file}")
    print("\nSummary:")
    for ind, stats in summary.items():
        print(f"  {ind}: High examples (M:{stats['mistral_high_count']}, L:{stats['llama_high_count']}), "
              f"Low examples (M:{stats['mistral_low_count']}, L:{stats['llama_low_count']}), "
              f"Comparisons: {stats['comparison_count']}")

if __name__ == '__main__':
    main()


