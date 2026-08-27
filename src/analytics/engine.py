import pandas as pd
from src.analytics.ratios import *
from src.analytics.cashflow_kpis import *
from src.analytics.cagr import compute_cagr_series


# -------------------------
# HELPERS
# -------------------------

def safe_sign_label(x):
    if pd.isna(x):
        return "ZERO"
    return "POS" if x > 0 else ("NEG" if x < 0 else "ZERO")


def classify_issue(calc, src):
    if pd.isnull(src):
        return "NO_SOURCE"

    if src == 0:
        return "DATA_SOURCE_ISSUE"

    try:
        if abs(calc - src) > 20:
            return "FORMULA_DISCREPANCY"
    except:
        return "INVALID_COMPARISON"

    return "MINOR_VARIANCE"


# -------------------------
# SCORING
# -------------------------

def score_roe(roe):
    if roe is None:
        return 0
    if roe > 20:
        return 10
    elif roe > 15:
        return 8
    elif roe > 10:
        return 5
    else:
        return 2


def score_leverage(de):
    if de is None:
        return 0
    if de < 0.5:
        return 10
    elif de < 1:
        return 8
    elif de < 2:
        return 5
    else:
        return 2


def score_cfo(label):
    if label == "HIGH_QUALITY":
        return 10
    elif label == "MODERATE":
        return 6
    else:
        return 2


def rating(score):
    if score >= 20:
        return "COMPOUNDER"
    elif score >= 15:
        return "GOOD"
    elif score >= 10:
        return "AVERAGE"
    else:
        return "WEAK"


# -------------------------
# MAIN ENGINE
# -------------------------

