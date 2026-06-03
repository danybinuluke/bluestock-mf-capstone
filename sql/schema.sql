-- Dimension Table: dim_fund
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount INTEGER,
    min_lumpsum_amount INTEGER,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- Dimension Table: dim_date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id TEXT PRIMARY KEY, -- YYYY-MM-DD format
    year INTEGER,
    month INTEGER,
    day INTEGER,
    quarter INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

-- Fact Table: fact_nav
CREATE TABLE IF NOT EXISTS fact_nav (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date TEXT,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date) REFERENCES dim_date(date_id)
);
CREATE INDEX idx_fact_nav_amfi_code ON fact_nav(amfi_code);
CREATE INDEX idx_fact_nav_date ON fact_nav(date);

-- Fact Table: fact_transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    transaction_date TEXT,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount_inr INTEGER,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date_id)
);
CREATE INDEX idx_fact_trans_amfi_code ON fact_transactions(amfi_code);
CREATE INDEX idx_fact_trans_date ON fact_transactions(transaction_date);

-- Fact Table: fact_performance
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    plan TEXT,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore INTEGER,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,
    anomaly_flag BOOLEAN,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact Table: fact_aum
CREATE TABLE IF NOT EXISTS fact_aum (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    fund_house TEXT,
    aum_lakh_crore REAL,
    aum_crore INTEGER,
    num_schemes INTEGER,
    FOREIGN KEY (date) REFERENCES dim_date(date_id)
);
CREATE INDEX idx_fact_aum_date ON fact_aum(date);
CREATE INDEX idx_fact_aum_fund_house ON fact_aum(fund_house);
