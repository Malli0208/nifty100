-- Total companies
SELECT COUNT(*) FROM companies;

-- Top 5 profit companies
SELECT symbol, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC LIMIT 5;

-- Loss companies
SELECT * FROM profitandloss WHERE net_profit < 0;

-- Most data coverage
SELECT symbol, COUNT(*) years
FROM profitandloss GROUP BY symbol
ORDER BY years DESC;

-- Latest year
SELECT symbol, MAX(year) FROM profitandloss GROUP BY symbol;

-- High debt
SELECT symbol, year, debt
FROM balancesheet ORDER BY debt DESC LIMIT 5;

-- Negative cashflow
SELECT * FROM cashflow WHERE net_cash < 0;

-- Price records
SELECT COUNT(*) FROM stock_prices;

-- Duplicate check
SELECT symbol, year, COUNT(*)
FROM profitandloss
GROUP BY symbol, year HAVING COUNT(*) > 1;

-- Profit trend
SELECT year, SUM(net_profit)
FROM profitandloss GROUP BY year;