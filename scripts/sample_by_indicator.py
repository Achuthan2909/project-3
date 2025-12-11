import json
import csv
import random
from pathlib import Path
from collections import defaultdict, Counter

BASE_DIR = Path(__file__).parent
DATASETS_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = BASE_DIR / "prompts"

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


def classify_scenario(text, ctx=""):
    s = text.lower()
    c = ctx.lower() if ctx else ""
    full = s + " " + c
    scores = {}
    for name, words in SCENARIO_KEYWORDS.items():
        n = sum(1 for w in words if w in full)
        if n:
            scores[name] = n
    if not scores:
        return None
    return max(scores.items(), key=lambda x: x[1])[0]


def classify_intensity(text):
    s = text.lower()
    sev = sum(1 for w in INTENSITY_INDICATORS["severe"] if w in s)
    mod = sum(1 for w in INTENSITY_INDICATORS["moderate"] if w in s)
    mil = sum(1 for w in INTENSITY_INDICATORS["mild"] if w in s)
    if sev:
        return "severe"
    if mod:
        return "moderate"
    if mil:
        return "mild"
    return "moderate"


def map_indicators(scenario, intensity, emotion, text):
    inds = []
    if scenario:
        inds.append("L4.1")
        inds.append("L4.2")
        if scenario in ["financial", "health", "academic"]:
            inds.append("L4.7")
    if intensity == "severe":
        inds.extend(["L4.5", "L4.6"])
    s = text.lower()
    if any(w in s for w in ["angry", "furious", "mad", "upset", "rage", "hate"]):
        inds.append("L4.3")
    if "?" in text or len(text.split()) > 18:
        inds.append("L4.4")
    return sorted(set(inds))


def load_ed():
    all_rows = []
    ed_dir = DATASETS_DIR / "empathetic_dialogues"
    for split in ["train", "valid", "test"]:
        fp = ed_dir / f"{split}.csv"
        if not fp.exists():
            continue
        with open(fp, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                txt = (row.get("prompt") or "").strip()
                if not txt:
                    continue
                ctx = (row.get("context") or "").strip()
                emo = EMOTION_CONTEXT_MAP.get(ctx.lower(), ctx.lower())
                scen = classify_scenario(txt, ctx)
                inten = classify_intensity(txt)
                inds = map_indicators(scen, inten, emo, txt)
                p = {
                    "prompt_id": f"ED_{row.get('conv_id','')}_{row.get('utterance_idx','')}",
                    "prompt_text": txt,
                    "source": "empathetic_dialogues",
                    "source_file": fp.name,
                    "scenario_type": scen or "general",
                    "emotion": emo,
                    "intensity": inten,
                    "context_field": ctx,
                    "indicators": inds,
                    "conv_id": row.get("conv_id", ""),
                    "utterance_idx": row.get("utterance_idx", ""),
                    "speaker_idx": row.get("speaker_idx", "")
                }
                all_rows.append(p)
    return all_rows


def sample_by_indicator(target_per_indicator=150, seed=42):
    random.seed(seed)
    print("=" * 60)
    print("Sampling by indicator from EmpatheticDialogues")
    print("=" * 60)
    prompts = load_ed()
    print(f"\nLoaded {len(prompts)} prompts from empathetic_dialogues")
    by_indicator = defaultdict(list)
    for p in prompts:
        for ind in p.get("indicators", []):
            by_indicator[ind].append(p)
    print("\nAvailable per indicator:")
    for ind, lst in sorted(by_indicator.items()):
        print(f"  {ind}: {len(lst)}")
    selected = []
    for ind, lst in by_indicator.items():
        if not lst:
            continue
        k = min(target_per_indicator, len(lst))
        picked = random.sample(lst, k)
        selected.extend(picked)
        print(f"  -> selected {k} for {ind}")
    by_text = {}
    for p in selected:
        t = p["prompt_text"].strip()
        if not t:
            continue
        if t not in by_text:
            by_text[t] = p
    final = list(by_text.values())
    print(f"\nAfter dedupe: {len(final)} unique prompts")
    ind_counts = Counter()
    for p in final:
        for ind in p.get("indicators", []):
            ind_counts[ind] += 1
    print("\nFinal coverage per indicator:")
    for ind in sorted(ind_counts):
        print(f"  {ind}: {ind_counts[ind]}")
    scen_counts = Counter(p.get("scenario_type", "unknown") for p in final)
    print("\nScenario distribution:")
    for scen, c in scen_counts.most_common():
        print(f"  {scen}: {c}")
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    out_file = OUTPUT_DIR / "final_prompts_sampled.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2)
    print(f"\nSaved {len(final)} prompts to {out_file}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            n = 150
    else:
        n = 150
    sample_by_indicator(target_per_indicator=n)


