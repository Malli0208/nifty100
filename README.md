Nifty100 Data Engineering Pipeline

Overview
 This project builds an end-to-end ETL pipeline to ingest, clean, validate, and store financial data of Nifty 100 companies into a structured SQLite database.
 It simulates real-world data engineering workflows including data ingestion, normalization, validation, and auditing.

Features
Ingests data from 12 Excel source files
Loads into 10 normalized SQLite tables
Implements 16 Data Quality (DQ) rules
 PK uniqueness
 FK integrity
 Financial validations (balance sheet, cash flow)
Generates:
 load_audit.csv → row counts & rejected data
 validation_failures.csv → DQ rule results
 Unit tests for normalization functions

Tech Stack
 Python (Pandas, SQLite3)
 SQL
 Pytest
 VS Code

Project Structure
Nifty100/
│
├── src/etl/
│   ├── loader.py
│   ├── validator.py
│
├── db/
│   └── schema.sql
│
├── output/
│   ├── load_audit.csv
│   └── validation_failures.csv
│
├── tests/
│   └── test_normalizer.py
│
├── notebooks/
│   └── exploratory_queries.sql
│
├── requirements.txt
├── Makefile
└── README.md

How to Run
Install dependencies
   pip install -r requirements.txt
Run ETL pipeline
   python src/etl/loader.py
Run validation
   python src/etl/validator.py
Run tests
   pytest

Output Files
load_audit.csv
Tracks number of rows loaded and rejected per table.
validation_failures.csv
Contains results of all data quality checks:
  CRITICAL → must fix
  WARNING → acceptable data issues

Key Learnings
 Handling real-world messy data
 Designing relational database schema
 Implementing data validation rules
 Debugging ETL pipelines
 Working with financial datasets

Data Notes
 Some financial inconsistencies (e.g., balance mismatch, net cash mismatch) are expected due to real-world data variations.
 No critical data quality failures remain.

Future Improvements
 KPI calculations (ROE, ROCE, margins)
 Dashboard visualization
 API layer for querying data

Author
 CMR
