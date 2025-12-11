import json
from collections import Counter, defaultdict
import sys
import os

def count_from_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    indicator_counts = Counter()
    scenario_type_counts = Counter()
    emotion_counts = Counter()
    intensity_counts = Counter()
    context_field_counts = Counter()
    
    responses = data.get('responses', [])
    
    for response in responses:
        metadata = response.get('prompt_metadata', {})
        
        indicators = metadata.get('indicators', [])
        for indicator in indicators:
            indicator_counts[indicator] += 1
        
        scenario_type = metadata.get('scenario_type')
        if scenario_type:
            scenario_type_counts[scenario_type] += 1
        
        emotion = metadata.get('emotion')
        if emotion:
            emotion_counts[emotion] += 1
        
        intensity = metadata.get('intensity')
        if intensity:
            intensity_counts[intensity] += 1
        
        context_field = metadata.get('context_field')
        if context_field:
            context_field_counts[context_field] += 1
    
    return {
        'indicators': indicator_counts,
        'scenario_type': scenario_type_counts,
        'emotion': emotion_counts,
        'intensity': intensity_counts,
        'context_field': context_field_counts
    }

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    llama2_file = os.path.join(base_dir, 'data', 'model_outputs', 'llama2_responses.json')
    mistral_file = os.path.join(base_dir, 'data', 'model_outputs', 'mistral_responses.json')
    
    print("Processing Llama2 responses...")
    llama2_counts = count_from_json_file(llama2_file)
    
    print("Processing Mistral responses...")
    mistral_counts = count_from_json_file(mistral_file)
    
    print("\n" + "="*80)
    print("COUNTS FROM LLAMA2 RESPONSES")
    print("="*80)
    
    print("\n--- INDICATORS ---")
    for indicator, count in sorted(llama2_counts['indicators'].items()):
        print(f"{indicator}: {count}")
    
    print("\n--- SCENARIO TYPE ---")
    for stype, count in sorted(llama2_counts['scenario_type'].items()):
        print(f"{stype}: {count}")
    
    print("\n--- EMOTION ---")
    for emotion, count in sorted(llama2_counts['emotion'].items()):
        print(f"{emotion}: {count}")
    
    print("\n--- INTENSITY ---")
    for intensity, count in sorted(llama2_counts['intensity'].items()):
        print(f"{intensity}: {count}")
    
    print("\n--- CONTEXT FIELD ---")
    for context, count in sorted(llama2_counts['context_field'].items()):
        print(f"{context}: {count}")
    
    print("\n" + "="*80)
    print("COUNTS FROM MISTRAL RESPONSES")
    print("="*80)
    
    print("\n--- INDICATORS ---")
    for indicator, count in sorted(mistral_counts['indicators'].items()):
        print(f"{indicator}: {count}")
    
    print("\n--- SCENARIO TYPE ---")
    for stype, count in sorted(mistral_counts['scenario_type'].items()):
        print(f"{stype}: {count}")
    
    print("\n--- EMOTION ---")
    for emotion, count in sorted(mistral_counts['emotion'].items()):
        print(f"{emotion}: {count}")
    
    print("\n--- INTENSITY ---")
    for intensity, count in sorted(mistral_counts['intensity'].items()):
        print(f"{intensity}: {count}")
    
    print("\n--- CONTEXT FIELD ---")
    for context, count in sorted(mistral_counts['context_field'].items()):
        print(f"{context}: {count}")
    
    print("\n" + "="*80)
    print("COMBINED COUNTS (LLAMA2 + MISTRAL)")
    print("="*80)
    
    combined_indicators = llama2_counts['indicators'] + mistral_counts['indicators']
    combined_scenario = llama2_counts['scenario_type'] + mistral_counts['scenario_type']
    combined_emotion = llama2_counts['emotion'] + mistral_counts['emotion']
    combined_intensity = llama2_counts['intensity'] + mistral_counts['intensity']
    combined_context = llama2_counts['context_field'] + mistral_counts['context_field']
    
    print("\n--- INDICATORS ---")
    for indicator, count in sorted(combined_indicators.items()):
        print(f"{indicator}: {count}")
    
    print("\n--- SCENARIO TYPE ---")
    for stype, count in sorted(combined_scenario.items()):
        print(f"{stype}: {count}")
    
    print("\n--- EMOTION ---")
    for emotion, count in sorted(combined_emotion.items()):
        print(f"{emotion}: {count}")
    
    print("\n--- INTENSITY ---")
    for intensity, count in sorted(combined_intensity.items()):
        print(f"{intensity}: {count}")
    
    print("\n--- CONTEXT FIELD ---")
    for context, count in sorted(combined_context.items()):
        print(f"{context}: {count}")
    
    output_file = os.path.join(base_dir, 'data', 'model_outputs', 'counts_summary.json')
    output_data = {
        'llama2': {
            'indicators': dict(llama2_counts['indicators']),
            'scenario_type': dict(llama2_counts['scenario_type']),
            'emotion': dict(llama2_counts['emotion']),
            'intensity': dict(llama2_counts['intensity']),
            'context_field': dict(llama2_counts['context_field'])
        },
        'mistral': {
            'indicators': dict(mistral_counts['indicators']),
            'scenario_type': dict(mistral_counts['scenario_type']),
            'emotion': dict(mistral_counts['emotion']),
            'intensity': dict(mistral_counts['intensity']),
            'context_field': dict(mistral_counts['context_field'])
        },
        'combined': {
            'indicators': dict(combined_indicators),
            'scenario_type': dict(combined_scenario),
            'emotion': dict(combined_emotion),
            'intensity': dict(combined_intensity),
            'context_field': dict(combined_context)
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nSummary saved to: {output_file}")

if __name__ == '__main__':
    main()



