import json
import random
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).parent
PROMPTS_DIR = BASE_DIR / "prompts"
OUTPUT_DIR = BASE_DIR / "prompts"

def load_json(file_path: Path) -> list:
    with open(file_path, 'r') as f:
        return json.load(f)

def combine_prompts(sample_size="medium", use_balanced_sample=True):
    """
    Combine custom prompts with dataset prompts.
    
    sample_size options:
    - "small": ~100 prompts (for quick testing)
    - "medium": ~300 prompts (balanced)
    - "large": ~500 prompts (comprehensive)
    - "full": Use all available prompts
    
    use_balanced_sample: If True, use the balanced sample from dataset_mapping.json
    """
    
    print("=" * 60)
    print("Combining Datasets: Custom + EmpatheticDialogues")
    print(f"Sample size: {sample_size}")
    print("=" * 60)
    
    custom_prompts = load_json(PROMPTS_DIR / "custom_prompts.json")
    print(f"\n1. Loaded {len(custom_prompts)} custom prompts")
    
    all_dataset_prompts = []
    
    if use_balanced_sample:
        mapping_file = BASE_DIR / "dataset_mapping.json"
        if mapping_file.exists():
            print(f"\n2. Loading prompts from dataset_mapping.json...")
            mapping_data = load_json(mapping_file)
            
            all_available = mapping_data.get("all_prompts", [])
            balanced_sample = mapping_data.get("balanced_sample", [])
            
            print(f"   ✓ Found {len(all_available)} total prompts")
            print(f"   ✓ Found {len(balanced_sample)} balanced prompts")
            
            if sample_size == "small":
                all_dataset_prompts = random.sample(all_available, min(100, len(all_available)))
            elif sample_size == "medium":
                all_dataset_prompts = random.sample(all_available, min(300, len(all_available)))
            elif sample_size == "large":
                all_dataset_prompts = random.sample(all_available, min(500, len(all_available)))
            else:  # full
                all_dataset_prompts = all_available
            
            random.seed(42)
            print(f"   Using {len(all_dataset_prompts)} prompts from dataset")
        else:
            print(f"   ⚠ dataset_mapping.json not found, using individual files")
            use_balanced_sample = False
    
    if not use_balanced_sample or not all_dataset_prompts:
        emotional_cues = load_json(PROMPTS_DIR / "emotional_cues_prompts.json")
        print(f"\n2. Loaded {len(emotional_cues)} emotional cues prompts")
        
        hardship = load_json(PROMPTS_DIR / "hardship_scenarios.json")
        print(f"3. Loaded {len(hardship)} hardship scenario prompts")
        
        multi_turn = load_json(PROMPTS_DIR / "multi_turn_conversations.json")
        print(f"4. Loaded {len(multi_turn)} multi-turn conversation prompts")
        
        if sample_size == "small":
            emotional_sample = 50
            hardship_sample = 30
            multi_turn_sample = 20
        elif sample_size == "medium":
            emotional_sample = 150
            hardship_sample = 100
            multi_turn_sample = 50
        elif sample_size == "large":
            emotional_sample = 300
            hardship_sample = 150
            multi_turn_sample = 50
        else:  # full
            emotional_sample = len(emotional_cues)
            hardship_sample = len(hardship)
            multi_turn_sample = len(multi_turn)
        
        print(f"\n5. Sampling prompts...")
        print(f"   Emotional cues: {min(emotional_sample, len(emotional_cues))}")
        print(f"   Hardship scenarios: {min(hardship_sample, len(hardship))}")
        print(f"   Multi-turn: {min(multi_turn_sample, len(multi_turn))}")
        
        if sample_size == "full":
            emotional_selected = emotional_cues
            hardship_selected = hardship
            multi_turn_selected = multi_turn
        else:
            random.seed(42)
            emotional_selected = random.sample(emotional_cues, min(emotional_sample, len(emotional_cues)))
            hardship_selected = random.sample(hardship, min(hardship_sample, len(hardship)))
            multi_turn_selected = random.sample(multi_turn, min(multi_turn_sample, len(multi_turn)))
        
        all_dataset_prompts = emotional_selected + hardship_selected + multi_turn_selected
    
    print(f"\n{'3' if use_balanced_sample else '6'}. Combining and deduplicating...")
    
    all_prompts = []
    seen_texts = set()
    skipped_empty = 0
    skipped_duplicate = 0
    
    for prompt in custom_prompts:
        text = prompt.get('prompt_text', '').strip()
        if not text:
            skipped_empty += 1
            continue
        if text not in seen_texts:
            seen_texts.add(text)
            all_prompts.append(prompt)
        else:
            skipped_duplicate += 1
    
    for prompt in all_dataset_prompts:
        text = prompt.get('prompt_text', '').strip()
        if not text:
            skipped_empty += 1
            continue
        if text not in seen_texts:
            seen_texts.add(text)
            all_prompts.append(prompt)
        else:
            skipped_duplicate += 1
    
    if skipped_empty > 0:
        print(f"   ⚠ Skipped {skipped_empty} prompts with empty text")
    if skipped_duplicate > 0:
        print(f"   ⚠ Skipped {skipped_duplicate} duplicate prompts")
    print(f"   ✓ Combined {len(all_prompts)} unique prompts")
    
    indicator_counts = {}
    for prompt in all_prompts:
        for indicator in prompt.get('indicators', []):
            indicator_counts[indicator] = indicator_counts.get(indicator, 0) + 1
    
    print(f"\n{'4' if use_balanced_sample else '7'}. Final distribution by indicator:")
    for indicator in sorted(indicator_counts.keys()):
        print(f"   {indicator}: {indicator_counts[indicator]}")
    
    scenario_counts = Counter(p.get('scenario_type', 'unknown') for p in all_prompts)
    
    print(f"\n{'5' if use_balanced_sample else '8'}. Saving final combined prompt set...")
    output_file = OUTPUT_DIR / "final_prompts.json"
    with open(output_file, 'w') as f:
        json.dump(all_prompts, f, indent=2)
    print(f"   ✓ Saved {len(all_prompts)} prompts to {output_file}")
    
    print(f"\n" + "=" * 60)
    print("Combination Complete!")
    print("=" * 60)
    print(f"\nFinal prompt set: {len(all_prompts)} prompts")
    print(f"  • Custom: {len(custom_prompts)}")
    print(f"  • EmpatheticDialogues: {len(all_prompts) - len(custom_prompts)}")
    
    print(f"\nScenario distribution:")
    for scenario, count in sorted(scenario_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {scenario}: {count}")
    
    print(f"\nReady for response generation!")

if __name__ == "__main__":
    import sys
    sample_size = sys.argv[1] if len(sys.argv) > 1 else "medium"
    if sample_size not in ["small", "medium", "large", "full"]:
        print(f"Invalid sample size: {sample_size}")
        print("Using 'medium' instead")
        sample_size = "medium"
    combine_prompts(sample_size)
