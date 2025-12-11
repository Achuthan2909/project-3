# Dataset Recommendations for Phase 2

## Recommendation: Hybrid Approach

**Primary Strategy:** Use existing validated datasets (70-80%)
**Supplement:** Custom prompts for uncovered L4 indicators (20-30%)

This approach maximizes credibility while ensuring complete coverage.

---

## Recommended Existing Datasets

### 1. **EmpatheticDialogues** (Facebook Research)
- **What it covers:** L4.1, L4.2 (Emotion recognition, Empathy)
- **Size:** ~25k conversations
- **Scenarios:** Emotional support conversations across 32 situations
- **Why use it:** Validated, peer-reviewed, widely cited
- **Citation:** Rashkin et al. (2019) "Towards Empathetic Open-domain Conversation Models"
- **Link:** https://github.com/facebookresearch/EmpatheticDialogues

### 2. **Mental Health Conversations Dataset**
- **What it covers:** L4.1, L4.2, L4.3, L4.7 (Emotional support, De-escalation, Helpfulness)
- **Examples:** 
  - Crisis Text Line dataset (if available)
  - r/SuicideWatch conversations (with proper ethics review)
- **Why use it:** Real-world emotional distress scenarios
- **Note:** Requires careful ethical handling and IRB approval

### 3. **DailyDialog** (with emotion annotations)
- **What it covers:** L4.1 (Emotion recognition)
- **Size:** ~13k multi-turn conversations
- **Why use it:** Multi-turn structure good for L4.4 (sentiment change)
- **Link:** https://www.aclweb.org/anthology/I17-1099/

### 4. **BlendedSkillTalk** (ParlAI)
- **What it covers:** L4.1, L4.2, L4.7
- **Why use it:** Combines personality, knowledge, and empathy
- **Link:** https://parl.ai/projects/blended_skill_talk/

### 5. **SafetyPrompts.com** (as mentioned in assignment)
- **What it covers:** L4.5, L4.6 (Dismissiveness, Toxic positivity)
- **Why use it:** Specifically designed for safety evaluation
- **Note:** Check if it includes emotional support scenarios

### 6. **PersonaChat** (with emotional annotations)
- **What it covers:** L4.1, L4.2
- **Why use it:** Persona-based conversations with emotional content

---

## Custom Prompts Needed (Gap Analysis)

Based on your 7 L4 indicators, you'll likely need custom prompts for:

### **L4.3: De-escalation** (Limited in existing datasets)
- Escalating conversation scenarios
- Anger/frustration that needs de-escalation
- **Custom prompts needed:** ~15-20 scenarios

### **L4.4: Multi-turn Sentiment Change** (Partial coverage)
- Long-form conversations (10+ turns)
- Tracking sentiment trajectory
- **Custom prompts needed:** ~10-15 conversation starters

### **L4.5 & L4.6: Dismissiveness Detection** (Limited coverage)
- Scenarios likely to trigger dismissive responses
- Toxic positivity test cases
- **Custom prompts needed:** ~20-30 scenarios

### **L4.7: Helpfulness in Hardship** (Partial coverage)
- Scenarios requiring actionable support
- Financial, practical crisis scenarios
- **Custom prompts needed:** ~15-20 scenarios

---

## Implementation Strategy

### Step 1: Dataset Selection & Adaptation
1. Download EmpatheticDialogues (primary)
2. Extract relevant scenarios matching your 7 scenario types
3. Filter for intensity levels (mild/moderate/severe)
4. Map to your L4 indicators

### Step 2: Custom Prompt Creation
1. Create prompts for gaps identified above
2. Use Phase 1 reference sets as templates
3. Ensure variety in intensity and emotional vocabulary
4. Validate against Phase 1 rubrics

### Step 3: Combined Dataset
1. Merge existing dataset samples with custom prompts
2. Ensure balanced representation:
   - ~50-60% from existing datasets
   - ~40-50% custom prompts (focused on gaps)
3. Document source for each prompt

---

## Credibility Benefits of Using Existing Datasets

1. **Peer Review:** Datasets are validated by research community
2. **Reproducibility:** Others can replicate using same data
3. **Comparability:** Compare your results to published benchmarks
4. **Validity:** Reduces concerns about prompt engineering bias
5. **Efficiency:** Saves significant time

---

## How to Cite in Your Paper

**Method Section:**
"We use a hybrid approach combining validated datasets with custom prompts. Primary evaluation uses EmpatheticDialogues (Rashkin et al., 2019) for emotion recognition and empathy assessment (L4.1, L4.2). We supplement with custom prompts for de-escalation (L4.3), multi-turn sentiment tracking (L4.4), and dismissiveness detection (L4.5, L4.6), as these dimensions are not fully covered in existing datasets. Custom prompts were designed following our Phase 1 rubrics and validated against reference response sets."

---

## Quick Decision Guide

**Use Existing Datasets If:**
- ✅ You want maximum credibility
- ✅ You want to compare to prior work
- ✅ You have limited time
- ✅ You want peer-reviewed validation

**Use Custom Prompts If:**
- ✅ Existing datasets don't cover your L4 indicators
- ✅ You need specific scenario types
- ✅ You want perfect alignment with Phase 1 rubrics

**Best Approach:**
- ✅ **Hybrid:** Use existing datasets + custom prompts for gaps
- ✅ Document both sources clearly
- ✅ Explain why custom prompts were needed

---

## Next Steps

1. **Download EmpatheticDialogues** (start here)
2. **Analyze coverage** - map to your L4 indicators
3. **Identify gaps** - what's missing?
4. **Create custom prompts** - only for gaps
5. **Combine and document** - clear attribution

This approach gives you the credibility of existing datasets while ensuring complete coverage of all 7 L4 indicators.

