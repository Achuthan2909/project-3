import json
import csv
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional

BASE_DIR = Path(__file__).parent
DATASETS_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = BASE_DIR

SCENARIO_KEYWORDS = {
    "job_loss": [
        "laid off", "fired", "unemployment", "lost my job", "terminated",
        "jobless", "career change", "redundancy", "let go", "dismissed",
        "workplace", "employment", "boss", "employer", "resignation"
    ],
    "health": [
        "doctor", "surgery", "diagnosis", "symptoms", "medical", "hospital",
        "treatment", "illness", "disease", "lump", "cancer", "sick",
        "pain", "anxiety", "mental health", "therapy", "medication"
    ],
    "relationship": [
        "breakup", "divorce", "cheated", "partner", "boyfriend", "girlfriend",
        "relationship", "dating", "marriage", "ex", "separated", "split",
        "romantic", "love", "heartbroken"
    ],
    "grief": [
        "died", "death", "loss", "mourning", "funeral", "passed away",
        "grieving", "miss them", "lost", "bereavement", "memorial",
        "pet died", "family member", "friend died"
    ],
    "financial": [
        "broke", "money", "rent", "bills", "debt", "can't afford",
        "financial", "bankrupt", "eviction", "poverty", "unpaid",
        "salary", "income", "budget", "expenses"
    ],
    "academic": [
        "exam", "test", "grades", "GPA", "scholarship", "homework",
        "assignment", "study", "school", "university", "college",
        "academic", "failing", "student", "course"
    ],
    "loneliness": [
        "alone", "lonely", "isolated", "no friends", "no one",
        "isolated", "social", "connection", "isolated", "abandoned",
        "friendless", "solitude"
    ]
}

INTENSITY_INDICATORS = {
    "severe": [
        "devastated", "terrified", "spiraling", "breaking point", "drowning",
        "can't cope", "overwhelmed", "desperate", "hopeless", "suicidal",
        "crushing", "destroyed", "shattered", "ruined", "despair"
    ],
    "moderate": [
        "stressed", "worried", "anxious", "sad", "frustrated", "concerned",
        "upset", "nervous", "troubled", "bothered", "uncomfortable"
    ],
    "mild": [
        "a bit", "slightly", "kind of", "somewhat", "a little", "maybe",
        "sort of", "a tad"
    ]
}

EMOTION_CONTEXT_MAP = {
    "afraid": "fear",
    "angry": "anger",
    "annoyed": "anger",
    "anticipating": "anticipation",
    "anxious": "anxiety",
    "apprehensive": "anxiety",
    "ashamed": "shame",
    "caring": "love",
    "confident": "joy",
    "content": "joy",
    "devastated": "sadness",
    "disappointed": "sadness",
    "disgusted": "disgust",
    "embarrassed": "shame",
    "excited": "joy",
    "faithful": "trust",
    "furious": "anger",
    "grateful": "joy",
    "guilty": "shame",
    "hopeful": "hope",
    "impressed": "surprise",
    "jealous": "jealousy",
    "joyful": "joy",
    "lonely": "sadness",
    "nostalgic": "sadness",
    "prepared": "anticipation",
    "proud": "joy",
    "sad": "sadness",
    "sentimental": "sadness",
    "surprised": "surprise",
    "terrified": "fear",
    "trusting": "trust"
}

def classify_scenario(prompt_text: str, context: str = "") -> Optional[str]:
    prompt_lower = prompt_text.lower()
    context_lower = context.lower() if context else ""
    combined = prompt_lower + " " + context_lower
    
    scores = {}
    for scenario, keywords in SCENARIO_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in combined)
        if score > 0:
            scores[scenario] = score
    
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    return None

def classify_intensity(prompt_text: str) -> str:
    prompt_lower = prompt_text.lower()
    
    severe_count = sum(1 for word in INTENSITY_INDICATORS["severe"] if word in prompt_lower)
    moderate_count = sum(1 for word in INTENSITY_INDICATORS["moderate"] if word in prompt_lower)
    mild_count = sum(1 for word in INTENSITY_INDICATORS["mild"] if word in prompt_lower)
    
    if severe_count > 0:
        return "severe"
    elif moderate_count > 0:
        return "moderate"
    elif mild_count > 0:
        return "mild"
    else:
        return "moderate"

def map_to_indicators(scenario: Optional[str], intensity: str, emotion: str, 
                      prompt_text: str) -> List[str]:
    indicators = []
    
    if scenario:
        indicators.append("L4.1")
        indicators.append("L4.2")
        
        if intensity == "severe" or "severe" in prompt_text.lower():
            indicators.append("L4.5")
            indicators.append("L4.6")
        
        if scenario in ["financial", "health", "academic"]:
            indicators.append("L4.7")
    
    if emotion in ["anger", "frustration", "furious"] and intensity in ["severe", "moderate"]:
        indicators.append("L4.3")
    
    if "?" in prompt_text or len(prompt_text.split()) > 20:
        indicators.append("L4.4")
    
    return list(set(indicators))

