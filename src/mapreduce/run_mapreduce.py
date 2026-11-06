"""
run_mapreduce.py
Executes the MapReduce pipeline (Mapper -> Shuffle/Sort -> Reducer)
over advertising datasets and logs runtime and memory.
"""

import os
import sys
import time
import subprocess
import tracemalloc

def execute_mapreduce(csv_path):
    print(f"\n[MapReduce Engine] Processing: {csv_path}")
    tracemalloc.start()
    t0 = time.time()
    
    mapper_path = os.path.join(os.path.dirname(__file__), 'mapper.py')
    reducer_path = os.path.join(os.path.dirname(__file__), 'reducer.py')
    
    # Emulate MapReduce streaming:
    # 1. Map Phase: Stream CSV into mapper
    p1 = subprocess.Popen([sys.executable, mapper_path], 
                          stdin=open(csv_path, 'r', encoding='utf-8', errors='ignore'),
                          stdout=subprocess.PIPE, text=True)
    
    # 2. Shuffle & Sort Phase
    # In Hadoop, the framework sorts mapper output by key before passing to reducers
    mapped_lines = p1.stdout.readlines()
    p1.stdout.close()
    p1.wait()
    
    sorted_lines = sorted(mapped_lines)
    
    # 3. Reduce Phase: Stream sorted pairs into reducer
    p2 = subprocess.Popen([sys.executable, reducer_path],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, text=True)
    
    reducer_output, _ = p2.communicate(input="".join(sorted_lines))
    
    t1 = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    runtime = t1 - t0
    peak_mb = peak / (1024 * 1024)
    
    print(reducer_output)
    print(f"[MapReduce Completed] Runtime: {runtime:.3f} s | Peak RAM: {peak_mb:.2f} MB")
    return {'engine': 'MapReduce', 'runtime': runtime, 'peak_ram_mb': peak_mb}

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'data/raw/advertising_data_raw.csv'
    execute_mapreduce(target)
