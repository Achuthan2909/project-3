# Free Models Guide for Phase 2

## Best Free Options for Students

### Option 1: HuggingFace Inference API (Recommended) ⭐

**What it is:** Free API access to open-source models
**Cost:** FREE (with rate limits)
**Models available:** Llama 2, Mistral, Zephyr, etc.

**How to use:**
1. Sign up at https://huggingface.co (free)
2. Get API token (free)
3. Use Inference API (free tier: 1000 requests/day)

**Recommended models:**
- `meta-llama/Llama-2-7b-chat-hf` (Free, good quality)
- `mistralai/Mistral-7B-Instruct-v0.2` (Free, excellent)
- `HuggingFaceH4/zephyr-7b-beta` (Free, instruction-tuned)

**Pros:**
- ✅ Completely free
- ✅ No GPU needed
- ✅ Easy to use
- ✅ Good model quality
- ✅ Reproducible

**Cons:**
- ⚠️ Rate limits (1000 requests/day)
- ⚠️ Slower than paid APIs

---

### Option 2: Local Models (If you have GPU access)

**What it is:** Run models on your own machine/university GPU

**Requirements:**
- GPU with 8GB+ VRAM (or use Google Colab free tier)
- Python environment

**Recommended models:**
- `Llama-2-7b-chat` (via Ollama or HuggingFace Transformers)
- `Mistral-7B-Instruct`
- `Zephyr-7B-beta`

**How to use:**
```python
# Using Ollama (easiest)
pip install ollama
ollama pull llama2:7b-chat
ollama run llama2:7b-chat

# Or using HuggingFace Transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
```

**Pros:**
- ✅ No rate limits
- ✅ Complete control
- ✅ No API costs

**Cons:**
- ⚠️ Requires GPU access
- ⚠️ Setup complexity
- ⚠️ Slower inference

---

### Option 3: Free API Credits (Student Programs)

**OpenAI for Students:**
- Some universities have partnerships
- Check if your school provides credits
- Free tier: $5 credit (limited)

**Anthropic (Claude):**
- Check for student programs
- Limited free tier

**Google Colab:**
- Free GPU access (T4 GPU)
- Can run local models
- Time limits (12 hours max session)

**Pros:**
- ✅ Access to premium models
- ✅ Good quality

**Cons:**
- ⚠️ Limited credits
- ⚠️ May not be available
- ⚠️ Need to apply

---

### Option 4: HuggingChat (Web Interface)

**What it is:** Free web-based chat interface
**URL:** https://huggingface.co/chat

**Models available:**
- Llama 2
- Mistral
- Zephyr

**Pros:**
- ✅ No setup needed
- ✅ Free
- ✅ Easy to use

**Cons:**
- ⚠️ Manual data collection (copy-paste)
- ⚠️ Not automated
- ⚠️ Slower for large batches

---

## Recommended Setup for Your Project

### Primary Approach: HuggingFace Inference API

**Why:**
- Free and reliable
- Easy to automate
- Good model quality
- Reproducible

**Models to compare:**
1. **Mistral-7B-Instruct** (Best quality, free)
2. **Llama-2-7b-chat** (Good quality, free)
3. **Zephyr-7b-beta** (Instruction-tuned, free)

**This gives you:**
- ✅ 2-3 models to compare (meets assignment requirement)
- ✅ All free
- ✅ Reproducible
- ✅ Good quality

---

## Implementation Code

### Using HuggingFace Inference API

```python
import requests
import json
import time

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer YOUR_HF_TOKEN"}

def query_model(prompt, max_retries=3):
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512,
            "return_full_text": False
        }
    }
    
    for attempt in range(max_retries):
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            # Model is loading, wait
            time.sleep(10)
        else:
            print(f"Error: {response.status_code}")
            time.sleep(2)
    
    return None

# Example usage
prompt = "I just got laid off and I'm feeling devastated."
response = query_model(prompt)
print(response)
```

### Using Ollama (Local)

```python
import requests
import json

def query_ollama(prompt, model="llama2:7b-chat"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }
    
    response = requests.post(url, json=payload)
    return response.json()["response"]

# Example usage
prompt = "I just got laid off and I'm feeling devastated."
response = query_ollama(prompt)
print(response)
```

---

## Rate Limit Management

**HuggingFace Free Tier:**
- 1000 requests/day
- ~30 requests/hour

**Strategy:**
1. Batch your prompts (process in chunks)
2. Add delays between requests
3. Use multiple accounts if needed (ethical, but check ToS)
4. Process over multiple days if needed

**Code for rate limiting:**
```python
import time
from datetime import datetime

def rate_limited_request(prompt, delay=2):
    """Add delay to respect rate limits"""
    response = query_model(prompt)
    time.sleep(delay)  # Wait 2 seconds between requests
    return response
```

---

## Cost Comparison

| Option | Cost | Quality | Ease of Use | Rate Limits |
|-------|------|---------|-------------|-------------|
| HuggingFace API | FREE | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 1000/day |
| Local (Ollama) | FREE | ⭐⭐⭐⭐ | ⭐⭐⭐ | None |
| Google Colab | FREE | ⭐⭐⭐⭐ | ⭐⭐⭐ | 12hr sessions |
| HuggingChat | FREE | ⭐⭐⭐ | ⭐⭐ | Manual |

**Recommendation:** Start with HuggingFace Inference API

---

## Next Steps

1. **Sign up for HuggingFace** (free)
2. **Get API token** (free)
3. **Test with 1-2 prompts** to verify it works
4. **Create batch processing script** with rate limiting
5. **Generate responses** for all prompts

---

## Troubleshooting

**"Model is loading" error:**
- Wait 10-20 seconds and retry
- First request takes longer (model needs to load)

**Rate limit exceeded:**
- Wait 1 hour
- Process in smaller batches
- Spread over multiple days

**API token issues:**
- Check token is valid
- Verify account is active
- Check rate limit status

---

## Documentation for Your Paper

**In Method section, write:**

"We evaluate responses from two open-source models accessed via HuggingFace Inference API: Mistral-7B-Instruct (Mistral AI, 2024) and Llama-2-7b-chat (Touvron et al., 2023). These models were selected for their strong performance on instruction-following tasks and availability through free academic access. All API calls were made using temperature=0.7, max_tokens=512, with identical system prompts across models to ensure fair comparison."

This demonstrates:
- ✅ Academic rigor (citing models)
- ✅ Reproducibility (free access)
- ✅ Fair comparison (same parameters)







