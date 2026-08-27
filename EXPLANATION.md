# ==============================
# FINANCIAL RATIO ENGINE - EXPLANATION
# ==============================

1. OBJECTIVE
The goal of this project is to build a financial analytics engine that computes key financial ratios,
evaluates company quality, and enables screening of fundamentally strong companies.

---

2. DATA SOURCES
The system uses three main datasets:

- profitandloss → revenue, profit, EPS
- balancesheet → assets, equity, reserves, debt
- cashflow → operating, investing, financing cash flows

These are merged using (symbol, year) as the primary keys.

---

3. DATA PROCESSING

- Inner join used between P&L and Balance Sheet to ensure valid financial base
- Left join used for Cash Flow to avoid data loss
- Data sorted by (symbol, year) for time-series calculations

---

4. RATIO CALCULATIONS

Profitability:
- Net Profit Margin = Net Profit / Sales
- Operating Profit Margin = Operating Profit / Sales
- ROE = Net Profit / (Equity + Reserves)
- ROCE = EBIT / (Equity + Reserves + Debt)
- ROA = Net Profit / Assets

Leverage:
- Debt to Equity = Debt / (Equity + Reserves)
  - Ignored if equity base is weak (< 500)
  - Avoids inflated ratios

Cash Flow:
- Free Cash Flow = Operating CF - Investing CF
- FCF Conversion = FCF / Operating Profit
- Capex Intensity = Investing CF / Sales

Efficiency:
- Asset Turnover = Sales / Assets

---

5. DATA QUALITY HANDLING

- Null values handled using conditional checks
- Invalid divisions avoided (zero or negative base)
- Extreme values filtered:
  - ROE > 300 → ignored
  - ROA > 100 → ignored
- Weak equity base ignored for D/E to prevent distortion

---

6. GROWTH METRICS

5-Year CAGR calculated for:
- Revenue
- Net Profit (PAT)
- EPS

Flags added to indicate reliability of CAGR based on data availability.

---

7. CASH FLOW QUALITY

Cash flow quality is evaluated using:
- CFO vs PAT comparison
- Consistency of operating cash flows

Companies are labeled as:
- HIGH_QUALITY
- MODERATE
- LOW

---

8. CAPITAL ALLOCATION

Capital allocation pattern derived using:
- Operating CF (CFO)
- Investing CF (CFI)
- Financing CF (CFF)

Helps classify company behavior (growth, debt-driven, etc.)

---

9. SCORING MODEL

Three factors used:

- ROE Score (50% weight)
- Leverage Score (30% weight)
- CFO Quality Score (20% weight)

Final Score scaled to 0–20 and categorized:

- COMPOUNDER (>= 20)
- GOOD (>= 15)
- AVERAGE (>= 10)
- WEAK (< 10)

---

10. VALIDATION

SQL queries were used to validate:

- Total records count (1057 rows)
- Null values in key metrics
- Range checks (min/max values)
- Distribution of ROE and Debt/Equity
- High-quality company filtering

Manual validation performed on:
RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK

Results confirmed:
- No missing years
- Consistent financial values
- No abnormal spikes

---

11. KEY OBSERVATIONS

- No companies found with ROE > 15 and Debt/Equity < 1 initially
- After data cleaning, valid low-leverage companies identified
- Debt/Equity required filtering due to small equity distortions

---

12. OUTPUTS GENERATED

- financial_ratios table (main output)
- capital_allocation.csv
- ratio_edge_cases.log

---

13. LIMITATIONS

- Thresholds (e.g., equity < 500) are heuristic-based
- Sector-specific adjustments are minimal
- Some extreme real-world cases may be filtered out

---

14. CONCLUSION

The system successfully computes financial ratios, filters unreliable data,
and provides a structured framework for identifying fundamentally strong companies.