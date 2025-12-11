# Unified Indicator Evaluation Script

## Overview

This script evaluates all indicators (L4.1-L4.7) for model responses in a single unified process. It efficiently batches prompts and includes only the rubrics needed for each batch.

## Features

- **Unified Evaluation**: Evaluates all indicators in one script
- **Efficient Batching**: Groups prompts and includes only needed rubrics per batch
- **Random Run Selection**: Randomly selects 1 run per prompt (with fixed seed for reproducibility)
- **Incremental Saving**: Saves results after each batch (resumable)
- **Cost Optimized**: Only includes rubrics needed for each batch

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or pass it as an argument:
```bash
python evaluate_all_indicators.py llama2_responses.json --api-key your-key
```

## Usage

Evaluate all indicators for Llama2 model:
```bash
python scripts/evaluate_all_indicators.py llama2_responses.json
```

Evaluate all indicators for Mistral model:
```bash
python scripts/evaluate_all_indicators.py mistral_responses.json
```

Custom batch size (default is 5):
```bash
python scripts/evaluate_all_indicators.py llama2_responses.json --batch-size 6
```

## Output

Results are saved to:
- `data/model_outputs/all_indicators_evaluations_llama-2-7b-chat.json`
- `data/model_outputs/all_indicators_evaluations_mistral-7b-instruct.json`

Each file contains:
- All evaluated prompts with scores for each indicator (1-5)
- Justifications for each score
- Summary statistics per indicator (average, count, distribution)

## Cost Estimation

- 880 unique prompts per model
- Batch size: 5 prompts per API call
- ~176 API calls per model
- Estimated cost: ~$3.50-4.00 per model (using GPT-3.5-turbo)
- Total for both models: ~$7-8

## How It Works

1. **Loads Rubrics**: Parses all 7 rubrics from `documentation/phase1.md`
2. **Loads Responses**: Loads model responses and randomly selects 1 run per prompt
3. **Batches Prompts**: Groups prompts into batches of 5-6
4. **Smart Rubric Inclusion**: For each batch, includes only the rubrics needed for that batch's indicators
5. **Evaluates**: Calls API once per batch, evaluating all indicators for all prompts in batch
6. **Saves Incrementally**: Saves results after each batch (can resume if interrupted)

## Example Batch

If a batch contains:
- Prompt A: [L4.1, L4.2]
- Prompt B: [L4.4]
- Prompt C: [L4.1, L4.2, L4.4]

The script will:
- Include rubrics: L4.1, L4.2, L4.4 (only these 3, not all 7)
- Evaluate all 3 prompts in one API call
- Return scores for all specified indicators

## Notes

- Random seed is fixed (42) for reproducibility
- Results are saved incrementally (checkpoint after each batch)
- If the script fails, you can re-run it and it will continue (you may need to manually remove completed items)
- All indicators use the same LLM evaluation approach (no special handling)