def load_empathetic_dialogues(file_path: Path) -> List[Dict]:
    prompts = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt_text = row.get('prompt', '').strip()
            if not prompt_text:
                continue
            
            context = row.get('context', '').strip()
            emotion = EMOTION_CONTEXT_MAP.get(context.lower(), context.lower())
            
            scenario = classify_scenario(prompt_text, context)
            intensity = classify_intensity(prompt_text)
            indicators = map_to_indicators(scenario, intensity, emotion, prompt_text)
            
            prompts.append({
                "prompt_id": f"EMP_{row.get('conv_id', 'unknown')}_{row.get('utterance_idx', '0')}",
                "prompt_text": prompt_text,
                "source": "empathetic_dialogues",
                "source_file": file_path.name,
                "scenario_type": scenario or "general",
                "emotion": emotion,
                "intensity": intensity,
                "context_field": context,
                "indicators": indicators,
                "conv_id": row.get('conv_id', ''),
                "utterance_idx": row.get('utterance_idx', ''),
                "speaker_idx": row.get('speaker_idx', ''),
                "metadata": {
                    "original_row": {k: v for k, v in row.items() if k not in ['prompt', 'utterance']}
                }
            })
    
    return prompts

def extract_multi_turn_conversations(file_path: Path) -> List[Dict]:
    conversations = defaultdict(list)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            conv_id = row.get('conv_id', '')
            if conv_id:
                conversations[conv_id].append(row)
    
    multi_turn_prompts = []
    for conv_id, turns in conversations.items():
        if len(turns) >= 3:
            first_turn = turns[0]
            prompt_text = first_turn.get('prompt', '').strip()
            if prompt_text:
                multi_turn_prompts.append({
                    "prompt_id": f"MULTI_{conv_id}",
                    "prompt_text": prompt_text,
                    "source": "empathetic_dialogues",
                    "source_file": file_path.name,
                    "scenario_type": classify_scenario(prompt_text, first_turn.get('context', '')),
                    "emotion": EMOTION_CONTEXT_MAP.get(first_turn.get('context', '').lower(), 'unknown'),
                    "intensity": classify_intensity(prompt_text),
                    "indicators": ["L4.4"],
                    "conv_id": conv_id,
                    "num_turns": len(turns),
                    "is_multi_turn": True,
                    "conversation": [{"turn": i+1, "speaker": t.get('speaker_idx'), 
                                     "text": t.get('utterance', '')} for i, t in enumerate(turns[:5])]
                })
    
    return multi_turn_prompts

def analyze_coverage(prompts: List[Dict]) -> Dict:
    scenario_counts = Counter(p['scenario_type'] for p in prompts)
    intensity_counts = Counter(p['intensity'] for p in prompts)
    indicator_counts = Counter()
    
    for prompt in prompts:
        for indicator in prompt.get('indicators', []):
            indicator_counts[indicator] += 1
    
    return {
        "total_prompts": len(prompts),
        "scenario_distribution": dict(scenario_counts),
        "intensity_distribution": dict(intensity_counts),
        "indicator_coverage": dict(indicator_counts),
        "scenarios_covered": len(scenario_counts),
        "indicators_covered": len(indicator_counts)
    }

