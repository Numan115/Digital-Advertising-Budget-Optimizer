"""
clean_data.py
Cleans and validates raw advertising data for Project 2.
Input: data/raw/advertising_data_raw.csv
Output: data/processed/advertising_data_cleaned.csv
"""

import os
import pandas as pd

def clean_advertising_data(input_path='data/raw/advertising_data_raw.csv',
                           output_path='data/processed/advertising_data_cleaned.csv'):
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    print(f"Initial row count: {initial_rows}")
    
    # 1. Deduplication
    duplicates = df.duplicated().sum()
    print(f"Duplicates identified: {duplicates}")
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Row count after removing duplicates: {len(df)}")
    
    # 2. Date conversion
    df['date'] = pd.to_datetime(df['date'])
    
    # 3. Handle missing values if any
    missing_count = df.isnull().sum().sum()
    print(f"Total missing values: {missing_count}")
    if missing_count > 0:
        df = df.dropna().reset_index(drop=True)
        
    # 4. Business rule validation
    # clicks must be <= impressions
    valid_clicks = (df['clicks'] <= df['impressions']).all()
    # conversions must be <= clicks
    valid_conv = (df['conversions'] <= df['clicks']).all()
    # spend and revenue non-negative
    valid_spend = (df['spend'] >= 0).all()
    valid_rev = (df['revenue'] >= 0).all()
    
    print("\nBusiness Validation Checks:")
    print(f" - Clicks <= Impressions: {valid_clicks}")
    print(f" - Conversions <= Clicks: {valid_conv}")
    print(f" - Non-negative Spend: {valid_spend}")
    print(f" - Non-negative Revenue: {valid_rev}")
    
    # Ensure processed directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nCleaned and validated data successfully saved to: {output_path}")
    print(f"Final records count: {len(df)}")
    return df

if __name__ == '__main__':
    clean_advertising_data()
