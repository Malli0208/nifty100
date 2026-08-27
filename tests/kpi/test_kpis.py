import pytest

from src.analytics.ratios import *
from src.analytics.cashflow_kpis import *
from src.analytics.cagr import compute_cagr_series


# -------------------------
# DAY 08 — PROFITABILITY (8 TESTS)
# -------------------------

def test_npm_normal():
    assert net_profit_margin(100, 1000) == 10


def test_npm_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_opm_normal():
    assert operating_profit_margin(200, 1000) == 20


def test_roe_normal():
    assert return_on_equity(100, 200, 300) == 20  # 100 / 500 * 100


def test_roe_negative_equity():
    assert return_on_equity(100, -200, -300) is None


def test_roce_normal():
    assert return_on_capital_employed(100, 200, 300, 500) == 10  # 100 / 1000 * 100


def test_roa_normal():
    assert return_on_assets(100, 1000) == 10


def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None


# -------------------------
# DAY 09 — LEVERAGE (8 TESTS)
# -------------------------

def test_debt_to_equity_normal():
    assert debt_to_equity(200, 200, 300) == 0.4  # 200 / 500


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 200, 300) == 0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(100, -200, -300) is None


def test_high_leverage_flag_true():
    assert high_leverage_flag(6, "Industrials") is True


def test_high_leverage_flag_financials():
    assert high_leverage_flag(6, "Financials") is False


def test_interest_coverage_normal():
    assert interest_coverage(200, 50, 50) == 5  # (200+50)/50


def test_interest_coverage_zero_interest():
    assert interest_coverage(200, 50, 0) is None


def test_asset_turnover_normal():
    assert asset_turnover(1000, 500) == 2


# -------------------------
# DAY 10 — CAGR (4 TESTS)
# -------------------------

def test_cagr_normal():
    val, flag = compute_cagr_series([100, 200], 1)
    assert round(val, 2) == 100
    assert flag is None


def test_cagr_turnaround():
    val, flag = compute_cagr_series([-100, 200], 1)
    assert val is None
    assert flag == "TURNAROUND"


def test_cagr_decline_to_loss():
    val, flag = compute_cagr_series([100, -200], 1)
    assert val is None
    assert flag == "DECLINE_TO_LOSS"


def test_cagr_zero_base():
    val, flag = compute_cagr_series([0, 200], 1)
    assert val is None
    assert flag == "ZERO_BASE"


# -------------------------
# DAY 11 — CASHFLOW (4 TESTS)
# -------------------------

def test_free_cash_flow():
    assert free_cash_flow(100, -50) == 50


def test_cfo_quality_high():
    val, label = cfo_quality_score([100, 120, 110, 130, 140], [80, 100, 90, 100, 100])
    assert label == "HIGH_QUALITY"


def test_capex_intensity():
    val, label = capex_intensity(-100, 1000)
    assert round(val, 2) == 10
    assert label == "Capital Intensive"


def test_fcf_conversion_zero_op():
    assert fcf_conversion(100, 0) is None