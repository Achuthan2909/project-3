# Phase 2 Implementation Plan: Prompt Design & Data Collection

## Recommended Approach: Hybrid (Existing Datasets + Custom Prompts)

### Rationale
- **Credibility:** Using validated datasets increases academic credibility
- **Coverage:** Custom prompts ensure all 7 L4 indicators are tested
- **Reproducibility:** Others can replicate using same datasets
- **Efficiency:** Saves time while maintaining quality

---

## Step 1: Dataset Acquisition (Week 2, Days 1-2)

### Primary Dataset: EmpatheticDialogues
```bash
# Download EmpatheticDialogues
cd project-3/data
git clone https://github.com/facebookresearch/EmpatheticDialogues.git
# Or download from HuggingFace
```

**What to extract:**
- Conversations matching your 7 scenario types
- Filter by emotion intensity
- Map to L4 indicators

### Secondary Datasets (Optional):
- DailyDialog (for multi-turn conversations)
- BlendedSkillTalk (for empathy evaluation)

---

## Step 2: Dataset Analysis & Mapping (Week 2, Days 2-3)

**Script:** `analysis/dataset_mapper.py`

**Tasks:**
1. Load EmpatheticDialogues
2. Map scenarios to your 7 types:
   - Job Loss → "job_loss"
   - Health Concerns → "health"
   - Relationship Issues → "relationship"
   - Grief → "grief"
   - Financial Stress → "financial"
   - Academic/Work Pressure → "academic"
   - Social Isolation → "loneliness"
3. Classify intensity (mild/moderate/severe)
4. Map to L4 indicators
5. Identify gaps

**Output:** `data/dataset_mapping.json`

---

## Step 3: Custom Prompt Creation (Week 2, Days 3-5)

**Create custom prompts ONLY for:**
- L4.3: De-escalation scenarios (15-20 prompts)
- L4.4: Multi-turn conversation starters (10-15 prompts)
- L4.5/L4.6: Dismissiveness test cases (20-30 prompts)
- L4.7: Helpfulness scenarios not in dataset (15-20 prompts)

**Use Phase 1 reference sets as templates**

**Output:** `data/prompts/custom_prompts.json`

---

## Step 4: Combined Dataset Assembly (Week 2, Day 5)

**Script:** `data/combine_datasets.py`

**Tasks:**
1. Merge existing dataset samples with custom prompts
2. Ensure balanced representation:
   - 50-60% from EmpatheticDialogues
   - 40-50% custom prompts
3. Create final prompt sets:
   - `emotional_cues_prompts.json` (L4.1, L4.2)
   - `hardship_scenarios.json` (L4.5, L4.6, L4.7)
   - `multi_turn_conversations.json` (L4.3, L4.4)
4. Document source for each prompt

**Output:** Final prompt sets with metadata

---

## Step 5: Model Response Generation (Week 3)

**Script:** `scripts/generate_responses.py`

**Models to test (FREE options):**
- **Mistral-7B-Instruct** (HuggingFace Inference API) - Recommended ⭐
- **Llama-2-7b-chat** (HuggingFace Inference API)
- **Zephyr-7b-beta** (HuggingFace Inference API) - Optional third model

**Setup:**
1. Sign up for HuggingFace account (free): https://huggingface.co
2. Get API token (free): Settings → Access Tokens
3. Install: `pip install requests`

**Parameters to document:**
- Model version
- Temperature (0.7 recommended)
- System prompts
- Max tokens (512 recommended)
- API timestamps
- Rate limit handling

**Process:**
1. Load final prompt sets
2. For each prompt:
   - Generate 3 responses per model (account for variability)
   - Add 2-second delay between requests (rate limiting)
   - Document all parameters
   - Save with metadata
3. Store in `data/model_outputs/`

**Rate Limit Management:**
- HuggingFace free tier: 1000 requests/day
- Process in batches
- Add delays between requests
- Spread over multiple days if needed

**Output:**
- `mistral7b_responses.json`
- `llama2_7b_responses.json`
- `zephyr7b_responses.json` (optional)

---

## File Structure

```
project-3/
├── data/
│   ├── datasets/
│   │   └── empathetic_dialogues/  (downloaded dataset)
│   ├── prompts/
│   │   ├── emotional_cues_prompts.json
│   │   ├── hardship_scenarios.json
│   │   ├── multi_turn_conversations.json
│   │   └── custom_prompts.json
│   ├── dataset_mapping.json
│   └── model_outputs/
│       ├── gpt4_responses.json
│       └── claude3_responses.json
├── analysis/
│   └── dataset_mapper.py
└── data/
    └── combine_datasets.py
    └── generate_responses.py
```

---

## Documentation Requirements

**In your paper's Method section, include:**

1. **Dataset Sources:**
   - "We use EmpatheticDialogues (Rashkin et al., 2019) as our primary dataset..."
   - "We supplement with custom prompts for L4.3, L4.4, L4.5, L4.6 as these dimensions are not fully covered..."

2. **Prompt Selection Criteria:**
   - How you filtered/mapped existing dataset
   - Why custom prompts were needed
   - How you ensured balanced representation

3. **Model Configuration:**
   - Exact model versions
   - Temperature settings
   - System prompts used
   - Number of runs per prompt

---

## Advantages of This Approach

✅ **Credibility:** Using validated datasets
✅ **Completeness:** Custom prompts cover all L4 indicators
✅ **Reproducibility:** Clear documentation of sources
✅ **Validity:** Reduces prompt engineering bias concerns
✅ **Efficiency:** Leverages existing work

---

## Next Steps

1. Download EmpatheticDialogues
2. Run dataset mapper to analyze coverage
3. Create custom prompts for identified gaps
4. Generate model responses
5. Document everything

