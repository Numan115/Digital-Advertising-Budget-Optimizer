
import os
import numpy as np
import pandas as pd

def generate_advertising_dataset(
    num_records=10_000_000,
    chunk_size=500_000,
    random_seed=42
):
    rng = np.random.default_rng(random_seed)

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

    cities = [
        'Karachi', 'Lahore', 'Islamabad', 'Rawalpindi',
        'Faisalabad', 'Multan', 'Peshawar', 'Quetta',
        'Sialkot', 'Gujranwala'
    ]

    city_weights = [0.30, 0.25, 0.15, 0.08, 0.06,
                    0.05, 0.04, 0.03, 0.02, 0.02]

    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    age_weights = [0.35, 0.35, 0.18, 0.08, 0.04]

    genders = ['Male', 'Female', 'Other']
    gender_weights = [0.52, 0.46, 0.02]

    devices = ['Mobile', 'Desktop', 'Tablet']
    device_weights = [0.75, 0.20, 0.05]

    profiles = {
        'Google': {
            'imp': (2000, 25000), 'ctr': (0.025, 0.055),
            'cpc': (25, 60), 'cr': (0.035, 0.080),
            'aov': (2800, 6000)
        },
        'Instagram': {
            'imp': (3000, 35000), 'ctr': (0.020, 0.045),
            'cpc': (16, 38), 'cr': (0.025, 0.060),
            'aov': (2200, 5000)
        },
        'Facebook': {
            'imp': (4000, 40000), 'ctr': (0.015, 0.038),
            'cpc': (14, 32), 'cr': (0.020, 0.050),
            'aov': (1800, 4200)
        },
        'TikTok': {
            'imp': (5000, 50000), 'ctr': (0.025, 0.060),
            'cpc': (8, 22), 'cr': (0.015, 0.035),
            'aov': (1500, 3500)
        },
        'YouTube': {
            'imp': (3000, 30000), 'ctr': (0.012, 0.030),
            'cpc': (12, 28), 'cr': (0.012, 0.032),
            'aov': (1600, 3800)
        }
    }

    out_dir = os.path.join('data', 'raw')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'advertising_data_raw.csv')

    if os.path.exists(out_path):
        os.remove(out_path)

    records_written = 0

    while records_written < num_records:
        n = min(chunk_size, num_records - records_written)

        selected_platforms = rng.choice(
            platforms, size=n, p=platform_probs
        )

        impressions = np.zeros(n, dtype=int)
        clicks = np.zeros(n, dtype=int)
        spend = np.zeros(n)
        conversions = np.zeros(n, dtype=int)
        revenue = np.zeros(n)

        for platform in platforms:
            mask = selected_platforms == platform
            count = mask.sum()

            if count == 0:
                continue

            p = profiles[platform]

            imp = rng.integers(*p['imp'], size=count)
            ctr = rng.uniform(*p['ctr'], size=count)
            clk = np.maximum(1, (imp * ctr).astype(int))
            cpc = rng.uniform(*p['cpc'], size=count)
            conv_rate = rng.uniform(*p['cr'], size=count)
            conv = rng.binomial(clk, conv_rate)

            aov = rng.uniform(*p['aov'], size=count)
            rev = np.where(
                conv > 0,
                conv * aov * rng.uniform(0.9, 1.15, size=count),
                0
            )

            impressions[mask] = imp
            clicks[mask] = clk
            spend[mask] = np.round(clk * cpc, 2)
            conversions[mask] = conv
            revenue[mask] = np.round(rev, 2)

        dates = pd.to_datetime('2023-01-01') + pd.to_timedelta(
            rng.integers(0, 731, size=n), unit='D'
        )

        df = pd.DataFrame({
            'date': dates.strftime('%Y-%m-%d'),
            'campaign': rng.choice(campaigns, size=n),
            'platform': selected_platforms,
            'impressions': impressions,
            'clicks': clicks,
            'spend': spend,
            'conversions': conversions,
            'revenue': revenue,
            'age': rng.choice(age_groups, size=n, p=age_weights),
            'gender': rng.choice(genders, size=n, p=gender_weights),
            'city': rng.choice(cities, size=n, p=city_weights),
            'device': rng.choice(devices, size=n, p=device_weights)
        })

        df.to_csv(
            out_path,
            mode='a',
            header=(records_written == 0),
            index=False
        )

        records_written += n
        print(f'Generated {records_written:,} / {num_records:,} records')

    print('\nDataset generation completed!')
    print(f'Total records: {records_written:,}')
    print(f'Saved to: {out_path}')


if __name__ == '__main__':
    generate_advertising_dataset()
