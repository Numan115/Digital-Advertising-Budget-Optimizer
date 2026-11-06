#!/usr/bin/env python
"""
reducer.py
Hadoop Streaming compliant Reducer for Advertising Analytics.
Reads sorted Key-Value pairs from sys.stdin:
    Platform \t spend,revenue,clicks,conversions
Aggregates metrics and computes final KPIs:
    Total Spend, Total Revenue, Total Clicks, Total Conversions, ROAS, CPA
"""

import sys

def main():
    current_platform = None
    tot_spend = 0.0
    tot_revenue = 0.0
    tot_clicks = 0
    tot_conv = 0
    
    print("Platform\tTotal_Spend\tTotal_Revenue\tClicks\tConversions\tROAS\tCPA")
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            platform, values = line.split('\t', 1)
            spend, rev, clicks, conv = values.split(',')
            
            spend = float(spend)
            rev = float(rev)
            clicks = int(clicks)
            conv = int(conv)
        except (ValueError, IndexError):
            continue
        
        if current_platform == platform:
            tot_spend += spend
            tot_revenue += rev
            tot_clicks += clicks
            tot_conv += conv
        else:
            if current_platform is not None:
                roas = round(tot_revenue / tot_spend, 2) if tot_spend > 0 else 0.0
                cpa = round(tot_spend / tot_conv, 2) if tot_conv > 0 else 0.0
                print(f"{current_platform}\t{tot_spend:.2f}\t{tot_revenue:.2f}\t{tot_clicks}\t{tot_conv}\t{roas}\t{cpa}")
            
            current_platform = platform
            tot_spend = spend
            tot_revenue = rev
            tot_clicks = clicks
            tot_conv = conv
            
    # Output the last platform
    if current_platform is not None:
        roas = round(tot_revenue / tot_spend, 2) if tot_spend > 0 else 0.0
        cpa = round(tot_spend / tot_conv, 2) if tot_conv > 0 else 0.0
        print(f"{current_platform}\t{tot_spend:.2f}\t{tot_revenue:.2f}\t{tot_clicks}\t{tot_conv}\t{roas}\t{cpa}")

if __name__ == '__main__':
    main()