def run_ratio_engine(conn):

    print("Running Ratio Engine...")

    pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
    bs = pd.read_sql("SELECT * FROM balancesheet", conn)
    cf = pd.read_sql("SELECT * FROM cashflow", conn)
    companies = pd.read_sql("SELECT * FROM companies", conn)

    # Excel reference
    companies_excel = pd.read_excel("data/main/companies.xlsx", skiprows=1)
    companies_excel = companies_excel.drop_duplicates("company_name")

    excel_lookup = companies_excel.set_index("company_name")[
        ["roe_percentage", "roce_percentage"]
    ]

    # -------------------------
    # MERGE
    # -------------------------
    df = pnl.merge(bs, on=["symbol", "year"], how="inner")
    df = df.merge(cf, on=["symbol", "year"], how="left")
    df = df.merge(companies[['symbol', 'company_name', 'sector']], on="symbol", how="left")

    df = df.sort_values(["symbol", "year"])

    results = []
    log_lines = []
    capital_alloc_rows = []

    for symbol, group in df.groupby("symbol"):

        group = group.sort_values("year")

        # CLEAN SERIES (remove NaN)
        sales_series = [x for x in group["sales"].tolist() if pd.notnull(x)]
        pat_series   = [x for x in group["net_profit"].tolist() if pd.notnull(x)]
        eps_series   = [x for x in group["eps"].tolist() if pd.notnull(x)]
        cfo_series   = [x for x in group["operating_cf"].tolist() if pd.notnull(x)]

        # CAGR
        rev_cagr_5, rev_flag = compute_cagr_series(sales_series, 5)
        pat_cagr_5, pat_flag = compute_cagr_series(pat_series, 5)
        eps_cagr_5, eps_flag = compute_cagr_series(eps_series, 5)

        # CFO Quality
        cfo_window = cfo_series[-5:] if len(cfo_series) >= 5 else cfo_series
        pat_window = pat_series[-5:] if len(pat_series) >= 5 else pat_series

        cfo_quality_val, cfo_quality_label = cfo_quality_score(cfo_window, pat_window)

        for _, row in group.iterrows():

            sector = row["sector"] if pd.notnull(row["sector"]) else None

            # PROFITABILITY
            npm = net_profit_margin(row["net_profit"], row["sales"])
            opm = operating_profit_margin(row["operating_profit"], row["sales"])

            roe = return_on_equity(
                row.get("net_profit"),
                row.get("equity"),
                row.get("reserves")
            )
            roce = return_on_capital_employed(row["operating_profit"], row["equity"], row["reserves"], row["debt"])
            roa = return_on_assets(row["net_profit"], row["assets"])

            # LEVERAGE
            de = debt_to_equity(row["debt"], row["equity"], row["reserves"])
            hl_flag = high_leverage_flag(de, sector)

            bvps = book_value_per_share(
                row.get("equity"),
                row.get("reserves"),
                row.get("shares_outstanding")  # check existence
            )

            div_payout = dividend_payout_ratio(
                row.get("dividend"),
                row.get("net_profit")
            )

            # ICR SAFE
            if "interest" in row.index and "other_income" in row.index:
                if pd.notnull(row["interest"]) and pd.notnull(row["other_income"]):
                    icr = interest_coverage(row["operating_profit"], row["other_income"], row["interest"])
                    icr_lbl = icr_label(icr)
                else:
                    icr = None
                    icr_lbl = "Debt Free"
            else:
                icr = None
                icr_lbl = "Debt Free"

            asset_turn = asset_turnover(row["sales"], row["assets"])

            # CASHFLOW
            fcf = free_cash_flow(row["operating_cf"], row["investing_cf"])
            capex_val, capex_label = capex_intensity(row["investing_cf"], row["sales"])
            fcf_conv = fcf_conversion(fcf, row["operating_profit"])

            pattern = capital_allocation_pattern(
                row["operating_cf"],
                row["investing_cf"],
                row["financing_cf"],
                cfo_quality_val
            )

            capital_alloc_rows.append({
                "company_id": row["symbol"],
                "year": row["year"],
                "cfo_sign": safe_sign_label(row["operating_cf"]),
                "cfi_sign": safe_sign_label(row["investing_cf"]),
                "cff_sign": safe_sign_label(row["financing_cf"]),
                "pattern_label": pattern
            })

            # LOGGING
            company_name = row["company_name"]

            src_roe = None
            src_roce = None
            bvps = None
            div_payout = None

            if company_name in excel_lookup.index:
                src_roe = excel_lookup.loc[company_name, "roe_percentage"]
                src_roce = excel_lookup.loc[company_name, "roce_percentage"]

            if pd.notnull(src_roe) and roe is not None:
                if abs(roe - src_roe) > 5:
                    issue = classify_issue(roe, src_roe)
                    log_lines.append(f"{row['symbol']} {row['year']} ROE | calc={roe:.2f} src={src_roe} | {issue}")

            if pd.notnull(src_roce) and roce is not None:
                if abs(roce - src_roce) > 5:
                    issue = classify_issue(roce, src_roce)
                    log_lines.append(f"{row['symbol']} {row['year']} ROCE | calc={roce:.2f} src={src_roce} | {issue}")

            # SCORING
            roe_score = score_roe(roe)
            leverage_score = score_leverage(de)
            cfo_score = score_cfo(cfo_quality_label)

            total_score = round((roe_score * 0.5 + leverage_score * 0.3 + cfo_score * 0.2) * 2)
            rating_label = rating(total_score)

            results.append({
                "symbol": row["symbol"],
                "year": row["year"],

                "net_profit_margin_pct": npm,
                "operating_profit_margin_pct": opm,
                "return_on_equity_pct": roe,
                "return_on_capital_employed_pct": roce,
                "return_on_assets_pct": roa,

                "debt_to_equity": de,
                "high_leverage_flag": hl_flag,
                "interest_coverage": icr,
                "icr_label": icr_lbl,
                "asset_turnover": asset_turn,

                "free_cash_flow": fcf,
                "fcf_conversion_pct": fcf_conv,
                "capex_intensity_pct": capex_val,
                "capex_label": capex_label,
                "capital_allocation": pattern,
                "cfo_quality_label": cfo_quality_label,

                "revenue_cagr_5yr": rev_cagr_5,
                "revenue_cagr_flag": rev_flag,
                "pat_cagr_5yr": pat_cagr_5,
                "pat_cagr_flag": pat_flag,
                "eps_cagr_5yr": eps_cagr_5,
                "eps_cagr_flag": eps_flag,

                "roe_score": roe_score,
                "leverage_score": leverage_score,
                "cfo_score": cfo_score,
                "composite_quality_score": total_score,
                "rating": rating_label,
                "book_value_per_share": bvps,
                "dividend_payout_ratio_pct": div_payout,
            })

    # SAVE
    pd.DataFrame(results).to_sql("financial_ratios", conn, if_exists="replace", index=False)

    with open("output/ratio_edge_cases.log", "w") as f:
        f.write("\n".join(log_lines))

    pd.DataFrame(capital_alloc_rows).to_csv("output/capital_allocation.csv", index=False)

    print("financial_ratios rows:", len(results))
    print("log entries:", len(log_lines))
    print("capital_allocation.csv created")