# ==============================
# CASH FLOW KPIs
# ==============================

def free_cash_flow(cfo, cfi):
    if cfo is None or cfi is None:
        return None
    return cfo + cfi


# ------------------------------
# CFO QUALITY SCORE
# ------------------------------

def cfo_quality_score(cfo_list, pat_list):
    """
    Avg(CFO / PAT) over years
    """

    if cfo_list is None or pat_list is None:
        return None, None

    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):
        if pat == 0 or pat is None or cfo is None:
            continue
        ratios.append(cfo / pat)

    if len(ratios) == 0:
        return None, None

    avg = sum(ratios) / len(ratios)

    if avg > 1:
        return avg, "HIGH_QUALITY"
    elif avg >= 0.5:
        return avg, "MODERATE"
    else:
        return avg, "ACCRUAL_RISK"


# ------------------------------
# CAPEX INTENSITY
# ------------------------------

def capex_intensity(cfi, sales):
    """
    CapEx = abs(investing CF) / sales * 100
    """
    if sales == 0 or sales is None or cfi is None:
        return None, None

    val = abs(cfi) / sales * 100

    if val < 3:
        return val, "ASSET_LIGHT"
    elif val <= 8:
        return val, "MODERATE"
    else:
        return val, "Capital Intensive"


# ------------------------------
# FCF CONVERSION
# ------------------------------

def fcf_conversion(fcf, operating_profit):
    if operating_profit == 0 or operating_profit is None or fcf is None:
        return None

    return (fcf / operating_profit) * 100


# ==============================
# CAPITAL ALLOCATION PATTERN
# ==============================

def sign(x):
    if x is None:
        return "0"
    if x > 0:
        return "+"
    elif x < 0:
        return "-"
    else:
        return "0"


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Classify company behavior based on CF patterns
    """

    s = (sign(cfo), sign(cfi), sign(cff))

    if s == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            return "SHAREHOLDER_RETURNS"
        return "REINVESTOR"

    elif s == ("+", "+", "-"):
        return "LIQUIDATING_ASSETS"

    elif s == ("-", "+", "+"):
        return "DISTRESS"

    elif s == ("-", "-", "+"):
        return "GROWTH_DEBT_FUNDED"

    elif s == ("+", "+", "+"):
        return "CASH_ACCUMULATOR"

    elif s == ("-", "-", "-"):
        return "PRE_REVENUE"

    elif s == ("+", "-", "+"):
        return "MIXED"

    return "UNKNOWN"