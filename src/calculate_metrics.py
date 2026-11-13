"""
calculate_metrics.py
Calculates marketing KPIs: CTR, CPC, CPA, Conversion Rate, and ROAS.
Saves the enriched dataset to data/processed/advertising_data_with_kpis.csv.
"""

import os
import pandas as pd
import numpy as np

def calculate_marketing_kpis(input_path='data/processed/advertising_data_cleaned.csv',
                             output_path='data/processed/advertising_data_with_kpis.csv'):
    print(f"Loading cleaned data from: {input_path}")
    df = pd.read_csv(input_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # 1. Marketing KPIs
    # CTR (Click-Through Rate): % of impressions that resulted in a click
    df['ctr'] = np.where(df['impressions'] > 0, (df['clicks'] / df['impressions']) * 100, 0.0)
    
    # CPC (Cost Per Click): Average cost paid per ad click in PKR
    df['cpc'] = np.where(df['clicks'] > 0, df['spend'] / df['clicks'], 0.0)
    
    # Conversion Rate (%): % of clicks that converted
    df['conversion_rate'] = np.where(df['clicks'] > 0, (df['conversions'] / df['clicks']) * 100, 0.0)
    
    # CPA (Cost Per Acquisition): Cost paid per successful conversion in PKR
    df['cpa'] = np.where(df['conversions'] > 0, df['spend'] / df['conversions'], np.nan)
    
    # ROAS (Return On Ad Spend): Revenue generated per rupee spent
    df['roas'] = np.where(df['spend'] > 0, df['revenue'] / df['spend'], 0.0)
    
    # Profit (PKR)
    df['profit'] = df['revenue'] - df['spend']
    
    # 2. Date and Time Features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Round KPI columns for readability
    df['ctr'] = df['ctr'].round(2)
    df['cpc'] = df['cpc'].round(2)
    df['conversion_rate'] = df['conversion_rate'].round(2)
    df['cpa'] = df['cpa'].round(2)
    df['roas'] = df['roas'].round(2)
    df['profit'] = df['profit'].round(2)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset with KPIs saved to: {output_path}")
    
    print("\nPlatform-wise Performance Summary:")
    summary = df.groupby('platform').agg(
        total_spend=('spend', 'sum'),
        total_revenue=('revenue', 'sum'),
        total_clicks=('clicks', 'sum'),
        total_conversions=('conversions', 'sum'),
        avg_ctr=('ctr', 'mean'),
        avg_cpc=('cpc', 'mean'),
        avg_conv_rate=('conversion_rate', 'mean'),
        avg_roas=('roas', 'mean')
    ).reset_index()
    
    summary['overall_roas'] = (summary['total_revenue'] / summary['total_spend']).round(2)
    summary['overall_cpa'] = (summary['total_spend'] / summary['total_conversions']).round(2)
    print(summary.to_string(index=False))
    
    return df

if __name__ == '__main__':
    calculate_marketing_kpis()
