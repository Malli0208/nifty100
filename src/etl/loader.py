import pandas as pd
import sqlite3
import os
import re

DB_PATH = "nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# -------------------------------
# NORMALIZERS
# -------------------------------
def normalize_year(value):
    if pd.isna(value):
        return None

    value = str(value)
    match = re.search(r"(19|20)\d{2}", value)
    return int(match.group()) if match else None


def normalize_ticker(ticker):
    if pd.isna(ticker):
        return None

    ticker = str(ticker).upper().strip()

    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")
    ticker = ticker.replace(" LTD", "")
    ticker = ticker.replace(" LIMITED", "")

    return ticker


# -------------------------------
# HELPERS
# -------------------------------
def load_excel(file_path):
    df = pd.read_excel(file_path, header=None, skiprows=2)
    print(f"Loaded: {file_path} | Shape: {df.shape}")
    return df


# -------------------------------
# AUDIT
# -------------------------------
def write_audit(conn, rejected_counts):
    tables = [
        "companies", "profitandloss", "balancesheet",
        "cashflow", "analysis", "documents",
        "prosandcons", "financial_ratios",
        "stock_prices", "sectors", "peer_groups", "market_cap"
    ]

    audit = []

    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        rejected = rejected_counts.get(table, 0)
        audit.append([table, count, rejected])

    df = pd.DataFrame(audit, columns=["table_name", "rows_loaded", "rejected"])
    df.to_csv(f"{OUTPUT_DIR}/load_audit.csv", index=False)

    print("load_audit.csv created")


# -------------------------------
# VALIDATION
# -------------------------------
def write_validation(conn):
    checks = []

    dup = conn.execute("""
        SELECT COUNT(*) FROM (
            SELECT symbol, COUNT(*) c
            FROM companies GROUP BY symbol HAVING c > 1
        )
    """).fetchone()[0]

    checks.append(["DQ-01", "companies", "PK uniqueness", "OK" if dup == 0 else "FAIL"])

    dup = conn.execute("""
        SELECT COUNT(*) FROM (
            SELECT symbol, year, COUNT(*) c
            FROM profitandloss
            GROUP BY symbol, year HAVING c > 1
        )
    """).fetchone()[0]

    checks.append(["DQ-02", "profitandloss", "(symbol,year)", "OK" if dup == 0 else "FAIL"])

    fk = conn.execute("""
        SELECT COUNT(*) FROM profitandloss
        WHERE symbol NOT IN (SELECT symbol FROM companies)
    """).fetchone()[0]

    checks.append(["DQ-03", "FK", "integrity", "OK" if fk == 0 else "FAIL"])

    df = pd.DataFrame(checks, columns=["rule", "table", "issue", "status"])
    df.to_csv(f"{OUTPUT_DIR}/validation_failures.csv", index=False)

    print("validation_failures.csv created")


# -------------------------------
# LOADERS
# -------------------------------
def load_companies(conn, rejected):
    df = load_excel("data/main/companies.xlsx")

    df = df.iloc[:, [0, 2]]
    df.columns = ["symbol", "company_name"]

    df["symbol"] = df["symbol"].apply(normalize_ticker)

    # sector mapping
    sector_df = pd.read_excel("data/supporting/sectors.xlsx")
    sector_df = sector_df.iloc[:, [1, 2]]
    sector_df.columns = ["symbol", "sector"]
    sector_df["symbol"] = sector_df["symbol"].apply(normalize_ticker)

    sector_map = dict(zip(sector_df["symbol"], sector_df["sector"]))
    df["sector"] = df["symbol"].map(sector_map)

    before = len(df)
    df = df.drop_duplicates(subset=["symbol"])
    df = df[df["symbol"].notna()]

    rejected["companies"] = before - len(df)

    df.to_sql("companies", conn, if_exists="replace", index=False)
    print("companies:", len(df))


