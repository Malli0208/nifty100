from src.analytics.cagr import *

def test_cagr_normal():
    val, flag = calculate_cagr(100, 200, 5)
    assert round(val, 2) == 14.87
    assert flag is None

def test_cagr_zero_base():
    val, flag = calculate_cagr(0, 200, 5)
    assert val is None
    assert flag == "ZERO_BASE"

def test_cagr_turnaround():
    val, flag = calculate_cagr(-100, 200, 5)
    assert val is None
    assert flag == "TURNAROUND"

def test_cagr_decline_to_loss():
    val, flag = calculate_cagr(100, -200, 5)
    assert val is None
    assert flag == "DECLINE_TO_LOSS"

def test_cagr_both_negative():
    val, flag = calculate_cagr(-100, -200, 5)
    assert val is None
    assert flag == "BOTH_NEGATIVE"

def test_cagr_insufficient():
    val, flag = calculate_cagr(100, 200, 0)
    assert val is None
    assert flag == "INSUFFICIENT"

def test_series_cagr():
    values = [100, 120, 140, 160, 180, 200]
    val, flag = compute_cagr_series(values, 5)
    assert round(val, 2) == 14.87

def test_series_insufficient():
    values = [100, 120]
    val, flag = compute_cagr_series(values, 5)
    assert val is None
    assert flag == "INSUFFICIENT"