-- ========================
-- CRITICAL RULES
-- ========================

-- DQ-01: PK uniqueness companies
SELECT symbol, COUNT(*) 
FROM companies 
GROUP BY symbol 
HAVING COUNT(*) > 1;

-- DQ-02: (symbol, year) uniqueness
SELECT symbol, year, COUNT(*) 
FROM profitandloss 
GROUP BY symbol, year 
HAVING COUNT(*) > 1;

-- DQ-03: FK integrity
SELECT symbol 
FROM profitandloss 
WHERE symbol NOT IN (SELECT symbol FROM companies);


-- ========================
-- WARNING RULES
-- ========================

-- DQ-04: Balance check
SELECT * 
FROM balancesheet 
WHERE ABS(assets - (liabilities + equity)) > 1;

-- DQ-05: OPM sanity
SELECT * 
FROM profitandloss 
WHERE operating_profit > sales * 2;

-- DQ-06: Negative sales
SELECT * 
FROM profitandloss 
WHERE sales < 0;

-- DQ-07: Negative assets
SELECT * 
FROM balancesheet 
WHERE assets < 0;

-- DQ-08: Negative debt
SELECT * 
FROM balancesheet 
WHERE debt < 0;

-- DQ-09: Net cash mismatch
SELECT * 
FROM cashflow 
WHERE net_cash != (operating_cf + investing_cf + financing_cf);

-- DQ-10: EPS null
SELECT * 
FROM profitandloss 
WHERE eps IS NULL;


-- ========================
-- ADDITIONAL RULES (11–16)
-- ========================

-- DQ-11: Year null
SELECT * 
FROM profitandloss 
WHERE year IS NULL;

-- DQ-12: Company name null
SELECT * 
FROM companies 
WHERE company_name IS NULL;

-- DQ-13: Zero sales
SELECT * 
FROM profitandloss 
WHERE sales = 0;

-- DQ-14: Negative equity
SELECT * 
FROM balancesheet 
WHERE equity < 0;

-- DQ-15: Duplicate stock price keys
SELECT col0, COUNT(*) 
FROM stock_prices 
GROUP BY col0 
HAVING COUNT(*) > 1;

-- DQ-16: Missing sector
SELECT * 
FROM companies 
WHERE sector IS NULL;