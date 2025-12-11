# Measuring Affective Awareness and Support in AI Systems

This repository contains the complete implementation and evaluation framework for measuring Affective Awareness & Support in chat-based AI systems. The project evaluates two open-source models (Mistral-7B-Instruct and Llama-2-7b-chat) across seven indicators grounded in clinical psychology principles.

## Repository Structure

```
project-3/
├── data/
│   ├── datasets/              # EmpatheticDialogues dataset
│   ├── prompts/               # Evaluation prompt sets
│   └── model_outputs/         # Generated responses and evaluations
├── scripts/                    # Evaluation and analysis scripts
├── figures/                    # Generated visualizations
├── documentation/              # Methodology and rubrics
│   ├── scoring_rubrics.md    # Detailed scoring criteria for all 7 indicators
│   └── validity_analysis_report.md  # Validity and reliability analysis
├── paper.tex                   # LaTeX source for the paper
└── paper.pdf                   # Compiled paper
```

## Quick Start

### Prerequisites

1. **Python 3.8+** with required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ollama** installed and running:
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull mistral:7b-instruct
   ollama pull llama2:7b-chat
   ```

3. **OpenAI API key** (for evaluation using ChatGPT):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

### Running the Evaluation

#### Step 1: Generate Model Responses

Generate responses from both models for all prompts:

```bash
python scripts/generate_responses.py
```

This script:
- Loads prompts from `data/prompts/`
- Generates responses using Ollama (Mistral and Llama-2)
- Saves outputs to `data/model_outputs/`
- Uses parameters: temperature=0.7, max_tokens=256

#### Step 2: Evaluate Responses

Evaluate all responses using ChatGPT with expert-defined rubrics:

```bash
python scripts/evaluate_all_indicators.py
```

This script:
- Loads model responses from `data/model_outputs/`
- Uses ChatGPT (GPT-4) to evaluate each response against rubrics
- Scores all 7 indicators (L4.1 through L4.7)
- Saves evaluations to `data/model_outputs/all_indicators_evaluations_*.json`

#### Step 3: Statistical Analysis

Run comparative analysis:

```bash
jupyter notebook model_comparative_analysis.ipynb
```

This generates:
- Mean scores and standard deviations
- Statistical tests (t-test, Mann-Whitney U)
- Effect sizes (Cohen's d)
- Visualizations in `figures/`

## Key Files

### Scripts
- `scripts/generate_responses.py` - Generate model responses via Ollama
- `scripts/evaluate_all_indicators.py` - Evaluate responses using ChatGPT
- `scripts/sample_by_indicator.py` - Sample prompts by indicator
- `model_comparative_analysis.ipynb` - Statistical analysis and visualization

### Documentation
- `documentation/scoring_rubrics.md` - Complete scoring rubrics for all 7 indicators
- `documentation/validity_analysis_report.md` - Validity and reliability evidence

### Data
- `data/prompts/` - All evaluation prompts (EmpatheticDialogues + custom)
- `data/model_outputs/` - Generated responses and evaluations
- `data/dataset_mapping.json` - Mapping of prompts to indicators

## Evaluation Framework

The evaluation measures seven indicators:

1. **L4.1: Recognizes and Responds to Emotional Cues** - Emotion recognition accuracy
2. **L4.2: Empathy Quality** - Depth of empathic understanding
3. **L4.3: De-escalation** - Ability to calm distressed users
4. **L4.4: Sentiment Change Across Multi-Turn Sessions** - Conversation trajectory improvement
5. **L4.5: Avoids Dismissiveness and Toxic Positivity** - Validation quality
6. **L4.6: Dismissiveness Occurrences per 1k Interactions** - Frequency of dismissive responses
7. **L4.7: Users Rate the AI as Helpful in Hardship Scenarios** - Perceived helpfulness

Each indicator is scored 1-5 using expert-defined rubrics grounded in clinical psychology (Rogers, Linehan, Roberts, etc.).

## Results

Complete results are available in:
- `paper.pdf` - Full paper with detailed analysis
- `data/model_outputs/comparative_analysis_table.csv` - Summary statistics
- `figures/` - Visualizations of model comparisons

## Replication

All materials needed for replication are included:
- Complete prompt sets with metadata
- Evaluation rubrics and criteria
- Model responses and evaluations
- Statistical analysis code
- Configuration details (temperature, system prompts, etc.)

See the paper's Appendix section for detailed replication instructions and GitHub links.

## Citation

If you use this work, please cite:

```
Measuring Affective Awareness and Support in AI Systems
[Your Name/Institution]
2024
```

## License

[Specify your license]
