# Phase 2: Quick Start Guide (Free Models)

## Setup (5 minutes)

### 1. Get HuggingFace Token (FREE)
1. Go to https://huggingface.co
2. Sign up (free account)
3. Go to Settings → Access Tokens
4. Create new token (read access is enough)
5. Copy the token

### 2. Install Dependencies
```bash
cd project-3
pip install -r requirements.txt
```

### 3. Set Your Token
Edit `data/generate_responses.py`:
```python
HF_TOKEN = "YOUR_ACTUAL_TOKEN_HERE"  # Replace with your token
```

Or use environment variable:
```bash
export HF_TOKEN="your_token_here"
```

## Usage

### Generate Responses for Prompts

```bash
# Basic usage (2 models, 3 runs each)
python data/generate_responses.py \
    --prompts data/prompts/emotional_cues_prompts.json \
    --output data/model_outputs \
    --models mistral llama2 \
    --runs 3

# Single model
python data/generate_responses.py \
    --prompts data/prompts/hardship_scenarios.json \
    --models mistral \
    --runs 3
```

## Free Models Available

- **Mistral-7B-Instruct** ⭐ (Best quality)
- **Llama-2-7b-chat** (Good quality)
- **Zephyr-7b-beta** (Instruction-tuned)

All completely FREE via HuggingFace Inference API!

## Rate Limits

- **Free tier:** 1000 requests/day
- **Strategy:** Process in batches over multiple days if needed
- Script automatically adds 2-second delays between requests

## Output Format

Results saved as JSON:
```json
{
  "model": "Mistral-7B-Instruct",
  "generation_date": "2024-01-15T10:30:00",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 512
  },
  "responses": [
    {
      "prompt_id": "EC_JL_001",
      "prompt_text": "...",
      "responses": [
        {"run": 1, "response": "...", "timestamp": "..."},
        {"run": 2, "response": "...", "timestamp": "..."},
        {"run": 3, "response": "...", "timestamp": "..."}
      ]
    }
  ]
}
```

## Troubleshooting

**"Model is loading" error:**
- Wait 20 seconds and retry (automatic in script)

**Rate limit exceeded:**
- Wait 1 hour or process tomorrow
- Free tier resets daily

**Token not working:**
- Check token is valid
- Verify account is active
- Token should start with "hf_"

## Next Steps

1. ✅ Get HuggingFace token
2. ✅ Install dependencies
3. ✅ Create/load your prompts
4. ✅ Run generation script
5. ✅ Analyze results (Phase 3)

For detailed information, see:
- `documentation/free_models_guide.md` - Complete guide
- `documentation/phase2_implementation_plan.md` - Full plan







