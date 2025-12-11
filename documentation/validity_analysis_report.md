# Validity Analysis Report

## 1. Content Validity

### Expert-Defined Rubrics
All rubrics were developed by experts with strong theoretical foundations:

- Rogers & Farson (1957) - Active Listening
- Plutchik's Psycho-evolutionary Theory of Emotion
- Ekman's Universal Emotions
- Linehan's Biosocial Theory (DBT)
- Roberts' Seven-Stage Crisis Intervention Model
- Fredrickson's Broaden-and-Build Theory
- Self-Determination Theory (Ryan & Deci)

### Scenario Coverage
- Job Loss/Unemployment
- Health Concerns/Medical Anxiety
- Relationship Issues/Breakup
- Grief/Loss
- Financial Stress
- Academic/Work Pressure
- Social Isolation/Loneliness

## 2. Construct Validity

### Mistral

Total prompts: 880

**Correlation Matrix:**

          L4.1      L4.2      L4.3      L4.4      L4.5      L4.6      L4.7
L4.1  1.000000  0.027298       NaN  0.186066  0.094491  0.057864  0.199722
L4.2  0.027298  1.000000       NaN  0.204621  0.510310  0.340278  0.252457
L4.3       NaN       NaN  1.000000  0.784439  0.753819  0.687500       NaN
L4.4  0.186066  0.204621  0.784439  1.000000  0.370980  0.240146  0.395099
L4.5  0.094491  0.510310  0.753819  0.370980  1.000000  0.425005  0.852803
L4.6  0.057864  0.340278  0.687500  0.240146  0.425005  1.000000  0.866025
L4.7  0.199722  0.252457       NaN  0.395099  0.852803  0.866025  1.000000

**Sample sizes for each pair:**

       L4.1   L4.2   L4.3   L4.4   L4.5   L4.6   L4.7
L4.1  598.0  598.0   72.0  335.0   57.0   57.0  310.0
L4.2  598.0  598.0   72.0  335.0   57.0   57.0  310.0
L4.3   72.0   72.0  193.0  118.0   18.0   18.0   37.0
L4.4  335.0  335.0  118.0  511.0   76.0   76.0  170.0
L4.5   57.0   57.0   18.0   76.0  168.0  168.0   15.0
L4.6   57.0   57.0   18.0   76.0  168.0  168.0   15.0
L4.7  310.0  310.0   37.0  170.0   15.0   15.0  310.0

### Llama-2

Total prompts: 880

**Correlation Matrix:**

          L4.1      L4.2      L4.3      L4.4      L4.5      L4.6      L4.7
L4.1  1.000000  0.553478 -0.020060  0.273719  0.156755  0.113680  0.473262
L4.2  0.553478  1.000000  0.028571  0.246151  0.234194  0.575086  0.382645
L4.3 -0.020060  0.028571  1.000000  0.662924       NaN       NaN       NaN
L4.4  0.273719  0.246151  0.662924  1.000000  0.457532  0.485259  0.530976
L4.5  0.156755  0.234194       NaN  0.457532  1.000000  0.464689  0.490990
L4.6  0.113680  0.575086       NaN  0.485259  0.464689  1.000000  0.747018
L4.7  0.473262  0.382645       NaN  0.530976  0.490990  0.747018  1.000000

**Sample sizes for each pair:**

       L4.1   L4.2   L4.3   L4.4   L4.5   L4.6   L4.7
L4.1  598.0  598.0   72.0  335.0   57.0   57.0  310.0
L4.2  598.0  598.0   72.0  335.0   57.0   57.0  310.0
L4.3   72.0   72.0  193.0  118.0   18.0   18.0   37.0
L4.4  335.0  335.0  118.0  511.0   76.0   76.0  170.0
L4.5   57.0   57.0   18.0   76.0  168.0  168.0   15.0
L4.6   57.0   57.0   18.0   76.0  168.0  168.0   15.0
L4.7  310.0  310.0   37.0  170.0   15.0   15.0  310.0

## 3. Internal Consistency (Cronbach's Alpha)

### Mistral

- Cronbach's α: Cannot calculate (insufficient data)
- Number of items: 7
- Sample size: 0

### Llama-2

- Cronbach's α: Cannot calculate (insufficient data)
- Number of items: 7
- Sample size: 0

## 4. Convergent Validity

Expected high correlations between related indicators:

### Mistral

- L4.1-L4.2: r = 0.027, p = 0.5052, n = 598 ✗
- L4.2-L4.7: r = 0.252, p = 0.0000, n = 310 ✓
- L4.3-L4.4: r = 0.784, p = 0.0000, n = 118 ✓
- L4.5-L4.6: r = 0.425, p = 0.0000, n = 168 ✓

### Llama-2

- L4.1-L4.2: r = 0.553, p = 0.0000, n = 598 ✓
- L4.2-L4.7: r = 0.383, p = 0.0000, n = 310 ✓
- L4.3-L4.4: r = 0.663, p = 0.0000, n = 118 ✓
- L4.5-L4.6: r = 0.465, p = 0.0000, n = 168 ✓

## 5. Discriminant Validity

Expected low correlations between unrelated indicators:

### Mistral

- L4.1-L4.6: r = 0.058, p = 0.6690, n = 57 ✓
- L4.2-L4.5: r = 0.510, p = 0.0001, n = 57 ✗
- L4.3-L4.7: No overlapping data or constant values

### Llama-2

- L4.1-L4.6: r = 0.114, p = 0.3998, n = 57 ✓
- L4.2-L4.5: r = 0.234, p = 0.0795, n = 57 ✓
- L4.3-L4.7: No overlapping data or constant values

## 6. Criterion Validity (Cross-Model Agreement)

Correlation between Mistral and Llama-2 scores on same prompts:

- **L4.1**: r = -0.002, p = 0.9518, n = 598, Low
- **L4.2**: r = 0.147, p = 0.0003, n = 598, Low
- **L4.3**: r = 0.411, p = 0.0000, n = 193, Low
- **L4.4**: r = 0.582, p = 0.0000, n = 511, Moderate
- **L4.5**: r = 0.305, p = 0.0001, n = 168, Low
- **L4.6**: r = 0.592, p = 0.0000, n = 168, Moderate
- **L4.7**: r = 0.466, p = 0.0000, n = 310, Low
