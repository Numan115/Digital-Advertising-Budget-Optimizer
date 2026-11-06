"""
generate_data.py
Simulates 10,000 realistic digital advertising records for Project 2:
Digital Advertising Budget Optimizer.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_advertising_dataset(num_records=10000, random_seed=42):
    np.random.seed(random_seed)
    
    platforms = ['Facebook', 'Instagram', 'Google', 'TikTok', 'YouTube']
    platform_probs = [0.25, 0.25, 0.20, 0.18, 0.12]
    
    campaigns = [
        'Brand Awareness Boost',
        'Lead Generation Wave',
        'Summer Sale Mega Promo',
        'Flash Discount 50%',
        'App Install Push',
        'Festive Eid Special',
        'Back to School Promo',
        'New Product Launch'
    ]
    
    cities = ['Karachi', 'Lahore', 'Islamabad', 'Rawalpindi', 'Faisalabad', 
              'Multan', 'Peshawar', 'Quetta', 'Sialkot', 'Gujranwala']
    city_weights = [0.30, 0.25, 0.15, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.02]
    
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    age_weights = [0.35, 0.35, 0.18, 0.08, 0.04]
    
    genders = ['Male', 'Female', 'Other']
    gender_weights = [0.52, 0.46, 0.02]
    
    devices = ['Mobile', 'Desktop', 'Tablet']
    device_weights = [0.75, 0.20, 0.05]
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days
    
    # Generate random dates
    random_days = np.random.randint(0, total_days, size=num_records)
    dates = [start_date + timedelta(days=int(d)) for d in random_days]
    
    selected_platforms = np.random.choice(platforms, size=num_records, p=platform_probs)
    selected_campaigns = np.random.choice(campaigns, size=num_records)
    selected_cities = np.random.choice(cities, size=num_records, p=city_weights)
    selected_ages = np.random.choice(age_groups, size=num_records, p=age_weights)
    selected_genders = np.random.choice(genders, size=num_records, p=gender_weights)
    selected_devices = np.random.choice(devices, size=num_records, p=device_weights)
    
    # Platform-specific profiles for realistic performance
    # Impressions, base CTR, base CPC (PKR), base Conversion Rate, base Order Value (PKR)
    platform_profiles = {
        'Google': {
            'imp_range': (2000, 25000), 'ctr': (0.025, 0.055), 'cpc': (25, 60), 
            'conv_rate': (0.035, 0.080), 'aov': (2800, 6000)
        },
        'Instagram': {
            'imp_range': (3000, 35000), 'ctr': (0.020, 0.045), 'cpc': (16, 38), 
            'conv_rate': (0.025, 0.060), 'aov': (2200, 5000)
        },
        'Facebook': {
            'imp_range': (4000, 40000), 'ctr': (0.015, 0.038), 'cpc': (14, 32), 
            'conv_rate': (0.020, 0.050), 'aov': (1800, 4200)
        },
        'TikTok': {
            'imp_range': (5000, 50000), 'ctr': (0.025, 0.060), 'cpc': (8, 22), 
            'conv_rate': (0.015, 0.035), 'aov': (1500, 3500)
        },
        'YouTube': {
            'imp_range': (3000, 30000), 'ctr': (0.012, 0.030), 'cpc': (12, 28), 
            'conv_rate': (0.012, 0.032), 'aov': (1600, 3800)
        }
    }
    
    impressions = np.zeros(num_records, dtype=int)
    clicks = np.zeros(num_records, dtype=int)
    spends = np.zeros(num_records, dtype=float)
    conversions = np.zeros(num_records, dtype=int)
    revenues = np.zeros(num_records, dtype=float)
    
    for i in range(num_records):
        p = selected_platforms[i]
        prof = platform_profiles[p]
        
        # Impressions
        imp = np.random.randint(prof['imp_range'][0], prof['imp_range'][1])
        impressions[i] = imp
        
        # Clicks based on CTR
        ctr = np.random.uniform(prof['ctr'][0], prof['ctr'][1])
        c = max(1, int(imp * ctr))
        clicks[i] = c
        
        # Spend based on CPC
        cpc = np.random.uniform(prof['cpc'][0], prof['cpc'][1])
        spend = round(c * cpc, 2)
        spends[i] = spend
        
        # Conversions based on conversion rate
        cr = np.random.uniform(prof['conv_rate'][0], prof['conv_rate'][1])
        conv = int(np.random.binomial(c, cr))
        conversions[i] = conv
        
        # Revenue based on conversions & Average Order Value (AOV)
        if conv > 0:
            aov = np.random.uniform(prof['aov'][0], prof['aov'][1])
            # slight variation per order
            rev = round(conv * aov * np.random.uniform(0.9, 1.15), 2)
        else:
            rev = 0.0
        revenues[i] = rev

    df = pd.DataFrame({
        'date': [d.strftime('%Y-%m-%d') for d in dates],
        'campaign': selected_campaigns,
        'platform': selected_platforms,
        'impressions': impressions,
        'clicks': clicks,
        'spend': spends,
        'conversions': conversions,
        'revenue': revenues,
        'age': selected_ages,
        'gender': selected_genders,
        'city': selected_cities,
        'device': selected_devices
    })
    
    # Introduce small realistic data cleaning challenges for Milestone 3 (~0.5% missing, slight duplicates)
    # 25 duplicate rows
    duplicate_rows = df.sample(n=25, random_state=42)
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    
    # Shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    # Save to data/raw/advertising_data_raw.csv
    out_dir = os.path.join('data', 'raw')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'advertising_data_raw.csv')
    df.to_csv(out_path, index=False)
    
    print(f"Successfully generated {len(df)} advertising records.")
    print(f"Saved dataset to: {out_path}")
    print("\nDataset Summary Preview:")
    print(df.head(5))
    print("\nPlatform Distribution:")
    print(df['platform'].value_counts())
    print("\nSummary Statistics:")
    print(df[['impressions', 'clicks', 'spend', 'conversions', 'revenue']].describe())

if __name__ == '__main__':
    generate_advertising_dataset()
