PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS companies;
CREATE TABLE IF NOT EXISTS companies (
    symbol TEXT PRIMARY KEY,
    company_name TEXT,
    sector TEXT
);

DROP TABLE IF EXISTS profitandloss;
CREATE TABLE profitandloss (
    symbol TEXT,
    raw_year TEXT,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    net_profit REAL,
    eps REAL
);

DROP TABLE IF EXISTS balancesheet;
CREATE TABLE balancesheet (
    symbol TEXT,
    raw_year TEXT,
    assets REAL,
    liabilities REAL,
    equity REAL,
    reserves REAL,
    debt REAL
);

DROP TABLE IF EXISTS cashflow;
CREATE TABLE cashflow (
    symbol TEXT,
    raw_year TEXT,
    operating_cf REAL,
    investing_cf REAL,
    financing_cf REAL,
    net_cash REAL
);

DROP TABLE IF EXISTS analysis;
CREATE TABLE analysis (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT, col4 TEXT, col5 TEXT
);

DROP TABLE IF EXISTS documents;
CREATE TABLE documents (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT
);

DROP TABLE IF EXISTS prosandcons;
CREATE TABLE prosandcons (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT
);

DROP TABLE IF EXISTS financial_ratios;
CREATE TABLE financial_ratios (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT, col4 TEXT,
    col5 TEXT, col6 TEXT, col7 TEXT, col8 TEXT, col9 TEXT,
    col10 TEXT, col11 TEXT, col12 TEXT, col13 TEXT, col14 TEXT, col15 TEXT
);

DROP TABLE IF EXISTS stock_prices;
CREATE TABLE stock_prices (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT, col4 TEXT,
    col5 TEXT, col6 TEXT, col7 TEXT, col8 TEXT
);

DROP TABLE IF EXISTS sectors;
CREATE TABLE sectors (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT, col4 TEXT, col5 TEXT
);

DROP TABLE IF EXISTS peer_groups;
CREATE TABLE peer_groups (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT
);

DROP TABLE IF EXISTS market_cap;
CREATE TABLE market_cap (
    col0 TEXT, col1 TEXT, col2 TEXT, col3 TEXT, col4 TEXT,
    col5 TEXT, col6 TEXT, col7 TEXT, col8 TEXT
);