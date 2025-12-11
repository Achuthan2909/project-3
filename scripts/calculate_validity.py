import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import sys

def load_evaluations(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_scores_matrix(eval_data):
    indicators = ['L4.1', 'L4.2', 'L4.3', 'L4.4', 'L4.5', 'L4.6', 'L4.7']
    data = {ind: [] for ind in indicators}
    prompt_ids = []
    
    for prompt_id, eval_info in eval_data['evaluations'].items():
        prompt_scores = {}
        
        for ind in indicators:
            if ind in eval_info['indicators']:
                score = eval_info['indicators'][ind].get('score')
                if score is not None:
                    prompt_scores[ind] = score
        
        if len(prompt_scores) > 0:
            prompt_ids.append(prompt_id)
            for ind in indicators:
                if ind in prompt_scores:
                    data[ind].append(prompt_scores[ind])
                else:
                    data[ind].append(np.nan)
    
    df = pd.DataFrame(data, index=prompt_ids)
    return df

def calculate_construct_validity(df):
    indicators = df.columns.tolist()
    n = len(indicators)
    
    correlation_matrix = np.zeros((n, n))
    p_value_matrix = np.zeros((n, n))
    n_pairs = np.zeros((n, n))
    
    for i, ind1 in enumerate(indicators):
        for j, ind2 in enumerate(indicators):
            if i == j:
                correlation_matrix[i, j] = 1.0
                p_value_matrix[i, j] = 0.0
                n_pairs[i, j] = len(df[ind1].dropna())
            else:
                valid_mask = ~(df[ind1].isna() | df[ind2].isna())
                if valid_mask.sum() > 2:
                    data1 = df.loc[valid_mask, ind1].values
                    data2 = df.loc[valid_mask, ind2].values
                    if np.std(data1) > 0 and np.std(data2) > 0:
                        r, p = pearsonr(data1, data2)
                        correlation_matrix[i, j] = r
                        p_value_matrix[i, j] = p
                    else:
                        correlation_matrix[i, j] = np.nan
                        p_value_matrix[i, j] = np.nan
                    n_pairs[i, j] = valid_mask.sum()
                else:
                    correlation_matrix[i, j] = np.nan
                    p_value_matrix[i, j] = np.nan
                    n_pairs[i, j] = 0
    
    corr_df = pd.DataFrame(correlation_matrix, index=indicators, columns=indicators)
    pval_df = pd.DataFrame(p_value_matrix, index=indicators, columns=indicators)
    n_df = pd.DataFrame(n_pairs, index=indicators, columns=indicators)
    
    return corr_df, pval_df, n_df

def calculate_internal_consistency(df):
    indicators = df.columns.tolist()
    
    df_clean = df[indicators].dropna()
    
    if len(df_clean) < 2:
        return np.nan
    
    cronbach_alpha = calculate_cronbach_alpha(df_clean.values)
    
    return cronbach_alpha

def calculate_cronbach_alpha(data):
    data = np.array(data)
    n_items = data.shape[1]
    item_variances = np.var(data, axis=0, ddof=1)
    total_variance = np.var(data.sum(axis=1), ddof=1)
    
    if total_variance == 0:
        return np.nan
    
    alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
    return alpha

def calculate_convergent_validity(df):
    indicators = df.columns.tolist()
    
    convergent_pairs = [
        ('L4.1', 'L4.2'),
        ('L4.2', 'L4.7'),
        ('L4.3', 'L4.4'),
        ('L4.5', 'L4.6'),
    ]
    
    results = {}
    for ind1, ind2 in convergent_pairs:
        if ind1 in df.columns and ind2 in df.columns:
            valid_mask = ~(df[ind1].isna() | df[ind2].isna())
            if valid_mask.sum() > 2:
                data1 = df.loc[valid_mask, ind1].values
                data2 = df.loc[valid_mask, ind2].values
                if np.std(data1) > 0 and np.std(data2) > 0:
                    r, p = pearsonr(data1, data2)
                    results[f"{ind1}-{ind2}"] = {
                        'correlation': float(r),
                        'p_value': float(p),
                        'significant': bool(p < 0.05),
                        'n': int(valid_mask.sum())
                    }
                else:
                    results[f"{ind1}-{ind2}"] = {
                        'correlation': None,
                        'p_value': None,
                        'significant': False,
                        'n': int(valid_mask.sum())
                    }
            else:
                results[f"{ind1}-{ind2}"] = {
                    'correlation': np.nan,
                    'p_value': np.nan,
                    'significant': False,
                    'n': 0
                }
    
    return results

def calculate_discriminant_validity(df):
    indicators = df.columns.tolist()
    
    discriminant_pairs = [
        ('L4.1', 'L4.6'),
        ('L4.2', 'L4.5'),
        ('L4.3', 'L4.7'),
    ]
    
    results = {}
    for ind1, ind2 in discriminant_pairs:
        if ind1 in df.columns and ind2 in df.columns:
            valid_mask = ~(df[ind1].isna() | df[ind2].isna())
            if valid_mask.sum() > 2:
                data1 = df.loc[valid_mask, ind1].values
                data2 = df.loc[valid_mask, ind2].values
                if np.std(data1) > 0 and np.std(data2) > 0:
                    r, p = pearsonr(data1, data2)
                    results[f"{ind1}-{ind2}"] = {
                        'correlation': float(r),
                        'p_value': float(p),
                        'significant': bool(p < 0.05),
                        'low_correlation': bool(abs(r) < 0.3),
                        'n': int(valid_mask.sum())
                    }
                else:
                    results[f"{ind1}-{ind2}"] = {
                        'correlation': None,
                        'p_value': None,
                        'significant': False,
                        'low_correlation': False,
                        'n': int(valid_mask.sum())
                    }
            else:
                results[f"{ind1}-{ind2}"] = {
                    'correlation': np.nan,
                    'p_value': np.nan,
                    'significant': False,
                    'low_correlation': False,
                    'n': 0
                }
    
    return results

def calculate_content_validity_summary():
    return {
        'expert_defined_rubrics': True,
        'theoretical_foundation': [
            'Rogers & Farson (1957) - Active Listening',
            'Plutchik\'s Psycho-evolutionary Theory of Emotion',
            'Ekman\'s Universal Emotions',
            'Linehan\'s Biosocial Theory (DBT)',
            'Roberts\' Seven-Stage Crisis Intervention Model',
            'Fredrickson\'s Broaden-and-Build Theory',
            'Self-Determination Theory (Ryan & Deci)'
        ],
        'rubric_development': 'Expert-defined with theoretical grounding',
        'scenario_coverage': [
            'Job Loss/Unemployment',
            'Health Concerns/Medical Anxiety',
            'Relationship Issues/Breakup',
            'Grief/Loss',
            'Financial Stress',
            'Academic/Work Pressure',
            'Social Isolation/Loneliness'
        ],
        'emotion_coverage': [
            'Anger', 'Anxiety', 'Fear', 'Sadness', 'Joy',
            'Surprise', 'Trust', 'Shame', 'Hope', 'Anticipation',
            'Love', 'Disgust', 'Jealousy'
        ],
        'intensity_levels': ['Mild', 'Moderate', 'Severe']
    }

def calculate_criterion_validity(df_mistral, df_llama):
    common_prompts = list(set(df_mistral.index) & set(df_llama.index))
    
    if len(common_prompts) < 10:
        return None
    
    df_mistral_common = df_mistral.loc[common_prompts]
    df_llama_common = df_llama.loc[common_prompts]
    
    criterion_validity = {}
    
    for ind in df_mistral_common.columns:
        if ind in df_llama_common.columns:
            valid_mask = ~(df_mistral_common[ind].isna() | df_llama_common[ind].isna())
            if valid_mask.sum() > 2:
                data1 = df_mistral_common.loc[valid_mask, ind].values
                data2 = df_llama_common.loc[valid_mask, ind].values
                if np.std(data1) > 0 and np.std(data2) > 0:
                    r, p = pearsonr(data1, data2)
                    criterion_validity[ind] = {
                        'correlation': float(r),
                        'p_value': float(p),
                        'n': int(valid_mask.sum()),
                        'interpretation': 'High' if r > 0.7 else 'Moderate' if r > 0.5 else 'Low'
                    }
                else:
                    criterion_validity[ind] = {
                        'correlation': None,
                        'p_value': None,
                        'n': int(valid_mask.sum()),
                        'interpretation': 'Cannot calculate'
                    }
    
    return criterion_validity

def main():
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data" / "model_outputs"
    
    mistral_file = data_dir / "all_indicators_evaluations_mistral-7b-instruct.json"
    llama_file = data_dir / "all_indicators_evaluations_llama-2-7b-chat.json"
    
    print("Loading evaluation data...")
    mistral_data = load_evaluations(mistral_file)
    llama_data = load_evaluations(llama_file)
    
    print("Extracting scores matrices...")
    df_mistral = extract_scores_matrix(mistral_data)
    df_llama = extract_scores_matrix(llama_data)
    
    print(f"Mistral: {len(df_mistral)} prompts with all indicators")
    print(f"Llama-2: {len(df_llama)} prompts with all indicators")
    
    results = {
        'construct_validity': {},
        'internal_consistency': {},
        'convergent_validity': {},
        'discriminant_validity': {},
        'content_validity': {},
        'criterion_validity': {}
    }
    
    print("\nCalculating construct validity (correlations)...")
    for model_name, df in [('Mistral', df_mistral), ('Llama-2', df_llama)]:
        if len(df) > 0:
            corr_df, pval_df, n_df = calculate_construct_validity(df)
            results['construct_validity'][model_name] = {
                'correlation_matrix': corr_df.to_dict(),
                'p_value_matrix': pval_df.to_dict(),
                'n_matrix': n_df.to_dict(),
                'n_prompts': len(df)
            }
            
            alpha = calculate_internal_consistency(df)
            n_valid = len(df.dropna())
            results['internal_consistency'][model_name] = {
                'cronbach_alpha': float(alpha) if not np.isnan(alpha) else None,
                'n': n_valid,
                'n_items': len(df.columns),
                'n_prompts': len(df)
            }
            
            convergent = calculate_convergent_validity(df)
            results['convergent_validity'][model_name] = convergent
            
            discriminant = calculate_discriminant_validity(df)
            results['discriminant_validity'][model_name] = discriminant
    
    print("Calculating content validity...")
    results['content_validity'] = calculate_content_validity_summary()
    
    print("Calculating criterion validity (cross-model agreement)...")
    criterion = calculate_criterion_validity(df_mistral, df_llama)
    if criterion:
        results['criterion_validity'] = criterion
    
    output_dir = base_dir / "documentation"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "validity_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nValidity analysis saved to: {output_file}")
    
    report_file = output_dir / "validity_analysis_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Validity Analysis Report\n\n")
        
        f.write("## 1. Content Validity\n\n")
        f.write("### Expert-Defined Rubrics\n")
        f.write("All rubrics were developed by experts with strong theoretical foundations:\n\n")
        for theory in results['content_validity']['theoretical_foundation']:
            f.write(f"- {theory}\n")
        
        f.write("\n### Scenario Coverage\n")
        for scenario in results['content_validity']['scenario_coverage']:
            f.write(f"- {scenario}\n")
        
        f.write("\n## 2. Construct Validity\n\n")
        for model_name in results['construct_validity'].keys():
            f.write(f"### {model_name}\n\n")
            f.write(f"Total prompts: {results['construct_validity'][model_name]['n_prompts']}\n\n")
            f.write("**Correlation Matrix:**\n\n")
            corr_df = pd.DataFrame(results['construct_validity'][model_name]['correlation_matrix'])
            f.write(corr_df.to_string())
            f.write("\n\n")
            f.write("**Sample sizes for each pair:**\n\n")
            n_df = pd.DataFrame(results['construct_validity'][model_name]['n_matrix'])
            f.write(n_df.to_string())
            f.write("\n\n")
        
        f.write("## 3. Internal Consistency (Cronbach's Alpha)\n\n")
        for model_name, stats in results['internal_consistency'].items():
            f.write(f"### {model_name}\n\n")
            if stats['cronbach_alpha'] is not None:
                f.write(f"- Cronbach's α: {stats['cronbach_alpha']:.3f}\n")
            else:
                f.write(f"- Cronbach's α: Cannot calculate (insufficient data)\n")
            f.write(f"- Number of items: {stats['n_items']}\n")
            f.write(f"- Sample size: {stats['n']}\n\n")
            if stats['cronbach_alpha'] is not None:
                interpretation = "Excellent" if stats['cronbach_alpha'] > 0.9 else \
                               "Good" if stats['cronbach_alpha'] > 0.8 else \
                               "Acceptable" if stats['cronbach_alpha'] > 0.7 else \
                               "Questionable" if stats['cronbach_alpha'] > 0.6 else "Poor"
                f.write(f"**Interpretation:** {interpretation} (α > 0.7 is generally considered acceptable)\n\n")
        
        f.write("## 4. Convergent Validity\n\n")
        f.write("Expected high correlations between related indicators:\n\n")
        for model_name, convergent in results['convergent_validity'].items():
            f.write(f"### {model_name}\n\n")
            for pair, stats in convergent.items():
                if stats['n'] > 0 and stats['correlation'] is not None:
                    sig = "✓" if stats['significant'] else "✗"
                    f.write(f"- {pair}: r = {stats['correlation']:.3f}, p = {stats['p_value']:.4f}, n = {stats['n']} {sig}\n")
                else:
                    f.write(f"- {pair}: No overlapping data or constant values\n")
            f.write("\n")
        
        f.write("## 5. Discriminant Validity\n\n")
        f.write("Expected low correlations between unrelated indicators:\n\n")
        for model_name, discriminant in results['discriminant_validity'].items():
            f.write(f"### {model_name}\n\n")
            for pair, stats in discriminant.items():
                if stats['n'] > 0 and stats['correlation'] is not None:
                    sig = "✓" if stats['low_correlation'] else "✗"
                    f.write(f"- {pair}: r = {stats['correlation']:.3f}, p = {stats['p_value']:.4f}, n = {stats['n']} {sig}\n")
                else:
                    f.write(f"- {pair}: No overlapping data or constant values\n")
            f.write("\n")
        
        if results.get('criterion_validity'):
            f.write("## 6. Criterion Validity (Cross-Model Agreement)\n\n")
            f.write("Correlation between Mistral and Llama-2 scores on same prompts:\n\n")
            for ind, stats in results['criterion_validity'].items():
                if stats['correlation'] is not None:
                    f.write(f"- **{ind}**: r = {stats['correlation']:.3f}, p = {stats['p_value']:.4f}, "
                            f"n = {stats['n']}, {stats['interpretation']}\n")
                else:
                    f.write(f"- **{ind}**: Cannot calculate, n = {stats['n']}\n")
    
    print(f"Validity report saved to: {report_file}")
    
    print("\n=== Summary ===")
    for model_name in results['internal_consistency'].keys():
        alpha = results['internal_consistency'][model_name]['cronbach_alpha']
        if alpha is not None:
            print(f"{model_name} Cronbach's α: {alpha:.3f}")
        else:
            print(f"{model_name} Cronbach's α: Cannot calculate")
    
    if results.get('criterion_validity'):
        print("\nCross-model correlations:")
        for ind, stats in results['criterion_validity'].items():
            if stats['correlation'] is not None:
                print(f"  {ind}: r = {stats['correlation']:.3f} ({stats['interpretation']})")
            else:
                print(f"  {ind}: Cannot calculate")

if __name__ == '__main__':
    main()

