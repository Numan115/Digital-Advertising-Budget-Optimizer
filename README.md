# Digital Advertising Budget Optimizer
**End-to-End Big Data Analytics & Marketing Decision Support System**

---

## Executive Summary
This project analyzes multi-channel digital advertising campaigns across Pakistan to solve a core business challenge:  
> **Business Problem:** A company is advertising across Facebook, Instagram, Google, TikTok, and YouTube. Management has an additional **Rs. 1,000,000** and needs a data-driven system to allocate this budget to generate maximum revenue and conversions.

---

## Project Architecture: 3-Part Modular Design

```text
Project 2 / Digital-Advertising-Budget-Optimizer/
│
├── data/
│   ├── raw/
│   │   └── advertising_data_raw.csv           # 10,025 raw simulated records (Part 1)
│   ├── processed/
│   │   ├── advertising_data_cleaned.csv       # Deduplicated & cleaned data
│   │   └── advertising_data_with_kpis.csv     # Calculated KPIs (CTR, CPC, CPA, ROAS)
│   └── scaled/
│       ├── advertising_100k.csv               # 100,000 records (~9.4 MB) (Part 2)
│       └── advertising_1m.csv                 # 1,000,000 records (~94 MB) (Part 2)
│
├── notebooks/
│   ├── part1_analysis.ipynb                   # Part 1: Exploratory analysis & KPIs
│   ├── part2_big_data_benchmark.ipynb         # Part 2: Pandas vs MapReduce vs Spark
│   └── part3_budget_optimizer.ipynb           # Part 3: Budget Recommendation Engine
│
├── src/
│   ├── generate_data.py                       # Simulates 10,000 raw ad records
│   ├── clean_data.py                          # Data validation & cleaning pipeline
│   ├── calculate_metrics.py                   # Computes CTR, CPC, CPA, ROAS
│   ├── scale_dataset.py                       # Generates 100K and 1M records
│   ├── pandas_processing.py                   # Pandas in-memory processor
│   ├── benchmark_comparison.py                # Comparative benchmark driver
│   ├── budget_optimizer.py                    # Multi-criteria budget optimizer
│   ├── generate_visualizations.py             # Generates Part 1 charts (1-10)
│   ├── generate_part3_visualizations.py       # Generates Part 3 charts (14-16)
│   ├── mapreduce/
│   │   ├── mapper.py                          # Hadoop Streaming Mapper
│   │   ├── reducer.py                         # Hadoop Streaming Reducer
│   │   └── run_mapreduce.py                   # MapReduce execution driver
│   └── spark/
│       └── spark_processing.py                # Spark parallel in-memory RDD engine
│
├── visualizations/                            # 16 High-Resolution PNG Visualizations
│   ├── 01_platform_roas_comparison.png
│   ├── 02_spend_vs_revenue_by_platform.png
│   ├── 03_ctr_vs_conversion_rate.png
│   ├── 04_cpa_by_platform.png
│   ├── 05_campaign_performance_roas.png
│   ├── 06_demographics_heatmap.png
│   ├── 07_city_revenue_performance.png
│   ├── 08_device_distribution_donut.png
│   ├── 09_monthly_performance_trend.png
│   ├── 10_platform_day_of_week_roas.png
│   ├── 11_bigdata_execution_time_comparison.png
│   ├── 12_bigdata_memory_usage_comparison.png
│   ├── 13_bigdata_scalability_curve.png
│   ├── 14_budget_allocation_donut.png
│   ├── 15_projected_financial_impact.png
│   └── 16_before_vs_after_roas.png
│
├── reports/
│   ├── part1_findings.md                      # Part 1: EDA & Baseline Marketing Report
│   ├── part2_big_data_findings.md             # Part 2: Big Data Benchmarking Report
│   ├── part3_final_budget_recommendations.md  # Part 3: Rs. 1M Budget Allocation Report
│   ├── big_data_benchmark_results.csv         # Benchmark metrics across engines & scales
│   └── budget_allocation_recommendations.csv  # Platform-by-platform budget distribution
│
├── README.md
└── requirements.txt
```

---

## Summary of Key Results

### 1. Part 1 — Marketing Analytics & Baseline KPIs
- **Google & Instagram** led overall ROAS (**6.13x** and **5.89x** respectively).
- **TikTok** achieved the lowest Cost Per Click (**Rs. 14.94**) and highest CTR (**4.26%**).
- **Mobile devices** drove **75%** of all engagements and conversions.

### 2. Part 2 — Big Data Benchmarking (Pandas vs MapReduce vs Spark)
- At **10K & 100K records**, **Pandas** runs fastest due to low in-memory overhead.
- At **1M records**, **Apache Spark** surpasses MapReduce in runtime (**12.06s vs 13.17s**) by eliminating disk-spill overhead via in-memory partition-level reduction.
- **Hadoop MapReduce** maintains the most stable memory footprint across scales.

### 3. Part 3 — Rs. 1,000,000 Budget Recommendation
| Platform | Recommended Budget (PKR) | Allocation % | Expected Revenue (PKR) | Expected Profit (PKR) | ROAS |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Google** | **Rs. 311,300** | 31.13% | Rs. 1,906,864 | Rs. 1,595,564 | **6.13x** |
| **Instagram** | **Rs. 305,400** | 30.54% | Rs. 1,799,921 | Rs. 1,494,521 | **5.89x** |
| **Facebook** | **Rs. 203,300** | 20.33% | Rs. 942,943 | Rs. 739,643 | **4.64x** |
| **TikTok** | **Rs. 180,000** | 18.00% | Rs. 754,907 | Rs. 574,907 | **4.19x** |
| **YouTube** | **Rs. 0** | 0.00% | Rs. 0 | Rs. 0 | 3.07x |
| **TOTAL** | **Rs. 1,000,000** | **100%** | **Rs. 5,404,635** | **Rs. 4,404,635** | **5.40x** |

---

## How to Run This Project

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute Part 1 (Data Generation, Cleaning, & KPIs):**
   ```bash
   python src/generate_data.py
   python src/clean_data.py
   python src/calculate_metrics.py
   python src/generate_visualizations.py
   ```
3. **Execute Part 2 (Big Data Scaling & Benchmarking):**
   ```bash
   python src/scale_dataset.py --sizes 100k 1m
   python src/benchmark_comparison.py
   ```
4. **Execute Part 3 (Budget Optimizer):**
   ```bash
   python src/budget_optimizer.py
   python src/generate_part3_visualizations.py
   ```
5. **Open Interactive Notebooks:**
   Launch Jupyter and explore [`notebooks/part1_analysis.ipynb`](notebooks/part1_analysis.ipynb), [`notebooks/part2_big_data_benchmark.ipynb`](notebooks/part2_big_data_benchmark.ipynb), or [`notebooks/part3_budget_optimizer.ipynb`](notebooks/part3_budget_optimizer.ipynb).
