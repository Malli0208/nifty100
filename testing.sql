-- =====================================================
-- MASTER SQL VALIDATION SCRIPT
-- Purpose: Run all queries for validation & analysis
-- NOTE: Duplicates removed, logically grouped
-- =====================================================


-- ==============================
-- 1. BASIC TABLE CHECKS
-- ==============================

SELECT COUNT(*) FROM companies;

PRAGMA foreign_key_check;

.read db/schema.sql;

.tables;


-- ==============================
-- 2. RAW DATA VALIDATION
-- ==============================

SELECT * FROM profitandloss LIMIT 5;
SELECT * FROM balancesheet LIMIT 10;
SELECT * FROM cashflow LIMIT 1;

SELECT * FROM profitandloss WHERE symbol = 'TCS';
SELECT * FROM profitandloss WHERE symbol = 'RELIANCE';
SELECT * FROM balancesheet WHERE symbol = 'HDFCBANK';


-- ==============================
-- 3. TABLE STRUCTURE CHECK
-- ==============================

PRAGMA table_info(financial_ratios);
PRAGMA table_info(profitandloss);
PRAGMA table_info(balancesheet);


-- ==============================
-- 4. FINANCIAL RATIOS BASIC CHECK
-- ==============================

SELECT COUNT(*) FROM financial_ratios;

SELECT COUNT(DISTINCT symbol) FROM financial_ratios;

SELECT * FROM financial_ratios LIMIT 5;


-- ==============================
-- 5. KPI FIELD VALIDATION
-- ==============================

SELECT interest_coverage FROM financial_ratios LIMIT 5;

SELECT 
    revenue_cagr_5yr,
    cfo_quality_label,
    capital_allocation
FROM financial_ratios
LIMIT 5;

SELECT symbol, return_on_equity_pct FROM financial_ratios LIMIT 10;
SELECT symbol, debt_to_equity FROM financial_ratios LIMIT 10;


-- ==============================
-- 6. LEVERAGE ANALYSIS
-- ==============================

SELECT symbol, debt_to_equity, high_leverage_flag
FROM financial_ratios
LIMIT 10;

SELECT symbol, sector, debt_to_equity, high_leverage_flag
FROM financial_ratios
WHERE debt_to_equity > 5
LIMIT 10;

SELECT COUNT(*) 
FROM financial_ratios
WHERE debt_to_equity < 2;

SELECT COUNT(*) 
FROM financial_ratios
WHERE debt_to_equity < 1;


-- ==============================
-- 7. ROE ANALYSIS
-- ==============================

SELECT 
  MIN(return_on_equity_pct),
  MAX(return_on_equity_pct)
FROM financial_ratios;

SELECT 
  COUNT(*) as total,
  COUNT(CASE WHEN return_on_equity_pct IS NULL THEN 1 END) as null_roe,
  COUNT(CASE WHEN return_on_equity_pct > 15 THEN 1 END) as good_roe
FROM financial_ratios;

SELECT COUNT(*) 
FROM financial_ratios 
WHERE return_on_equity_pct > 15;


-- ==============================
-- 8. FILTERED STOCK SCREENS
-- ==============================

SELECT symbol, return_on_equity_pct, debt_to_equity, composite_quality_score, rating
FROM financial_ratios
WHERE return_on_equity_pct > 15
AND debt_to_equity < 2
ORDER BY composite_quality_score DESC
LIMIT 20;

SELECT symbol, return_on_equity_pct, debt_to_equity, composite_quality_score, rating
FROM financial_ratios
WHERE return_on_equity_pct > 12
AND debt_to_equity < 3
ORDER BY composite_quality_score DESC
LIMIT 20;

SELECT symbol, return_on_equity_pct, debt_to_equity, composite_quality_score, rating
FROM financial_ratios
WHERE return_on_equity_pct > 10
AND debt_to_equity < 4
ORDER BY composite_quality_score DESC
LIMIT 20;


-- ==============================
-- 9. LATEST YEAR FILTER
-- ==============================

SELECT *
FROM financial_ratios f
WHERE year = (
    SELECT MAX(f2.year)
    FROM financial_ratios f2
    WHERE f2.symbol = f.symbol
)
AND return_on_equity_pct > 10
AND debt_to_equity < 2
ORDER BY composite_quality_score DESC;


-- ==============================
-- 10. DATA QUALITY CHECKS
-- ==============================

SELECT COUNT(*) 
FROM financial_ratios 
WHERE return_on_equity_pct IS NULL;

SELECT MIN(debt_to_equity), MAX(debt_to_equity)
FROM financial_ratios;

SELECT 
  COUNT(CASE WHEN debt_to_equity < 1 THEN 1 END) as low_de,
  COUNT(CASE WHEN debt_to_equity < 2 THEN 1 END) as below_2,
  COUNT(*) as total
FROM financial_ratios;


-- ==============================
-- 11. EXTREME VALUE CHECKS
-- ==============================

SELECT symbol, year, return_on_assets_pct
FROM financial_ratios
WHERE return_on_assets_pct > 100;

SELECT symbol, year, net_profit, assets
FROM financial_ratios
WHERE return_on_assets_pct > 500;


-- ==============================
-- 12. JOIN VALIDATION
-- ==============================

SELECT f.symbol, f.year,
       f.debt_to_equity,
       b.debt, b.equity, b.reserves
FROM financial_ratios f
JOIN balancesheet b
ON f.symbol = b.symbol AND f.year = b.year
LIMIT 10;

SELECT f.symbol, f.year, f.debt_to_equity,
       b.debt, b.equity, b.reserves
FROM financial_ratios f
JOIN balancesheet b
ON f.symbol = b.symbol AND f.year = b.year
ORDER BY f.debt_to_equity DESC
LIMIT 5;


-- ==============================
-- 13. DATA CONSISTENCY CHECK
-- ==============================

SELECT p.symbol, p.year
FROM profitandloss p
LEFT JOIN balancesheet b
ON p.symbol = b.symbol AND p.year = b.year
WHERE b.symbol IS NULL;


-- ==============================
-- 14. CAGR DATA CHECK
-- ==============================

SELECT COUNT(*)
FROM financial_ratios
WHERE revenue_cagr_5yr IS NOT NULL;

SELECT symbol, revenue_cagr_5yr, revenue_cagr_flag
FROM financial_ratios
LIMIT 10;


-- ==============================
-- 15. LOG CHECK
-- ==============================

SELECT * FROM output/ratio_edge_cases.log;


-- ==============================
-- 16. SCORING & RANKING
-- ==============================

SELECT symbol, composite_quality_score, rating
FROM financial_ratios
ORDER BY composite_quality_score DESC
LIMIT 10;


-- ==============================
-- 17. BOOK VALUE & DIVIDEND CHECK
-- ==============================

SELECT 
COUNT(book_value_per_share),
COUNT(dividend_payout_ratio_pct)
FROM financial_ratios;


-- ==============================
-- 18. LOW DATA EDGE CASE
-- ==============================

SELECT symbol, year, assets
FROM balancesheet
WHERE assets < 100;


-- ==============================
-- END OF SCRIPT
-- ==============================

.exit;