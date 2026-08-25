import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

results = []

def check(rule, table, issue, query, severity):
    res = conn.execute(query).fetchall()
    count = len(res)

    status = "FAIL" if count > 0 and severity == "CRITICAL" else (
        "WARN" if count > 0 else "OK"
    )

    results.append([
        rule,
        table,
        f"{issue} ({count})",
        status
    ])


# =========================
# CRITICAL RULES
# =========================

check(
    "DQ-01", "companies", "duplicate symbols",
    """SELECT symbol FROM companies GROUP BY symbol HAVING COUNT(*) > 1""",
    "CRITICAL"
)

check(
    "DQ-02", "profitandloss", "duplicate symbol-year",
    """SELECT symbol FROM profitandloss GROUP BY symbol, year HAVING COUNT(*) > 1""",
    "CRITICAL"
)

check(
    "DQ-03", "profitandloss", "invalid FK",
    """SELECT symbol FROM profitandloss WHERE symbol NOT IN (SELECT symbol FROM companies)""",
    "CRITICAL"
)


# =========================
# WARNING RULES
# =========================

check(
    "DQ-04", "balancesheet", "balance mismatch",
    """SELECT * FROM balancesheet WHERE ABS(assets - (liabilities + equity)) > assets * 0.05""",
    "WARNING"
)

check(
    "DQ-05", "profitandloss", "OPM abnormal",
    """SELECT * FROM profitandloss WHERE operating_profit > sales * 2""",
    "WARNING"
)

check(
    "DQ-06", "profitandloss", "negative sales",
    """SELECT * FROM profitandloss WHERE sales < 0""",
    "WARNING"
)

check(
    "DQ-07", "balancesheet", "negative assets",
    """SELECT * FROM balancesheet WHERE assets < 0""",
    "WARNING"
)

check(
    "DQ-08", "balancesheet", "negative debt",
    """SELECT * FROM balancesheet WHERE debt < 0""",
    "WARNING"
)

check(
    "DQ-09", "cashflow", "net cash mismatch",
    """SELECT * FROM cashflow WHERE ABS(net_cash - (operating_cf + investing_cf + financing_cf)) > 1""",
    "WARNING"
)

check(
    "DQ-10", "profitandloss", "EPS null",
    """SELECT * FROM profitandloss WHERE eps IS NULL""",
    "WARNING"
)


# =========================
# EXTRA RULES (11–16)
# =========================

check(
    "DQ-11", "profitandloss", "year null",
    """SELECT * FROM profitandloss WHERE year IS NULL""",
    "WARNING"
)

check(
    "DQ-12", "companies", "company name null",
    """SELECT * FROM companies WHERE company_name IS NULL""",
    "WARNING"
)

check(
    "DQ-13", "profitandloss", "zero sales",
    """SELECT * FROM profitandloss WHERE sales = 0""",
    "WARNING"
)

check(
    "DQ-14", "balancesheet", "negative equity",
    """SELECT * FROM balancesheet WHERE equity < 0""",
    "WARNING"
)

check(
    "DQ-15", "stock_prices", "duplicate keys",
    """SELECT col0 FROM stock_prices GROUP BY col0 HAVING COUNT(*) > 1""",
    "WARNING"
)

check(
    "DQ-16", "companies", "missing sector",
    """SELECT * FROM companies WHERE sector IS NULL""",
    "WARNING"
)


# =========================
# SAVE OUTPUT
# =========================

df = pd.DataFrame(results, columns=["rule", "table", "issue", "status"])
df.to_csv("output/validation_failures.csv", index=False)

print("\nVALIDATION RESULTS:\n")
print(df)

conn.close()