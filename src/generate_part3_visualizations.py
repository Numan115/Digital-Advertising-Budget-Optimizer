"""
generate_part3_visualizations.py
Creates visualizations for Part 3: Budget Recommendation Engine.
Saved in: visualizations/
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_part3_visualizations(input_path='reports/budget_allocation_recommendations.csv',
                                output_dir='visualizations'):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_path)
    sns.set_theme(style='whitegrid')
    
    # 1. Budget Allocation Donut Chart
    plt.figure(figsize=(8, 8))
    alloc_df = df[df['allocated_budget'] > 0]
    colors = ['#2b5c8f', '#4ca585', '#d4a373', '#e76f51']
    plt.pie(alloc_df['allocated_budget'], labels=alloc_df['platform'], autopct='%1.1f%%',
            startangle=140, colors=colors, explode=[0.04, 0.04, 0.04, 0.04],
            wedgeprops=dict(width=0.6))
    plt.title('Recommended Rs. 1,000,000 Budget Distribution', fontsize=15, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '14_budget_allocation_donut.png'), dpi=300)
    plt.close()

    # 2. Projected Incremental Revenue and Net Profit
    plt.figure(figsize=(10, 6))
    plot_df = alloc_df.melt(id_vars='platform', value_vars=['allocated_budget', 'proj_revenue', 'proj_net_profit'],
                            var_name='Metric', value_name='Amount')
    plot_df['Metric'] = plot_df['Metric'].replace({
        'allocated_budget': 'Allocated Budget (PKR)',
        'proj_revenue': 'Projected Gross Revenue (PKR)',
        'proj_net_profit': 'Projected Net Profit (PKR)'
    })
    ax = sns.barplot(data=plot_df, x='platform', y='Amount', hue='Metric', palette=['#3a86ff', '#2a9d8f', '#38b000'])
    plt.title('Projected Financial Impact by Platform (PKR)', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Amount (PKR)', fontsize=12)
    plt.xlabel('Advertising Platform', fontsize=12)
    plt.legend(title='')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '15_projected_financial_impact.png'), dpi=300)
    plt.close()

    # 3. Before vs. After ROAS Comparison
    plt.figure(figsize=(9, 5))
    metrics = ['Historical Baseline (Project 1 & Part 1)', 'Optimized Rs. 1M Portfolio (Part 3)']
    roas_vals = [5.24, 5.40]
    palette = ['#457b9d', '#2a9d8f']
    ax = sns.barplot(x=metrics, y=roas_vals, palette=palette)
    plt.title('Overall Return on Ad Spend: Baseline vs. Optimized Budget', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Portfolio ROAS (x)', fontsize=12)
    plt.ylim(0, 7)
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}x",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=12, fontweight='bold', xytext=(0, 4),
                    textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '16_before_vs_after_roas.png'), dpi=300)
    plt.close()

    print("Part 3 Visualizations successfully saved in visualizations/:")
    print(" - 14_budget_allocation_donut.png")
    print(" - 15_projected_financial_impact.png")
    print(" - 16_before_vs_after_roas.png")

if __name__ == '__main__':
    create_part3_visualizations()
