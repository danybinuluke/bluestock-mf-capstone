# Day 2 Data Assessment Report

## 01_fund_master.csv
**Row Count:** 40
**Columns & Datatypes:**
- `amfi_code`: int64
- `fund_house`: str
- `scheme_name`: str
- `category`: str
- `sub_category`: str
- `plan`: str
- `launch_date`: str
- `benchmark`: str
- `expense_ratio_pct`: float64
- `exit_load_pct`: float64
- `min_sip_amount`: int64
- `min_lumpsum_amount`: int64
- `fund_manager`: str
- `risk_category`: str
- `sebi_category_code`: str
**Potential Date Columns:** launch_date
**Potential Key Columns (PK/FK):** amfi_code, sebi_category_code

## 02_nav_history.csv
**Row Count:** 46000
**Columns & Datatypes:**
- `amfi_code`: int64
- `date`: str
- `nav`: float64
**Potential Date Columns:** date
**Potential Key Columns (PK/FK):** amfi_code

## 03_aum_by_fund_house.csv
**Row Count:** 90
**Columns & Datatypes:**
- `date`: str
- `fund_house`: str
- `aum_lakh_crore`: float64
- `aum_crore`: int64
- `num_schemes`: int64
**Potential Date Columns:** date

## 04_monthly_sip_inflows.csv
**Row Count:** 48
**Columns & Datatypes:**
- `month`: str
- `sip_inflow_crore`: int64
- `active_sip_accounts_crore`: float64
- `new_sip_accounts_lakh`: float64
- `sip_aum_lakh_crore`: float64
- `yoy_growth_pct`: float64
**Missing Values:**
- `yoy_growth_pct`: 12 missing
**Potential Date Columns:** month

## 05_category_inflows.csv
**Row Count:** 144
**Columns & Datatypes:**
- `month`: str
- `category`: str
- `net_inflow_crore`: float64
**Potential Date Columns:** month

## 06_industry_folio_count.csv
**Row Count:** 21
**Columns & Datatypes:**
- `month`: str
- `total_folios_crore`: float64
- `equity_folios_crore`: float64
- `debt_folios_crore`: float64
- `hybrid_folios_crore`: float64
- `others_folios_crore`: float64
**Potential Date Columns:** month
**Potential Key Columns (PK/FK):** hybrid_folios_crore

## 07_scheme_performance.csv
**Row Count:** 40
**Columns & Datatypes:**
- `amfi_code`: int64
- `scheme_name`: str
- `fund_house`: str
- `category`: str
- `plan`: str
- `return_1yr_pct`: float64
- `return_3yr_pct`: float64
- `return_5yr_pct`: float64
- `benchmark_3yr_pct`: float64
- `alpha`: float64
- `beta`: float64
- `sharpe_ratio`: float64
- `sortino_ratio`: float64
- `std_dev_ann_pct`: float64
- `max_drawdown_pct`: float64
- `aum_crore`: int64
- `expense_ratio_pct`: float64
- `morningstar_rating`: int64
- `risk_grade`: str
**Potential Key Columns (PK/FK):** amfi_code

## 08_investor_transactions.csv
**Row Count:** 32778
**Columns & Datatypes:**
- `investor_id`: str
- `transaction_date`: str
- `amfi_code`: int64
- `transaction_type`: str
- `amount_inr`: int64
- `state`: str
- `city`: str
- `city_tier`: str
- `age_group`: str
- `gender`: str
- `annual_income_lakh`: float64
- `payment_mode`: str
- `kyc_status`: str
**Potential Date Columns:** transaction_date
**Potential Key Columns (PK/FK):** investor_id, amfi_code

## 09_portfolio_holdings.csv
**Row Count:** 322
**Columns & Datatypes:**
- `amfi_code`: int64
- `stock_symbol`: str
- `stock_name`: str
- `sector`: str
- `weight_pct`: float64
- `market_value_cr`: float64
- `current_price_inr`: float64
- `portfolio_date`: str
**Potential Date Columns:** portfolio_date
**Potential Key Columns (PK/FK):** amfi_code

## 10_benchmark_indices.csv
**Row Count:** 8050
**Columns & Datatypes:**
- `date`: str
- `index_name`: str
- `close_value`: float64
**Potential Date Columns:** date
