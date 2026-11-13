# Project 2 — Digital Advertising Budget Optimizer
## Part 1: Exploratory Data Analysis & Marketing Performance Report

**Date:** November 2026  
**Dataset:** 10,000 Advertising Records (Simulated across Pakistan, 2023–2024)  
**Target Goal:** Evaluate multi-platform advertising efficiency to guide the allocation of an additional **Rs. 1,000,000** budget.

---

## 1. Executive Summary

This report establishes the baseline analysis for **Project 2: Digital Advertising Budget Optimizer**. Over 2023 and 2024, our multi-platform digital advertising campaigns generated:
- **Total Ad Spend:** Rs. 162.27 Million
- **Total Revenue:** Rs. 850.18 Million
- **Overall Return on Ad Spend (ROAS):** **5.24x** (Every Rs. 1 invested generated Rs. 5.24 in gross sales)
- **Total Clicks:** 6.6 Million clicks across 198.8 Million impressions
- **Total Conversions:** 243,088 successful sales / conversions

---

## 2. Platform-by-Platform Performance Breakdown

| Platform | Total Spend (PKR) | Total Revenue (PKR) | Clicks | Conversions | Avg CTR (%) | Avg CPC (Rs.) | Conv Rate (%) | Overall CPA (Rs.) | Overall ROAS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Google** | Rs. 47.41M | Rs. 290.39M | 1,117,453 | 64,567 | 4.02% | Rs. 42.61 | **5.77%** | Rs. 734.24 | **6.13x** |
| **Instagram** | Rs. 43.02M | Rs. 253.54M | 1,588,242 | **68,287** | 3.23% | Rs. 27.01 | 4.29% | **Rs. 629.99** | **5.89x** |
| **Facebook** | Rs. 32.29M | Rs. 149.76M | 1,403,307 | 48,738 | 2.65% | Rs. 23.06 | 3.47% | Rs. 662.48 | **4.64x** |
| **TikTok** | Rs. 31.18M | Rs. 130.76M | **2,078,075** | 51,926 | **4.26%** | **Rs. 14.94** | 2.50% | **Rs. 600.45** | **4.19x** |
| **YouTube** | Rs. 8.38M | Rs. 25.73M | 419,165 | 9,296 | 2.09% | Rs. 20.07 | 2.20% | Rs. 901.31 | **3.07x** |

---

## 3. Core Analytical Findings

### Finding 1: Google Delivers the Highest Return on Investment
- **Observation:** Google delivers the highest conversion rate (5.77%) and the highest overall ROAS (6.13x).
- **Reasoning:** Google ads capture **high commercial intent** (users actively searching for products/solutions), translating into higher cart values and lower abandonment despite higher CPC.

### Finding 2: Instagram is the Most Balanced Conversion Engine
- **Observation:** Instagram delivered the greatest total volume of conversions (68,287) and high ROAS (5.89x) with a very cost-effective CPA (Rs. 630).
- **Reasoning:** Strong visual appeal, seamless in-app purchasing, and high engagement across the 18–34 age brackets.

### Finding 3: TikTok Offers Unmatched Top-of-Funnel Reach & Low CPC
- **Observation:** TikTok achieved the lowest Cost Per Click (Rs. 14.94) and highest Click-Through Rate (4.26%), while keeping CPA low (Rs. 600).
- **Reasoning:** Exceptional viral algorithmic distribution and high engagement with Gen Z and young millennials.

### Finding 4: YouTube Requires Repositioning
- **Observation:** YouTube has the lowest ROAS (3.07x) and highest acquisition cost (CPA Rs. 901).
- **Reasoning:** Video ads are primarily upper-funnel brand awareness drivers rather than direct-response purchase vehicles.

---

## 4. Demographic & Geographic Insights (Pakistan)

1. **Top Cities by Revenue:**
   - **Karachi:** ~30% of total revenue (~Rs. 255 Million)
   - **Lahore:** ~25% of total revenue (~Rs. 212 Million)
   - **Islamabad & Rawalpindi:** ~23% combined (~Rs. 195 Million)
   - Secondary cities (Faisalabad, Multan, Peshawar, Quetta, Sialkot, Gujranwala) represent growing opportunities.

2. **Device Preference:**
   - **Mobile Devices:** Account for **75.2%** of all ad clicks and impressions.
   - **Desktop:** 19.8% (mainly daytime office hours on Google and Facebook).
   - **Tablet:** 5.0%.

---

## 5. Visualizations Index

All 10 high-resolution charts are saved in `visualizations/`:
1. `01_platform_roas_comparison.png` — Comparison of ROAS across all 5 platforms.
2. `02_spend_vs_revenue_by_platform.png` — Total Spend vs Revenue in PKR Millions.
3. `03_ctr_vs_conversion_rate.png` — Click-Through Rate vs Conversion Rate.
4. `04_cpa_by_platform.png` — Cost per Acquisition (CPA) efficiency.
5. `05_campaign_performance_roas.png` — Campaign-level ROAS ranking.
6. `06_demographics_heatmap.png` — Age group × Gender ROAS interaction.
7. `07_city_revenue_performance.png` — Revenue across Pakistani cities.
8. `08_device_distribution_donut.png` — Share of mobile vs desktop vs tablet.
9. `09_monthly_performance_trend.png` — 24-month spend and revenue trend.
10. `10_platform_day_of_week_roas.png` — Day-of-week timing patterns.

---

## 6. Strategic Direction for Part 2 & Part 3

- **Part 2 (Big Data Scaling):** We will scale this schema to 100K, 1M, and 10M records and benchmark **Pandas vs. MapReduce vs. Apache Spark** across execution runtime and memory usage.
- **Part 3 (Budget Optimizer):** To allocate the additional **Rs. 1,000,000**, our mathematical optimization model should assign:
  - **40% (Rs. 400,000)** to **Google** (Maximizing high-ticket conversion & ROAS)
  - **35% (Rs. 350,000)** to **Instagram** (Maximizing conversion volume and low CPA)
  - **15% (Rs. 150,000)** to **TikTok** (Top-of-funnel youth acquisition)
  - **10% (Rs. 100,000)** to **Facebook** (Remarketing and regional retention)
  - **0% (Rs. 0)** to **YouTube** (Deprioritize paid direct-response ads due to lowest ROAS)
