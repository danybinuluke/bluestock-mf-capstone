# Bluestock Mutual Fund Analytics Data Dictionary

This document outlines the schema of the SQLite data warehouse (`bluestock_mf.db`) used in this project.

## Dimensions

### `dim_fund`
Source: `01_fund_master.csv`

| Column Name | Datatype | Business Definition | Example Value |
|-------------|----------|----------------------|---------------|
| `amfi_code` | INTEGER (PK) | Unique identifier for the mutual fund assigned by AMFI. | `119551` |
| `fund_house` | TEXT | Name of the Asset Management Company (AMC). | `HDFC Mutual Fund` |
| `scheme_name` | TEXT | Full name of the mutual fund scheme. | `HDFC Flexi Cap Fund` |
| `category` | TEXT | Primary investment category (e.g., Equity, Debt). | `Equity` |
| `sub_category` | TEXT | Specific sub-category within the primary category. | `Flexi Cap` |
| `plan` | TEXT | Investment plan type (Direct/Regular). | `Direct` |
| `launch_date` | DATE | Date the fund was launched. | `2013-01-01` |
| `benchmark` | TEXT | The benchmark index the fund is tracked against. | `NIFTY 500` |
| `expense_ratio_pct` | REAL | The annual maintenance charge levied by mutual funds. | `0.85` |
| `exit_load_pct` | REAL | Fee charged when investors redeem units before a specific period. | `1.0` |
| `min_sip_amount` | INTEGER | Minimum amount required to start a Systematic Investment Plan. | `500` |
| `min_lumpsum_amount`| INTEGER | Minimum amount required for a one-time investment. | `5000` |
| `fund_manager` | TEXT | Name of the manager(s) managing the fund. | `Prashant Jain` |
| `risk_category` | TEXT | Risk classification of the fund. | `Very High` |
| `sebi_category_code` | TEXT | Regulatory category code given by SEBI. | `EQ-FC` |

### `dim_date`
Source: Generated from transactions, NAV history, and fund master dates.

| Column Name | Datatype | Business Definition | Example Value |
|-------------|----------|----------------------|---------------|
| `date_id` | TEXT (PK) | Date in YYYY-MM-DD format. | `2023-10-15` |
| `year` | INTEGER | Year of the date. | `2023` |
| `month` | INTEGER | Month of the date (1-12). | `10` |
| `day` | INTEGER | Day of the month. | `15` |
| `quarter` | INTEGER | Quarter of the year (1-4). | `4` |
| `day_of_week` | INTEGER | Day of the week (0=Monday, 6=Sunday). | `6` |
| `is_weekend` | BOOLEAN | Flag indicating if the date falls on a weekend. | `1` |

## Facts

### `fact_nav`
Source: `02_nav_history.csv`

| Column Name | Datatype | Business Definition | Example Value |
|-------------|----------|----------------------|---------------|
| `id` | INTEGER (PK) | Auto-incrementing primary key. | `1` |
| `amfi_code` | INTEGER (FK) | Reference to `dim_fund`. | `119551` |
| `date` | TEXT (FK) | Reference to `dim_date`. | `2023-10-15` |
| `nav` | REAL | Net Asset Value per unit on the given date. | `145.67` |

### `fact_transactions`
Source: `08_investor_transactions.csv`

| Column Name | Datatype | Business Definition | Example Value |
|-------------|----------|----------------------|---------------|
| `transaction_id`| INTEGER (PK) | Auto-incrementing primary key. | `1` |
| `investor_id` | TEXT | Unique identifier for the investor. | `INV12345` |
| `transaction_date`| TEXT (FK) | Date the transaction occurred. Reference to `dim_date`. | `2023-10-15` |
| `amfi_code` | INTEGER (FK) | Reference to `dim_fund`. | `119551` |
| `transaction_type`| TEXT | Type of transaction (SIP, Lumpsum, Redemption). | `SIP` |
| `amount_inr` | INTEGER | Transaction amount in Indian Rupees. | `5000` |
| `state` | TEXT | State of the investor. | `Maharashtra` |
| `city` | TEXT | City of the investor. | `Mumbai` |
| `city_tier` | TEXT | Tier classification of the city (Tier 1/2/3). | `Tier 1` |
| `age_group` | TEXT | Age bracket of the investor. | `25-34` |
| `gender` | TEXT | Gender of the investor. | `M` |
| `annual_income_lakh`| REAL | Annual income of the investor in Lakhs. | `12.5` |
| `payment_mode` | TEXT | Method of payment. | `UPI` |
| `kyc_status` | TEXT | KYC verification status (Verified/Pending). | `Verified` |

### `fact_performance`
Source: `07_scheme_performance.csv`

| Column Name | Datatype | Business Definition | Example Value |
|-------------|----------|----------------------|---------------|
| `amfi_code` | INTEGER (PK, FK) | Reference to `dim_fund`. | `119551` |
| `scheme_name` | TEXT | Name of the fund. | `HDFC Flexi Cap Fund` |
| `fund_house` | TEXT | Name of the Asset Management Company. | `HDFC Mutual Fund` |
| `category` | TEXT | Primary investment category. | `Equity` |
| `plan` | TEXT | Investment plan type (Direct/Regular). | `Direct` |
| `return_1yr_pct` | REAL | Trailing 1-year return percentage. | `15.5` |
| `return_3yr_pct` | REAL | Trailing 3-year annualized return percentage. | `12.3` |
| `return_5yr_pct` | REAL | Trailing 5-year annualized return percentage. | `11.8` |
| `benchmark_3yr_pct`| REAL | Benchmark's 3-year return percentage. | `10.5` |
| `alpha` | REAL | Measure of performance on a risk-adjusted basis compared to the benchmark. | `2.1` |
| `beta` | REAL | Measure of volatility relative to the market. | `0.95` |
| `sharpe_ratio` | REAL | Risk-adjusted return metric. | `1.5` |
| `sortino_ratio` | REAL | Risk-adjusted return metric evaluating downside risk. | `2.2` |
| `std_dev_ann_pct`| REAL | Annualized standard deviation of returns (volatility). | `14.5` |
| `max_drawdown_pct` | REAL | Maximum observed loss from a peak to a trough. | `-20.5` |
| `aum_crore` | INTEGER | Assets Under Management in Crores. | `50000` |
| `expense_ratio_pct`| REAL | Annual expense ratio. | `0.85` |
| `morningstar_rating`| INTEGER | Rating given by Morningstar (1-5). | `4` |
| `risk_grade` | TEXT | Risk grade evaluation. | `High` |
| `anomaly_flag` | BOOLEAN | Flag indicating potentially anomalous performance numbers (e.g. returns > 100%). | `0` |

### `fact_aum`
Source: `03_aum_by_fund_house.csv`

| Column Name | Datatype | Business Definition | Example Value |
|-------------|----------|----------------------|---------------|
| `id` | INTEGER (PK) | Auto-incrementing primary key. | `1` |
| `date` | TEXT (FK) | Reference to `dim_date`. | `2023-10-31` |
| `fund_house` | TEXT | Name of the Asset Management Company. | `HDFC Mutual Fund` |
| `aum_lakh_crore` | REAL | AUM for the house in Lakh Crores. | `4.5` |
| `aum_crore` | INTEGER | AUM for the house in Crores. | `450000` |
| `num_schemes` | INTEGER | Number of active schemes managed by the fund house. | `85` |
