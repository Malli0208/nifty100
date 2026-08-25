SELECT COUNT(*) FROM companies;
PRAGMA foreign_key_check;

.read db/schema.sql

SELECT * FROM profitandloss WHERE symbol='TCS';
SELECT * FROM profitandloss WHERE symbol='RELIANCE';
SELECT * FROM balancesheet WHERE symbol='HDFCBANK';