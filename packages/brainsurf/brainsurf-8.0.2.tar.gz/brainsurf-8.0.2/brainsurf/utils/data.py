import numpy as np

def estimate_sampling_frequency(timestamps):
    time_diff = np.diff(timestamps)  # Calculate the time difference between consecutive samples
    sampling_freq = 1 / np.nanmean(time_diff) 
    return sampling_freq

def remove_null_columns(df):
    # Remove columns with all null values
    df_cleaned = df.dropna(axis=1, how='all')
    return df_cleaned

def merge_data(adarsh_pre_cog, adarsh_post_cog):
    min_len = min(len(adarsh_pre_cog), len(adarsh_post_cog))
    pre_merged_df = adarsh_pre_cog[:min_len]
    post_merged_df = adarsh_post_cog[:min_len]
    print(min_len)
    return pre_merged_df,post_merged_df

import pandas as pd

def create_analysis_dataframe(post_results, pre_results):
    """
    Create a nicely formatted DataFrame from the post-Stroop test analysis and pre-Stroop test analysis results.

    Parameters:
        post_results (dict): Results of the post-Stroop test analysis.
        pre_results (dict): Results of the pre-Stroop test analysis.

    Returns:
        pd.DataFrame: Nicely formatted DataFrame containing the combined results.
    """
    data = {
        'Condition': ['Post-Stroop', 'Pre-Stroop'],
        'Average Response Time': [post_results['Average Response Time - Congruent'], pre_results['Average Response Time - Congruent']],
        'Average Accuracy': [post_results['Average Accuracy - Congruent'], pre_results['Average Accuracy - Congruent']],
        'T-Test - Response Time (t-value)': [post_results['T-Test - Response Time - t-value'], pre_results['T-Test - Response Time - t-value']],
        'T-Test - Response Time (p-value)': [post_results['T-Test - Response Time - p-value'], pre_results['T-Test - Response Time - p-value']],
        'T-Test - Accuracy (t-value)': [post_results['T-Test - Accuracy - t-value'], pre_results['T-Test - Accuracy - t-value']],
        'T-Test - Accuracy (p-value)': [post_results['T-Test - Accuracy - p-value'], pre_results['T-Test - Accuracy - p-value']]
    }

    df = pd.DataFrame(data)

    # Format numerical values
    df['Average Response Time'] = df['Average Response Time'].map('{:.2f}'.format)
    df['Average Accuracy'] = df['Average Accuracy'].map('{:.2f}'.format)
    df['T-Test - Response Time (t-value)'] = df['T-Test - Response Time (t-value)'].map('{:.2f}'.format)
    df['T-Test - Response Time (p-value)'] = df['T-Test - Response Time (p-value)'].map('{:.2f}'.format)
    df['T-Test - Accuracy (t-value)'] = df['T-Test - Accuracy (t-value)'].map('{:.2f}'.format)
    df['T-Test - Accuracy (p-value)'] = df['T-Test - Accuracy (p-value)'].map('{:.2f}'.format)

    # Align columns
    column_headers = [
        'Condition',
        'Average Response Time',
        'Average Accuracy',
        'T-Test - Response Time (t-value)',
        'T-Test - Response Time (p-value)',
        'T-Test - Accuracy (t-value)',
        'T-Test - Accuracy (p-value)'
    ]
    df = df.reindex(columns=column_headers)

    return df