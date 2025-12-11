# Phase 2 Datasets Summary

## ✅ Downloaded Datasets

### 1. EmpatheticDialogues (Primary Dataset)
- **Source**: Facebook Research (Rashkin et al., 2019)
- **Size**: ~25k conversations
- **Files**: 
  - `train.csv` (84,170 samples)
  - `valid.csv` (12,079 samples)
  - `test.csv` (10,974 samples)
- **Location**: `data/datasets/EmpatheticDialogues/`
- **Covers Indicators**: L4.1 (Emotion Recognition), L4.2 (Empathy), L4.7 (Helpfulness)
- **Scenario Types**: Job loss, health, relationship, grief, financial, academic, loneliness

### 2. Emotions Dataset
- **Source**: HuggingFace (dair-ai/emotion)
- **Size**: 20,000 text entries
- **Files**:
  - `emotions_train.csv` (16,000 samples)
  - `emotions_validation.csv` (2,000 samples)
  - `emotions_test.csv` (2,000 samples)
- **Location**: `data/datasets/emotions/`
- **Covers Indicators**: L4.1 (Emotion Recognition)
- **Emotions**: 6 categories (joy, sadness, anger, fear, love, surprise)

### 3. BlendedSkillTalk
- **Source**: HuggingFace (ParlAI)
- **Size**: ~6,800 conversations
- **Files**:
  - `blended_skill_talk_train.csv` (4,819 samples)
  - `blended_skill_talk_validation.csv` (1,009 samples)
  - `blended_skill_talk_test.csv` (980 samples)
- **Location**: `data/datasets/blended_skill_talk/`
- **Covers Indicators**: L4.1, L4.2, L4.7
- **Features**: Combines personality, knowledge, and empathy

## ✅ Custom Prompts Created

**File**: `data/prompts/custom_prompts.json`
**Total**: 20 custom prompts

### Breakdown by Indicator:
- **L4.3 (De-escalation)**: 4 prompts
- **L4.4 (Multi-turn sentiment)**: 3 prompts
- **L4.5 (Dismissiveness)**: 4 prompts
- **L4.6 (Toxic Positivity)**: 4 prompts
- **L4.7 (Helpfulness)**: 4 prompts
- **L4.1 (Emotion Recognition)**: 1 prompt (mixed emotions)
- **L4.2 (Empathy)**: 1 prompt

### Custom Prompt Sources:
- Based on Phase 1 reference scenarios
- Designed to fill gaps in existing datasets
- Cover specific test cases from Phase 1 exercises

## 📊 Coverage Analysis

### Indicators Coverage:
- ✅ **L4.1** (Emotion Recognition): EmpatheticDialogues + Emotions + Custom
- ✅ **L4.2** (Empathy): EmpatheticDialogues + BlendedSkillTalk + Custom
- ✅ **L4.3** (De-escalation): Custom prompts (primary)
- ✅ **L4.4** (Multi-turn sentiment): Custom prompts (primary)
- ✅ **L4.5** (Dismissiveness): Custom prompts (primary)
- ✅ **L4.6** (Toxic Positivity): Custom prompts (primary)
- ✅ **L4.7** (Helpfulness): EmpatheticDialogues + Custom

## 📁 Directory Structure

```
data/
├── datasets/
│   ├── empathetic_dialogues/    (Primary dataset - train.csv, valid.csv, test.csv)
│   ├── emotions/                (Emotion classification - train/valid/test.csv)
│   └── blended_skill_talk/      (Multi-skill conversations - train/valid/test.csv)
├── prompts/
│   └── custom_prompts.json     (20 custom prompts)
├── model_outputs/              (Will contain AI responses)
├── download_datasets.py         (Download script)
├── generate_responses.py        (Response generation script)
├── dataset_info.json           (Metadata)
└── DATASETS_SUMMARY.md         (This file)
```

## 🎯 Next Steps

1. **Analyze Datasets**: Map existing datasets to L4 indicators
2. **Extract Prompts**: Pull relevant prompts from EmpatheticDialogues
3. **Combine**: Merge existing dataset prompts with custom prompts
4. **Generate Responses**: Use `generate_responses.py` to get AI model outputs
5. **Evaluate**: Use Phase 1 rubrics to score responses

## 📝 Notes

- EmpatheticDialogues is the primary dataset (most comprehensive)
- Custom prompts fill gaps for L4.3, L4.4, L4.5, L4.6
- All prompts are ready for response generation
- Total prompt pool: ~107k from datasets + 20 custom = comprehensive coverage

