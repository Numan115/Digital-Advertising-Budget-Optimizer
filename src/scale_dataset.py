"""
scale_dataset.py
High-performance dataset scaling engine for Big Data Analytics benchmarking.
Generates scaled advertising datasets:
- 100K records (~8 MB)
- 1M records (~80 MB)
- 10M records (~800 MB)
"""

import os
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_scaled_data(num_records, output_path, chunk_size=500000, random_seed=42):
    print(f"\n[Scaling Engine] Generating {num_records:,} records to: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    np.random.seed(random_seed)
    
    platforms = ['Facebook', 'Instagram', 'Google', 'TikTok', 'YouTube']
    platform_probs = [0.25, 0.25, 0.20, 0.18, 0.12]
    
    campaigns = [
        'Brand Awareness Boost', 'Lead Generation Wave', 'Summer Sale Mega Promo',
        'Flash Discount 50%', 'App Install Push', 'Festive Eid Special',
        'Back to School Promo', 'New Product Launch'
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
    
    platform_profiles = {
        'Google': {'imp': (2000, 25000), 'ctr': (0.025, 0.055), 'cpc': (25, 60), 'cr': (0.035, 0.080), 'aov': (2800, 6000)},
        'Instagram': {'imp': (3000, 35000), 'ctr': (0.020, 0.045), 'cpc': (16, 38), 'cr': (0.025, 0.060), 'aov': (2200, 5000)},
        'Facebook': {'imp': (4000, 40000), 'ctr': (0.015, 0.038), 'cpc': (14, 32), 'cr': (0.020, 0.050), 'aov': (1800, 4200)},
        'TikTok': {'imp': (5000, 50000), 'ctr': (0.025, 0.060), 'cpc': (8, 22), 'cr': (0.015, 0.035), 'aov': (1500, 3500)},
        'YouTube': {'imp': (3000, 30000), 'ctr': (0.012, 0.030), 'cpc': (12, 28), 'cr': (0.012, 0.032), 'aov': (1600, 3800)}
    }
    
    start_date = datetime(2023, 1, 1)
    total_days = 730
    
    written = 0
    first_chunk = True
    
    start_time = datetime.now()
    
    while written < num_records:
        current_chunk_size = min(chunk_size, num_records - written)
        
        # Vectorized platform selection
        sel_platforms = np.random.choice(platforms, size=current_chunk_size, p=platform_probs)
        sel_campaigns = np.random.choice(campaigns, size=current_chunk_size)
        sel_cities = np.random.choice(cities, size=current_chunk_size, p=city_weights)
        sel_ages = np.random.choice(age_groups, size=current_chunk_size, p=age_weights)
        sel_genders = np.random.choice(genders, size=current_chunk_size, p=gender_weights)
        sel_devices = np.random.choice(devices, size=current_chunk_size, p=device_weights)
        
        random_days = np.random.randint(0, total_days, size=current_chunk_size)
        dates = [(start_date + timedelta(days=int(d))).strftime('%Y-%m-%d') for d in random_days]
        
        # Arrays for numeric columns
        impressions = np.zeros(current_chunk_size, dtype=int)
        clicks = np.zeros(current_chunk_size, dtype=int)
        spends = np.zeros(current_chunk_size, dtype=float)
        conversions = np.zeros(current_chunk_size, dtype=int)
        revenues = np.zeros(current_chunk_size, dtype=float)
        
        for p, prof in platform_profiles.items():
            mask = (sel_platforms == p)
            count = np.sum(mask)
            if count == 0:
                continue
            
            imp = np.random.randint(prof['imp'][0], prof['imp'][1], size=count)
            ctr = np.random.uniform(prof['ctr'][0], prof['ctr'][1], size=count)
            c = np.maximum(1, (imp * ctr).astype(int))
            cpc = np.random.uniform(prof['cpc'][0], prof['cpc'][1], size=count)
            sp = np.round(c * cpc, 2)
            
            cr = np.random.uniform(prof['cr'][0], prof['cr'][1], size=count)
            conv = np.random.binomial(c, cr)
            
            aov = np.random.uniform(prof['aov'][0], prof['aov'][1], size=count)
            rev = np.where(conv > 0, np.round(conv * aov * np.random.uniform(0.9, 1.15, size=count), 2), 0.0)
            
            impressions[mask] = imp
            clicks[mask] = c
            spends[mask] = sp
            conversions[mask] = conv
            revenues[mask] = rev
            
        chunk_df = pd.DataFrame({
            'date': dates,
            'campaign': sel_campaigns,
            'platform': sel_platforms,
            'impressions': impressions,
            'clicks': clicks,
            'spend': spends,
            'conversions': conversions,
            'revenue': revenues,
            'age': sel_ages,
            'gender': sel_genders,
            'city': sel_cities,
            'device': sel_devices
        })
        
        chunk_df.to_csv(output_path, mode='w' if first_chunk else 'a', index=False, header=first_chunk)
        first_chunk = False
        written += current_chunk_size
        print(f"  -> Generated {written:,} / {num_records:,} records...")

    elapsed = (datetime.now() - start_time).total_seconds()
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[Done] Created {output_path} ({file_size_mb:.2f} MB) in {elapsed:.2f} seconds.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scale Advertising Dataset")
    parser.add_argument('--sizes', nargs='+', default=['100k', '1m'], help="Sizes to generate: e.g. 100k 1m 10m")
    args = parser.parse_args()
    
    size_map = {
        '100k': (100000, 'data/scaled/advertising_100k.csv'),
        '1m': (1000000, 'data/scaled/advertising_1m.csv'),
        '10m': (10000000, 'data/scaled/advertising_10m.csv')
    }
    
    for s in args.sizes:
        s_lower = s.lower()
        if s_lower in size_map:
            n, path = size_map[s_lower]
            generate_scaled_data(n, path)
        else:
            print(f"Unknown size: {s}")
