from src.analytics.cashflow_kpis import *

def test_fcf():
    assert free_cash_flow(100, -50) == 50

def test_cfo_quality_high():
    val, label = cfo_quality_score([100, 120], [80, 100])
    assert label == "HIGH_QUALITY"

def test_cfo_quality_none():
    val, label = cfo_quality_score([100], [0])
    assert val is None

def test_capex_intensity():
    val, label = capex_intensity(-50, 1000)
    assert label == "MODERATE"

def test_fcf_conversion():
    assert fcf_conversion(50, 100) == 50

def test_fcf_conversion_zero():
    assert fcf_conversion(50, 0) is None

def test_pattern_reinvestor():
    assert capital_allocation_pattern(100, -50, -30) == "REINVESTOR"

def test_pattern_shareholder():
    assert capital_allocation_pattern(100, -50, -30, 1.2) == "SHAREHOLDER_RETURNS"

def test_pattern_distress():
    assert capital_allocation_pattern(-100, 50, 50) == "DISTRESS"

def test_pattern_growth_debt():
    assert capital_allocation_pattern(-100, -50, 100) == "GROWTH_DEBT_FUNDED"