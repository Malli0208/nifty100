import pandas as pd
import yaml
import os
import sqlite3


# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "nifty100.db")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "screener_config.yaml")


# -------------------------
# LOAD CONFIG
# -------------------------
def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)["filters"]


# -------------------------
# LOAD DATA
# -------------------------
def load_data(conn):
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)

    # 🔥 CRITICAL FIX → handle NULLs (this was killing your data)
    df = df.fillna(0)

    return df


# -------------------------
# APPLY FILTERS
# -------------------------
def apply_filters(df, config):

    # --- FIX interest_coverage ---
    if "interest_coverage" in df.columns:
        df["interest_coverage"] = df["interest_coverage"].replace("Debt Free", float("inf"))
        df["interest_coverage"] = pd.to_numeric(df["interest_coverage"], errors="coerce").fillna(0)

    # --- Skip Financials for D/E ---
    if "sector" in df.columns:
        df = df[
            ~(
                (df["sector"] == "Financials") &
                (df["debt_to_equity"] > config.get("de_max", float("inf")))
            )
        ]

    # --- FILTERS (safe with fillna already done) ---
    if "roe_min" in config:
        df = df[df["return_on_equity_pct"] >= config["roe_min"]]

    if "de_max" in config:
        df = df[df["debt_to_equity"] <= config["de_max"]]

    if "fcf_min" in config:
        df = df[df["free_cash_flow"] >= config["fcf_min"]]

    if "revenue_cagr_5yr_min" in config:
        df = df[df["revenue_cagr_5yr"] >= config["revenue_cagr_5yr_min"]]

    if "pat_cagr_5yr_min" in config:
        df = df[df["pat_cagr_5yr"] >= config["pat_cagr_5yr_min"]]

    if "eps_cagr_5yr_min" in config:
        df = df[df["eps_cagr_5yr"] >= config["eps_cagr_5yr_min"]]

    if "asset_turnover_min" in config:
        df = df[df["asset_turnover"] >= config["asset_turnover_min"]]

    if "interest_coverage_min" in config:
        df = df[df["interest_coverage"] >= config["interest_coverage_min"]]

    return df


# -------------------------
# MAIN ENGINE
# -------------------------
def run_screener():

    print("Running Screener Engine...")

    conn = sqlite3.connect(DB_PATH)

    config = load_config()
    df = load_data(conn)
    df = apply_filters(df, config)

    # --- SORT ---
    if "composite_quality_score" in df.columns:
        df = df.sort_values(by="composite_quality_score", ascending=False)

    # Keep only latest year per company
    df = df.sort_values("year", ascending=False)
    df = df.drop_duplicates(subset=["symbol"], keep="first")
    
    print(f"Filtered companies: {len(df)}")

    return df.reset_index(drop=True)


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":

    result = run_screener()

    print(result.head())