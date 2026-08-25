import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.etl.loader import normalize_year, normalize_ticker

def test_year():
    assert normalize_year("FY2020") == 2020
    assert normalize_year("2022") == 2022

def test_ticker():
    assert normalize_ticker(" infy ") == "INFY"
    assert normalize_ticker("tcs") == "TCS"