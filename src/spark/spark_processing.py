"""
spark_processing.py
Apache Spark In-Memory Parallel Processing Engine.
Emulates Spark's RDD & DataFrame architecture:
- Partitioning across CPU cores
- Lazy evaluation & DAG transformation pipeline
- In-memory partition-level local reduction (Combiner)
- Parallel shuffle & reduceByKey aggregation without disk spilling
"""

import os
import sys
import time
import tracemalloc
import multiprocessing as mp
from functools import reduce

def process_partition(lines):
    """
    Spark Partition Worker:
    Executes in-memory Map & Partition-level Combiner (reduceByKey local)
    """
    local_acc = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith('date') or 'platform' in line:
            continue
        parts = line.split(',')
        if len(parts) >= 8:
            platform = parts[2]
            try:
                clicks = int(parts[4])
                spend = float(parts[5])
                conv = int(parts[6])
                rev = float(parts[7])
                
                if platform not in local_acc:
                    local_acc[platform] = [spend, rev, clicks, conv]
                else:
                    acc = local_acc[platform]
                    acc[0] += spend
                    acc[1] += rev
                    acc[2] += clicks
                    acc[3] += conv
            except (ValueError, IndexError):
                continue
    return local_acc

def merge_spark_accumulators(acc1, acc2):
    """Spark Global Reducer combining partition results in memory"""
    result = dict(acc1)
    for p, vals in acc2.items():
        if p in result:
            result[p] = [
                result[p][0] + vals[0],
                result[p][1] + vals[1],
                result[p][2] + vals[2],
                result[p][3] + vals[3]
            ]
        else:
            result[p] = list(vals)
    return result

def execute_spark(csv_path, num_partitions=None):
    if num_partitions is None:
        num_partitions = max(2, mp.cpu_count())
        
    print(f"\n[Apache Spark Engine] Processing: {csv_path} with {num_partitions} in-memory partitions")
    tracemalloc.start()
    t0 = time.time()
    
    # In-memory distributed partition read (RDD partition chunking)
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        all_lines = f.readlines()
        
    chunk_size = len(all_lines) // num_partitions + 1
    partitions = [all_lines[i * chunk_size : (i + 1) * chunk_size] for i in range(num_partitions)]
    
    # Parallel RDD Transformations via Worker Pool
    with mp.Pool(processes=num_partitions) as pool:
        partition_results = pool.map(process_partition, partitions)
        
    # Global In-Memory Action (collect / aggregate)
    final_aggregation = reduce(merge_spark_accumulators, partition_results)
    
    t1 = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    runtime = t1 - t0
    peak_mb = peak / (1024 * 1024)
    
    print("\nPlatform\tTotal_Spend\tTotal_Revenue\tClicks\tConversions\tROAS\tCPA")
    for platform in sorted(final_aggregation.keys()):
        spend, rev, clicks, conv = final_aggregation[platform]
        roas = round(rev / spend, 2) if spend > 0 else 0.0
        cpa = round(spend / conv, 2) if conv > 0 else 0.0
        print(f"{platform}\t{spend:.2f}\t{rev:.2f}\t{clicks}\t{conv}\t{roas}\t{cpa}")
        
    print(f"[Spark Completed] Runtime: {runtime:.3f} s | Peak RAM: {peak_mb:.2f} MB")
    return {'engine': 'Apache Spark', 'runtime': runtime, 'peak_ram_mb': peak_mb}

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/advertising_data_raw.csv'
    execute_spark(target)
