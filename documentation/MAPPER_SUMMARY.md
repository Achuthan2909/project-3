# Dataset Mapper Summary

## What Was Created

### 1. `dataset_mapper.py` - Complex Classification System

This script performs intelligent classification and mapping of prompts from EmpatheticDialogues:

#### Features:
- **Scenario Classification**: Maps prompts to 7 scenario types (job_loss, health, relationship, grief, financial, academic, loneliness)
- **Intensity Classification**: Classifies emotion intensity as mild/moderate/severe
- **L4 Indicator Mapping**: Automatically maps prompts to relevant L4 indicators
- **Multi-turn Extraction**: Extracts full conversation threads for L4.4 testing
- **Balanced Sampling**: Creates stratified samples across scenarios and intensities
- **Gap Analysis**: Identifies coverage gaps for each indicator

#### Output Files:
- `dataset_mapping.json` - Complete mapping with metadata (117,414 prompts analyzed)
- `emotional_cues_prompts.json` - Prompts for L4.1, L4.2 (200 prompts)
- `hardship_scenarios.json` - Prompts for L4.5, L4.6, L4.7 (200 prompts)
- `multi_turn_conversations.json` - Multi-turn prompts for L4.4 (200 prompts)

### 2. `combine_datasets.py` - Final Prompt Assembly

Combines custom prompts with dataset prompts:
- Deduplicates prompts
- Creates final prompt set ready for AI response generation
- Output: `final_prompts.json` (62 prompts)

## Results

### Coverage Analysis:
- **Total Prompts Analyzed**: 117,414 from EmpatheticDialogues
- **Scenarios Covered**: 9 types (including "general")
- **Indicators Covered**: All 7 L4 indicators
- **Multi-turn Conversations**: 17,768 identified

### Scenario Distribution:
- General: 61,867
- Relationship: 19,277
- Academic: 6,823
- Financial: 5,250
- Grief: 4,422
- Loneliness: 3,983
- Health: 3,489
- Job Loss: 1,208

### Indicator Coverage:
- L4.1 (Emotion Recognition): 37,779 prompts
- L4.2 (Empathy): 37,779 prompts
- L4.3 (De-escalation): 9,901 prompts
- L4.4 (Multi-turn): 50,637 prompts
- L4.5 (Dismissiveness): 330 prompts
- L4.6 (Toxic Positivity): 330 prompts
- L4.7 (Helpfulness): 13,229 prompts

### Gap Analysis:
All indicators have sufficient coverage (targets met or exceeded)

## How It Works

### Classification Logic:

1. **Scenario Classification**:
   - Uses keyword matching against 7 scenario types
   - Checks both prompt text and context field
   - Returns best match or "general" if no match

2. **Intensity Classification**:
   - Analyzes linguistic markers (devastated, stressed, a bit)
   - Classifies as severe/moderate/mild
   - Defaults to "moderate" if unclear

3. **L4 Indicator Mapping**:
   - L4.1, L4.2: All prompts with scenarios
   - L4.3: Prompts with anger/frustration + high intensity
   - L4.4: Multi-turn conversations or long prompts
   - L4.5, L4.6: Severe intensity prompts
   - L4.7: Financial, health, academic scenarios

4. **Multi-turn Extraction**:
   - Groups by conversation ID
   - Extracts conversations with 3+ turns
   - Preserves conversation structure

## Usage

### Run the Mapper:
```bash
cd project-3/data
source ../.venv/bin/activate
python3 dataset_mapper.py
```

### Combine Datasets:
```bash
python3 combine_datasets.py
```

### Use Final Prompts:
```bash
python3 generate_responses.py --prompts prompts/final_prompts.json --output model_outputs
```

## Next Steps

1. ✅ Dataset mapping complete
2. ✅ Prompt sets created
3. ⏭️ Generate AI responses (use `generate_responses.py`)
4. ⏭️ Evaluate responses using Phase 1 rubrics
5. ⏭️ Compare models statistically

## Notes

- The mapper uses keyword-based classification (not perfect, but good enough)
- Some prompts classified as "general" if they don't match specific scenarios
- Custom prompts fill gaps for L4.3, L4.5, L4.6 (de-escalation, dismissiveness)
- All prompts include rich metadata for documentation

