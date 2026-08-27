# ==============================
# CAGR ENGINE
# ==============================

def calculate_cagr(start_value, end_value, years):
    """
    CAGR = ((end/start)^(1/n) - 1) * 100
    Returns (value, flag)
    """

    # --------------------------
    # EDGE CASES
    # --------------------------

    # insufficient data
    if years is None or years <= 0:
        return None, "INSUFFICIENT"

    # zero base
    if start_value == 0:
        return None, "ZERO_BASE"

    # both negative
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    # decline to loss
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # turnaround
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # final guard (cleaner than "INVALID")
    if start_value <= 0 or end_value <= 0:
        return None, "INVALID"

    # --------------------------
    # NORMAL CASE
    # --------------------------
    try:
        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
        return cagr, None
    except Exception:
        return None, "ERROR"


# ==============================
# SERIES HELPER
# ==============================

def compute_cagr_series(values, years):
    """
    values = list of yearly values (oldest → latest)
    """

    if values is None or len(values) == 0:
        return None, "INSUFFICIENT"

    if len(values) < years + 1:
        return None, "INSUFFICIENT"

    start = values[-(years + 1)]
    end = values[-1]

    return calculate_cagr(start, end, years)