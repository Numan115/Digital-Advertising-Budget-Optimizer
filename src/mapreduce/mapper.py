#!/usr/bin/env python
"""
mapper.py
Hadoop Streaming compliant Mapper for Advertising Analytics.
Reads CSV rows from standard input (sys.stdin).
Emits Key-Value pairs to sys.stdout in the format:
    Platform \t spend,revenue,clicks,conversions
"""

import sys

def main():
    # Detect and skip header row
    first_line = True
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(',')
        if first_line:
            first_line = False
            # Check if this is the header row
            if parts[0] == 'date' or 'platform' in line:
                continue
        
        # Expected Schema:
        # 0: date, 1: campaign, 2: platform, 3: impressions, 4: clicks, 
        # 5: spend, 6: conversions, 7: revenue, 8: age, 9: gender, 10: city, 11: device
        if len(parts) >= 8:
            platform = parts[2]
            try:
                clicks = parts[4]
                spend = parts[5]
                conversions = parts[6]
                revenue = parts[7]
                
                # Emit: key \t spend,revenue,clicks,conversions
                print(f"{platform}\t{spend},{revenue},{clicks},{conversions}")
            except (ValueError, IndexError):
                continue

if __name__ == '__main__':
    main()
