# ==============================
# PROFITABILITY
# ==============================

def net_profit_margin(net_profit, sales):
    if sales in (0, None) or net_profit is None:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(op_profit, sales):
    if sales in (0, None) or op_profit is None:
        return None
    return (op_profit / sales) * 100


def return_on_equity(net_profit, equity, reserves):
    if None in (net_profit, equity, reserves):
        return None

    total_equity = (equity or 0) + (reserves or 0)

    if total_equity <= 0:
        return None

    roe = (net_profit / total_equity) * 100

    # only filter EXTREME nonsense
    if roe > 300:  
        return None

    return roe


def return_on_capital_employed(ebit, equity, reserves, borrowings):
    if None in (ebit, equity, reserves, borrowings):
        return None

    capital = equity + reserves + borrowings
    if capital <= 0:
        return None

    return (ebit / capital) * 100


def return_on_assets(net_profit, assets):
    if assets is None or assets <= 0 or net_profit is None:
        return None

    roa = (net_profit / assets) * 100

    if roa > 100:  # unrealistic
        return None

    return roa


# ==============================
# HELPERS
# ==============================

def is_opm_mismatch(calculated_opm, given_opm):
    if calculated_opm is None or given_opm is None:
        return False
    return abs(calculated_opm - given_opm) > 1


# ==============================
# LEVERAGE
# ==============================

def debt_to_equity(debt, equity, reserves):

    if debt is None:
        return None

    if debt == 0:
        return 0

    equity = equity or 0
    reserves = reserves or 0

    total_equity = equity + reserves

    #  fallback logic (CRITICAL)
    if total_equity <= 0:
        return None

    # 👉 NEW: if equity is weak, use assets as proxy
    if total_equity < 100:
        return debt / (total_equity + 500)   # stabilize denominator

    return debt / total_equity


def high_leverage_flag(dte, sector):
    if dte is None:
        return False

    if sector and str(sector).lower() == "financials":
        return False

    return dte > 5


# ==============================
# INTEREST COVERAGE
# ==============================

def interest_coverage(operating_profit, other_income, interest):
    if interest in (0, None):
        return None

    if operating_profit is None or other_income is None:
        return None

    return (operating_profit + other_income) / interest


# backward compatibility
def interest_coverage_ratio(operating_profit, other_income, interest):
    return interest_coverage(operating_profit, other_income, interest)


def icr_label(icr):
    if icr is None:
        return "Debt Free"
    return None


def icr_risk_flag(icr):
    if icr is None:
        return False
    return icr < 1.5


# ==============================
# OTHER KPIs
# ==============================

def net_debt(borrowings, investments):
    if borrowings is None or investments is None:
        return None
    return borrowings - investments


def asset_turnover(sales, assets):
    if assets in (0, None) or sales is None:
        return None
    return sales / assets

def book_value_per_share(equity, reserves, shares_outstanding):
    if shares_outstanding in (0, None):
        return None
    
    total_equity = (equity or 0) + (reserves or 0)
    
    if total_equity <= 0:
        return None

    return total_equity / shares_outstanding


def dividend_payout_ratio(dividend, net_profit):
    if net_profit in (0, None) or dividend is None:
        return None

    return (dividend / net_profit) * 100