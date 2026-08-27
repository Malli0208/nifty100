from src.analytics.ratios import *

def test_net_profit_margin():
    assert net_profit_margin(100, 1000) == 10

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None

def test_roe_normal():
    assert round(return_on_equity(100, 200, 300), 2) == 20.00

def test_roe_negative_equity():
    assert return_on_equity(100, -500, 100) is None

def test_roce():
    val = return_on_capital_employed(200, 300, 200, 100)
    assert round(val, 2) == 33.33

def test_roa():
    assert round(return_on_assets(100, 500), 2) == 20.00

def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None

def test_opm_cross_check():
    assert is_opm_mismatch(20, 18) is True