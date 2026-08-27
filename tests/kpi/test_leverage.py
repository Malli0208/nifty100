from src.analytics.ratios import *

def test_debt_to_equity_normal():
    assert debt_to_equity(100, 200, 300) == 100 / 500

def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 200, 300) == 0

def test_debt_to_equity_negative_equity():
    assert debt_to_equity(100, -500, 100) is None

def test_high_leverage_flag():
    assert high_leverage_flag(6, "Industrials") is True

def test_high_leverage_financials():
    assert high_leverage_flag(10, "Financials") is False

def test_icr_normal():
    assert interest_coverage_ratio(100, 20, 10) == 12

def test_icr_zero_interest():
    assert interest_coverage_ratio(100, 20, 0) is None

def test_icr_label():
    assert icr_label(None) == "Debt Free"

def test_icr_risk():
    assert icr_risk_flag(1.2) is True

def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2