# Measuring Affective Awareness and Support in AI Systems

This repository contains the complete implementation and evaluation framework for measuring Affective Awareness & Support in chat-based AI systems, as described in the paper "Measuring Affective Awareness and Support in AI Systems."

## Overview

This project evaluates two open-source chat models (Mistral-7B-Instruct and Llama-2-7b-chat) across seven indicators of affective awareness and support, grounded in clinical psychology principles.

## Structure

```
project-3/
├── data/
│   ├── datasets/              # EmpatheticDialogues and other datasets
│   ├── prompts/               # Prompt sets for evaluation
│   └── model_outputs/         # Generated responses and evaluations
├── scripts/                   # Evaluation and analysis scripts
├── figures/                   # Generated plots and visualizations
├── documentation/             # Detailed methodology and rubrics
├── paper.tex                  # LaTeX source for the paper
└── paper.pdf                  # Compiled paper
```

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Setup

1. Download EmpatheticDialogues dataset:
   ```bash
   # Dataset available on HuggingFace
   # See documentation/phase2_implementation_plan.md for details
   ```

2. Set up Ollama with models:
   ```bash
   ollama pull mistral:7b-instruct
   ollama pull llama2:7b-chat
   ```

### Running Evaluation

1. Generate model responses:
   ```bash
   python scripts/generate_responses.py
   ```

2. Evaluate responses:
   ```bash
   python scripts/evaluate_all_indicators.py
   ```

3. Run statistical analysis:
   ```bash
   jupyter notebook model_comparative_analysis.ipynb
   ```

## Key Files

- `documentation/phase1.md` - Detailed scoring rubrics for all 7 indicators
- `documentation/phase2_implementation_plan.md` - Data collection methodology
- `documentation/validity_analysis_report.md` - Validity and reliability analysis
- `scripts/evaluate_all_indicators.py` - Main evaluation script
- `model_comparative_analysis.ipynb` - Statistical analysis notebook

## Results

See `paper.pdf` for complete results, or `data/model_outputs/comparative_analysis_table.csv` for summary statistics.

## Citation

If you use this work, please cite:

```
Measuring Affective Awareness and Support in AI Systems
[Your Name/Institution]
2024
```

## License

[Specify your license]

