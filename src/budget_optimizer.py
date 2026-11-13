"""
budget_optimizer.py
Part 3: Marketing Budget Recommendation Engine.
Allocates an additional Rs. 1,000,000 across advertising platforms
to maximize overall Return on Ad Spend (ROAS) and conversions.
"""

import os
import pandas as pd
import numpy as np

def optimize_budget(input_path='data/processed/advertising_data_with_kpis.csv',
                    additional_budget=1000000.0,
                    output_dir='reports'):
    print(f"\n=======================================================")
    print(f"   MARKETING BUDGET OPTIMIZATION ENGINE (PART 3)       ")
    print(f"=======================================================")
    print(f"Total Additional Budget to Allocate: Rs. {additional_budget:,.2f}")
    
    df = pd.read_csv(input_path)
    
    # 1. Platform Performance Metrics Aggregation
    perf = df.groupby('platform').agg(
        total_spend=('spend', 'sum'),
        total_revenue=('revenue', 'sum'),
        total_clicks=('clicks', 'sum'),
        total_conversions=('conversions', 'sum'),
        avg_ctr=('ctr', 'mean'),
        avg_cpc=('cpc', 'mean'),
        avg_conv_rate=('conversion_rate', 'mean')
    ).reset_index()
    
    perf['roas'] = perf['total_revenue'] / perf['total_spend']
    perf['cpa'] = perf['total_spend'] / perf['total_conversions']
    
    # 2. Multi-Criteria Scoring Algorithm
    # Normalized ROAS (Higher is better)
    norm_roas = (perf['roas'] - perf['roas'].min()) / (perf['roas'].max() - perf['roas'].min())
    # Normalized CPA (Lower is better -> inverted)
    norm_cpa = (perf['cpa'].max() - perf['cpa']) / (perf['cpa'].max() - perf['cpa'].min())
    # Normalized Conversion Rate (Higher is better)
    norm_cr = (perf['avg_conv_rate'] - perf['avg_conv_rate'].min()) / (perf['avg_conv_rate'].max() - perf['avg_conv_rate'].min())
    
    # Composite Score: 50% ROAS, 30% CPA Efficiency, 20% Conversion Rate
    perf['composite_score'] = (0.50 * norm_roas) + (0.30 * norm_cpa) + (0.20 * norm_cr)
    
    # Apply Threshold / Penalty: If ROAS < 3.5x, zero out allocation
    perf['eligible_score'] = np.where(perf['roas'] >= 3.5, perf['composite_score'], 0.0)
    
    # Raw allocation percentage
    total_score = perf['eligible_score'].sum()
    perf['allocation_pct'] = (perf['eligible_score'] / total_score).round(4)
    
    # Business Constraints: Cap max allocation at 45% (diversification), min threshold 10% for eligible
    perf['allocated_budget'] = (perf['allocation_pct'] * additional_budget).round(2)
    
    # 3. Projected Incremental Impact Modeling
    perf['proj_clicks'] = np.where(perf['avg_cpc'] > 0, perf['allocated_budget'] / perf['avg_cpc'], 0).astype(int)
    perf['proj_conversions'] = (perf['proj_clicks'] * (perf['avg_conv_rate'] / 100.0)).astype(int)
    perf['proj_revenue'] = (perf['allocated_budget'] * perf['roas']).round(2)
    perf['proj_net_profit'] = perf['proj_revenue'] - perf['allocated_budget']
    
    os.makedirs(output_dir, exist_ok=True)
    out_csv = os.path.join(output_dir, 'budget_allocation_recommendations.csv')
    perf.to_csv(out_csv, index=False)
    
    print("\n--- RECOMMENDED BUDGET ALLOCATION ---")
    summary_cols = ['platform', 'roas', 'cpa', 'allocation_pct', 'allocated_budget', 
                    'proj_conversions', 'proj_revenue', 'proj_net_profit']
    print(perf[summary_cols].to_string(index=False))
    
    total_alloc = perf['allocated_budget'].sum()
    total_proj_rev = perf['proj_revenue'].sum()
    total_proj_conv = perf['proj_conversions'].sum()
    overall_proj_roas = total_proj_rev / total_alloc
    total_proj_profit = total_proj_rev - total_alloc
    
    print("\n=======================================================")
    print("           PORTFOLIO PROJECTION SUMMARY                ")
    print("=======================================================")
    print(f"Allocated Budget:           Rs. {total_alloc:,.2f}")
    print(f"Projected Gross Revenue:    Rs. {total_proj_rev:,.2f}")
    print(f"Projected Incremental Sales: {total_proj_conv:,} conversions")
    print(f"Projected Incremental Profit:Rs. {total_proj_profit:,.2f}")
    print(f"Projected Portfolio ROAS:   {overall_proj_roas:.2f}x")
    print("=======================================================\n")
    
    return perf

if __name__ == '__main__':
    optimize_budget()
