# analyze_prompts.py - Run this to get unique prompt statistics

import json
from collections import defaultdict, Counter

def analyze_prompts():
    base_dir = 'data/model_outputs'
    
    with open(f'{base_dir}/llama2_responses.json', 'r') as f:
        llama2_data = json.load(f)
    
    with open(f'{base_dir}/mistral_responses.json', 'r') as f:
        mistral_data = json.load(f)
    
    llama2_prompts = {}
    for item in llama2_data['responses']:
        pid = item['prompt_id']
        indicators = tuple(sorted(item.get('prompt_metadata', {}).get('indicators', [])))
        if pid not in llama2_prompts:
            llama2_prompts[pid] = {
                'indicators': set(indicators),
                'prompt_text': item.get('prompt_text', ''),
                'metadata': item.get('prompt_metadata', {})
            }
        else:
            llama2_prompts[pid]['indicators'].update(indicators)
    
    mistral_prompts = {}
    for item in mistral_data['responses']:
        pid = item['prompt_id']
        indicators = tuple(sorted(item.get('prompt_metadata', {}).get('indicators', [])))
        if pid not in mistral_prompts:
            mistral_prompts[pid] = {
                'indicators': set(indicators),
                'prompt_text': item.get('prompt_text', ''),
                'metadata': item.get('prompt_metadata', {})
            }
        else:
            mistral_prompts[pid]['indicators'].update(indicators)
    
    all_prompt_ids = set(llama2_prompts.keys()) | set(mistral_prompts.keys())
    common_prompts = set(llama2_prompts.keys()) & set(mistral_prompts.keys())
    
    print("="*80)
    print("UNIQUE PROMPT ANALYSIS")
    print("="*80)
    print(f"\nTotal unique prompts: {len(all_prompt_ids)}")
    print(f"Llama2 unique prompts: {len(llama2_prompts)}")
    print(f"Mistral unique prompts: {len(mistral_prompts)}")
    print(f"Prompts in both models: {len(common_prompts)}")
    
    indicator_prompt_map = defaultdict(set)
    indicator_counts = Counter()
    prompt_indicator_count = Counter()
    
    for pid, data in llama2_prompts.items():
        indicators = data['indicators']
        prompt_indicator_count[len(indicators)] += 1
        for ind in indicators:
            indicator_prompt_map[ind].add(pid)
            indicator_counts[ind] += 1
    
    print(f"\n{'='*80}")
    print("INDICATOR DISTRIBUTION (Unique Prompts)")
    print("="*80)
    for ind in sorted(indicator_prompt_map.keys()):
        count = len(indicator_prompt_map[ind])
        print(f"  {ind}: {count} unique prompts")
    
    print(f"\n{'='*80}")
    print("PROMPTS BY NUMBER OF INDICATORS")
    print("="*80)
    for count in sorted(prompt_indicator_count.keys()):
        print(f"  {count} indicator(s): {prompt_indicator_count[count]} prompts")
    
    indicator_combinations = Counter()
    for pid, data in llama2_prompts.items():
        combo = tuple(sorted(data['indicators']))
        indicator_combinations[combo] += 1
    
    print(f"\n{'='*80}")
    print("TOP 10 INDICATOR COMBINATIONS")
    print("="*80)
    for combo, count in indicator_combinations.most_common(10):
        print(f"  {', '.join(combo)}: {count} prompts")
    
    total_evaluations_needed = sum(len(data['indicators']) for data in llama2_prompts.values())
    print(f"\n{'='*80}")
    print("EVALUATION ESTIMATE")
    print("="*80)
    print(f"Total prompt-indicator pairs to evaluate (Llama2): {total_evaluations_needed}")
    print(f"Total prompt-indicator pairs to evaluate (Mistral): {total_evaluations_needed}")
    print(f"Total for both models: {total_evaluations_needed * 2}")
    print(f"\nEstimated API calls (batch size 8): ~{total_evaluations_needed * 2 // 8}")
    print(f"Estimated cost (GPT-3.5-turbo): ~${total_evaluations_needed * 2 * 0.002:.2f}")

if __name__ == '__main__':
    analyze_prompts()