# Nifty100 Data Engineering & Financial Analytics Pipeline

## Overview

This project builds an end-to-end ETL + Analytics pipeline to ingest, clean, validate, and analyze financial data of Nifty 100 companies using SQLite.

It simulates a real-world data engineering workflow and extends into financial analytics by computing key ratios, evaluating company quality, and enabling stock screening.

---

## Features

### 🔹 Data Engineering (ETL)

- Ingests data from 12 Excel source files
- Loads into 10+ normalized SQLite tables
- Implements Data Quality (DQ) rules:
  - PK uniqueness
  - FK integrity
  - Financial validations (balance sheet, cash flow)

- Generates:
  - `load_audit.csv` → row counts & rejected data
  - `validation_failures.csv` → DQ rule results

---

### 🔹 Financial Analytics Engine

- Computes key financial ratios:
  - Profitability → ROE, ROCE, ROA, Margins
  - Leverage → Debt to Equity, High Leverage Flag
  - Efficiency → Asset Turnover
  - Cash Flow → FCF, FCF Conversion, Capex Intensity

- Growth metrics:
  - 5-Year CAGR (Revenue, PAT, EPS)

- Cash Flow Quality classification:
  - HIGH_QUALITY / MODERATE / LOW

- Capital Allocation pattern detection

---

### 🔹 Scoring & Classification

- Composite Quality Score based on:
  - ROE (50%)
  - Leverage (30%)
  - Cash Flow Quality (20%)

- Final Rating:
  - COMPOUNDER
  - GOOD
  - AVERAGE
  - WEAK

---

### 🔹 Validation & Audit

- SQL-based validation queries:
  - Row counts
  - Null checks
  - Min/Max range checks
  - Ratio distribution analysis

- Manual validation performed on:
  - RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK

- Outputs:
  - `ratio_edge_cases.log`
  - `capital_allocation.csv`

---

## Tech Stack

- Python (Pandas)
- SQLite / SQL
- Pytest
- Excel (openpyxl)

---

## Project Structure

Nifty100/
│
├── src/
│ ├── etl/
│ │ ├── loader.py
│ │ ├── validator.py
│ │
│ ├── analytics/
│ │ ├── ratios.py
│ │ ├── cashflow_kpis.py
│ │ ├── cagr.py
│ │
│ └── engine.py
│
├── db/
│ └── schema.sql
│
├── output/
│ ├── load_audit.csv
│ ├── validation_failures.csv
│ ├── capital_allocation.csv
│ └── ratio_edge_cases.log
│
├── data/
│ └── main/companies.xlsx
│
├── tests/
│ └── test_normalizer.py
│
├── notebooks/
│ └── exploratory_queries.sql
│
├── requirements.txt
├── explanation.txt
├── manual_review.txt
└── README.md


---
## How to Run
### Install dependencies
```bash
pip install -r requirements.txt
Run ETL pipeline
python src/etl/loader.py
Run validation
python src/etl/validator.py
Run analytics engine
python src/engine.py
Run tests
pytest
Output Files
Data Engineering Outputs
load_audit.csv
→ Tracks rows loaded and rejected per table
validation_failures.csv
→ Data quality check results
Analytics Outputs
financial_ratios (SQLite table)
→ Main computed dataset (~1000+ rows)
capital_allocation.csv
→ Company capital usage patterns
ratio_edge_cases.log
→ Flags inconsistencies vs reference data
Key Learnings
Designing end-to-end data pipelines
Handling real-world messy financial data
Implementing validation & audit layers
Building financial analytics systems
Combining SQL + Python for data analysis
Data Notes
Some inconsistencies are expected due to real-world financial reporting differences
Extreme/unrealistic values are filtered during processing
financial_ratios is a derived table generated after ETL
Future Improvements
Sector-specific ratio thresholds
Dashboard visualization (Power BI / Streamlit)
API layer for querying financial data
Advanced screening strategies
Author
CMR
---
## 🔥 What changed (so you understand)
- Added **analytics engine (your biggest upgrade)**
- Added **scoring system (this is interview gold)**
- Updated **project structure**
- Separated **ETL vs Analytics**
- Made it look like a **complete system, not just ETL**
---
## 🚀 Next Step (important)
Now do:
```bash
git add README.md
git commit -m "Updated README with analytics engine and scoring system"
git push