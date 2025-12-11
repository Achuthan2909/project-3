import json
import time
from datetime import datetime
from pathlib import Path

import ollama

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = DATA_DIR / "prompts"
OUT_DIR = DATA_DIR / "model_outputs"

MODELS = {
    "mistral": {
        "model_id": "mistral:7b-instruct",
        "name": "Mistral-7B-Instruct"
    },
    "llama2": {
        "model_id": "llama2:7b-chat",
        "name": "Llama-2-7b-chat"
    }
}

SYSTEM_PROMPT = (
    "You are a helpful, empathetic assistant. "
    "Respond to the user's message with understanding and support."
)


def generate_one(model_id, user_message, system_prompt=SYSTEM_PROMPT, max_new_tokens=256, temperature=0.7, max_retries=3, delay=2):
    for i in range(max_retries):
        try:
            response = ollama.chat(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                options={
                    "temperature": temperature,
                    "num_predict": max_new_tokens,
                }
            )
            return response["message"]["content"].strip()
        except Exception as e:
            print(f"   error: {e} (attempt {i+1}/{max_retries})")
            if i < max_retries - 1:
                time.sleep(delay * (i + 1))
    return None


def generate_responses(prompts_file, models, runs=3, limit=None):
    with open(prompts_file, "r", encoding="utf-8") as f:
        prompts_data = json.load(f)

    if limit:
        prompts_data = prompts_data[:limit]
        print(f"Limiting to first {limit} prompts")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for key in models:
        if key not in MODELS:
            print(f"Unknown model key: {key}")
            continue

        info = MODELS[key]
        model_id = info["model_id"]

        print(f"\n=== {info['name']} ({model_id}) ===")

        out_path = OUT_DIR / f"{key}_responses.json"
        
        processed_ids = set()
        res = {
            "model": info["name"],
            "model_id": model_id,
            "generation_date": datetime.now().isoformat(),
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 256,
                "system_prompt": SYSTEM_PROMPT,
                "num_runs_per_prompt": runs,
            },
            "responses": [],
        }
        
        if out_path.exists():
            try:
                with open(out_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                    res["responses"] = existing.get("responses", [])
                    processed_ids = {r["prompt_id"] for r in res["responses"]}
                    print(f"Resuming: Found {len(processed_ids)} already processed prompts")
            except Exception as e:
                print(f"Could not load existing file: {e}, starting fresh")

        n = len(prompts_data)
        print(f"Total prompts: {n}")

        for idx, p in enumerate(prompts_data, 1):
            pid = p.get("prompt_id", f"p_{idx}")
            text = p.get("prompt_text") or p.get("initial_prompt") or ""
            text = text.strip()
            if not text:
                continue

            if pid in processed_ids:
                print(f"[{idx}/{n}] {pid} (already processed, skipping)")
                continue

            print(f"[{idx}/{n}] {pid}")

            runs_list = []
            for r in range(1, runs + 1):
                print(f"   run {r}/{runs}...", end=" ", flush=True)
                start_time = time.time()
                ans = generate_one(model_id, text)
                elapsed = time.time() - start_time
                if ans:
                    runs_list.append(
                        {
                            "run": r,
                            "response": ans,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                    print(f"ok ({elapsed:.1f}s)")
                else:
                    print(f"fail ({elapsed:.1f}s)")

                if r < runs:
                    time.sleep(1.5)

            res["responses"].append(
                {
                    "prompt_id": pid,
                    "prompt_metadata": {k: v for k, v in p.items() if k != "prompt_text"},
                    "prompt_text": text,
                    "responses": runs_list,
                }
            )

            if idx % 5 == 0:
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(res, f, indent=2)
                print(f"   checkpoint saved ({len(res['responses'])}/{n} prompts)")

            time.sleep(0.5)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
        print(f"\nSaved final results to {out_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=str, required=True)
    parser.add_argument("--models", nargs="+", default=["mistral", "llama2"])
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--limit", type=int, default=None, help="Limit number of prompts to process")
    args = parser.parse_args()

    generate_responses(args.prompts, args.models, args.runs, args.limit)