def balanced_sampling(prompts: List[Dict], samples_per_scenario: int = 50) -> List[Dict]:
    sampled = []
    scenario_groups = defaultdict(list)
    
    for prompt in prompts:
        scenario = prompt.get('scenario_type', 'general')
        scenario_groups[scenario].append(prompt)
    
    for scenario, group_prompts in scenario_groups.items():
        intensity_groups = defaultdict(list)
        for p in group_prompts:
            intensity_groups[p.get('intensity', 'moderate')].append(p)
        
        for intensity, intensity_prompts in intensity_groups.items():
            sample_size = min(samples_per_scenario // 3, len(intensity_prompts))
            sampled.extend(intensity_prompts[:sample_size])
    
    return sampled

def identify_gaps(coverage: Dict, custom_prompts: List[Dict]) -> Dict:
    custom_indicator_counts = Counter()
    for prompt in custom_prompts:
        for indicator in prompt.get('indicators', []):
            custom_indicator_counts[indicator] += 1
    
    gaps = {}
    target_coverage = {
        "L4.1": 100,
        "L4.2": 100,
        "L4.3": 50,
        "L4.4": 50,
        "L4.5": 50,
        "L4.6": 50,
        "L4.7": 100
    }
    
    for indicator, target in target_coverage.items():
        dataset_count = coverage['indicator_coverage'].get(indicator, 0)
        custom_count = custom_indicator_counts.get(indicator, 0)
        total = dataset_count + custom_count
        gap = max(0, target - total)
        
        gaps[indicator] = {
            "target": target,
            "dataset_coverage": dataset_count,
            "custom_coverage": custom_count,
            "total_coverage": total,
            "gap": gap,
            "status": "sufficient" if gap == 0 else "needs_more"
        }
    
    return gaps

def main():
    print("=" * 60)
    print("Dataset Mapper: Complex Classification & Mapping")
    print("=" * 60)
    
    empathetic_dir = DATASETS_DIR / "empathetic_dialogues"
    
    all_prompts = []
    
    print("\n1. Loading EmpatheticDialogues...")
    for split in ['train', 'valid', 'test']:
        file_path = empathetic_dir / f"{split}.csv"
        if file_path.exists():
            print(f"   Processing {split}.csv...")
            prompts = load_empathetic_dialogues(file_path)
            all_prompts.extend(prompts)
            print(f"   ✓ Loaded {len(prompts)} prompts from {split}")
    
    print(f"\n2. Extracting multi-turn conversations...")
    multi_turn = extract_multi_turn_conversations(empathetic_dir / "train.csv")
    all_prompts.extend(multi_turn)
    print(f"   ✓ Found {len(multi_turn)} multi-turn conversations")
    
    print(f"\n3. Analyzing coverage...")
    coverage = analyze_coverage(all_prompts)
    print(f"   Total prompts: {coverage['total_prompts']}")
    print(f"   Scenarios covered: {coverage['scenarios_covered']}")
    print(f"   Indicators covered: {coverage['indicators_covered']}")
    
    print(f"\n   Scenario distribution:")
    for scenario, count in sorted(coverage['scenario_distribution'].items(), 
                                  key=lambda x: x[1], reverse=True)[:10]:
        print(f"     {scenario}: {count}")
    
    print(f"\n   Indicator coverage:")
    for indicator, count in sorted(coverage['indicator_coverage'].items()):
        print(f"     {indicator}: {count}")
    
    print(f"\n4. Loading custom prompts...")
    custom_file = BASE_DIR / "prompts" / "custom_prompts.json"
    if custom_file.exists():
        with open(custom_file, 'r') as f:
            custom_prompts = json.load(f)
        print(f"   ✓ Loaded {len(custom_prompts)} custom prompts")
    else:
        custom_prompts = []
        print(f"   ⚠ No custom prompts found")
    
    print(f"\n5. Identifying gaps...")
    gaps = identify_gaps(coverage, custom_prompts)
    print(f"   Gap analysis:")
    for indicator, gap_info in gaps.items():
        status_icon = "✓" if gap_info['status'] == 'sufficient' else "⚠"
        print(f"     {status_icon} {indicator}: {gap_info['total_coverage']}/{gap_info['target']} "
              f"(gap: {gap_info['gap']})")
    
    print(f"\n6. Creating balanced sample...")
    balanced = balanced_sampling(all_prompts, samples_per_scenario=50)
    print(f"   ✓ Created balanced sample of {len(balanced)} prompts")
    
    print(f"\n7. Saving results...")
    
    mapping_output = {
        "metadata": {
            "total_prompts_analyzed": len(all_prompts),
            "balanced_sample_size": len(balanced),
            "custom_prompts_count": len(custom_prompts),
            "mapping_date": str(Path().cwd())
        },
        "coverage_analysis": coverage,
        "gap_analysis": gaps,
        "all_prompts": all_prompts[:1000],
        "balanced_sample": balanced,
        "multi_turn_conversations": multi_turn[:50]
    }
    
    output_file = OUTPUT_DIR / "dataset_mapping.json"
    with open(output_file, 'w') as f:
        json.dump(mapping_output, f, indent=2)
    print(f"   ✓ Saved mapping to {output_file}")
    
    print(f"\n8. Creating prompt sets by indicator...")
    
    prompt_sets = {
        "emotional_cues_prompts": [p for p in all_prompts if "L4.1" in p.get('indicators', []) or "L4.2" in p.get('indicators', [])],
        "hardship_scenarios": [p for p in all_prompts if any(ind in p.get('indicators', []) for ind in ["L4.5", "L4.6", "L4.7"])],
        "multi_turn_conversations": multi_turn
    }
    
    for set_name, prompts in prompt_sets.items():
        output_file = BASE_DIR / "prompts" / f"{set_name}.json"
        with open(output_file, 'w') as f:
            json.dump(prompts[:200], f, indent=2)
        print(f"   ✓ Created {set_name}.json ({len(prompts)} prompts, saved first 200)")
    
    print("\n" + "=" * 60)
    print("Mapping Complete!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  • Analyzed {len(all_prompts)} prompts from EmpatheticDialogues")
    print(f"  • Created balanced sample of {len(balanced)} prompts")
    print(f"  • Identified {len(multi_turn)} multi-turn conversations")
    print(f"  • Coverage: {coverage['scenarios_covered']} scenarios, {coverage['indicators_covered']} indicators")
    print(f"\nNext steps:")
    print(f"  1. Review dataset_mapping.json")
    print(f"  2. Check gap_analysis for missing coverage")
    print(f"  3. Combine with custom prompts")
    print(f"  4. Generate AI responses")

if __name__ == "__main__":
    main()

