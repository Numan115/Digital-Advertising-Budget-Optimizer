"""
pandas_processing.py
Standard In-Memory Single-Threaded Pandas Processing Engine.
"""

import sys
import time
import tracemalloc
import pandas as pd

def execute_pandas(csv_path):
    print(f"\n[Pandas Engine] Processing: {csv_path}")
    tracemalloc.start()
    t0 = time.time()
    
    df = pd.read_csv(csv_path)
    
    grouped = df.groupby('platform').agg(
        Total_Spend=('spend', 'sum'),
        Total_Revenue=('revenue', 'sum'),
        Clicks=('clicks', 'sum'),
        Conversions=('conversions', 'sum')
    ).reset_index()
    
    grouped['ROAS'] = (grouped['Total_Revenue'] / grouped['Total_Spend']).round(2)
    grouped['CPA'] = (grouped['Total_Spend'] / grouped['Conversions']).round(2)
    
    t1 = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    runtime = t1 - t0
    peak_mb = peak / (1024 * 1024)
    
    print("\n" + grouped.to_string(index=False))
    print(f"[Pandas Completed] Runtime: {runtime:.3f} s | Peak RAM: {peak_mb:.2f} MB")
    return {'engine': 'Pandas', 'runtime': runtime, 'peak_ram_mb': peak_mb}

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/advertising_data_raw.csv'
    execute_pandas(target)