def load_profitandloss(conn, rejected):
    df = load_excel("data/main/profitandloss.xlsx")

    df = df.iloc[:, 1:8]
    df.columns = [
        "symbol", "raw_year", "sales", "expenses",
        "operating_profit", "net_profit", "eps"
    ]

    df["symbol"] = df["symbol"].apply(normalize_ticker)
    df["year"] = df["raw_year"].apply(normalize_year)

    df = df.drop_duplicates(subset=["symbol", "year"])

    valid_symbols = set(pd.read_sql("SELECT symbol FROM companies", conn)["symbol"])

    before = len(df)

    df = df[df["symbol"].isin(valid_symbols)]
    df = df[df["year"].notna()]
    df = df[df["sales"] > 0]

    rejected["profitandloss"] = before - len(df)

    df.to_sql("profitandloss", conn, if_exists="replace", index=False)
    print("profitandloss:", len(df))


def load_balancesheet(conn, rejected):
    df = load_excel("data/main/balancesheet.xlsx")

    df = df.iloc[:, 1:8]
    df.columns = [
        "symbol", "raw_year", "assets", "liabilities",
        "equity", "reserves", "debt"
    ]

    df["symbol"] = df["symbol"].apply(normalize_ticker)
    df["year"] = df["raw_year"].apply(normalize_year)

    df = df.drop_duplicates(subset=["symbol", "year"])

    valid_symbols = set(pd.read_sql("SELECT symbol FROM companies", conn)["symbol"])

    before = len(df)

    df = df[df["symbol"].isin(valid_symbols)]
    df = df[df["year"].notna()]

    rejected["balancesheet"] = before - len(df)

    df.to_sql("balancesheet", conn, if_exists="replace", index=False)
    print("balancesheet:", len(df))


def load_cashflow(conn, rejected):
    df = load_excel("data/main/cashflow.xlsx")

    df = df.iloc[:, 1:7]
    df.columns = [
        "symbol", "raw_year", "operating_cf",
        "investing_cf", "financing_cf", "net_cash"
    ]

    df["symbol"] = df["symbol"].apply(normalize_ticker)
    df["year"] = df["raw_year"].apply(normalize_year)

    df = df.drop_duplicates(subset=["symbol", "year"])

    valid_symbols = set(pd.read_sql("SELECT symbol FROM companies", conn)["symbol"])

    before = len(df)

    df = df[df["symbol"].isin(valid_symbols)]
    df = df[df["year"].notna()]

    rejected["cashflow"] = before - len(df)

    df.to_sql("cashflow", conn, if_exists="replace", index=False)
    print("cashflow:", len(df))


def load_simple(conn, file_path, table_name, rejected):
    df = load_excel(file_path)
    df.columns = [f"col{i}" for i in range(df.shape[1])]

    rejected[table_name] = 0

    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"{table_name}:", len(df))


# -------------------------------
# MAIN
# -------------------------------
def main():
    conn = sqlite3.connect(DB_PATH)
    rejected = {}

    conn.execute("PRAGMA foreign_keys = ON")

    with open("db/schema.sql", "r") as f:
        conn.executescript(f.read())

    print("\nLoading Data...\n")

    load_companies(conn, rejected)
    load_profitandloss(conn, rejected)
    load_balancesheet(conn, rejected)
    load_cashflow(conn, rejected)

    load_simple(conn, "data/main/analysis.xlsx", "analysis", rejected)
    load_simple(conn, "data/main/documents.xlsx", "documents", rejected)
    load_simple(conn, "data/main/prosandcons.xlsx", "prosandcons", rejected)

    load_simple(conn, "data/supporting/stock_prices.xlsx", "stock_prices", rejected)
    load_simple(conn, "data/supporting/sectors.xlsx", "sectors", rejected)
    load_simple(conn, "data/supporting/peer_groups.xlsx", "peer_groups", rejected)
    load_simple(conn, "data/supporting/market_cap.xlsx", "market_cap", rejected)

    write_audit(conn, rejected)
    write_validation(conn)

    from src.analytics.engine import run_ratio_engine
    run_ratio_engine(conn)

    print("\nALL DATA LOADED SUCCESSFULLY")
    conn.close()


if __name__ == "__main__":
    main()