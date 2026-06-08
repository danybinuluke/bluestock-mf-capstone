# Power BI Data Model Documentation

This document outlines the data model architecture for the Bluestock Mutual Fund Analytics Platform Power BI dashboard. It defines the tables, relationships, and data modeling strategies required for accurate and performant analytics.

## Tables

### Dimension Tables

1. **`dim_fund`**
   * **Description**: Contains static and descriptive attributes of mutual fund schemes.
   * **Primary Key**: `amfi_code`
   * **Key Columns**: `amfi_code`, `fund_name`, `fund_house`, `category`, `sub_category`, `risk_category`, `plan_type`, `launch_date`.

2. **`dim_date`**
   * **Description**: The standard continuous date table used for time intelligence functions. Must be marked as a Date table in Power BI.
   * **Primary Key**: `date` (or `date_id`)
   * **Key Columns**: `date`, `year`, `quarter`, `month`, `month_name`, `day`, `is_weekend`, `fin_year`.

### Fact Tables

3. **`fact_nav`**
   * **Description**: Historical daily Net Asset Value (NAV) records for all funds.
   * **Foreign Keys**: `amfi_code`, `date`
   * **Key Columns**: `amfi_code`, `date`, `nav`.

4. **`fact_transactions`**
   * **Description**: Transaction-level details including investments and redemptions.
   * **Foreign Keys**: `amfi_code`, `date`
   * **Key Columns**: `transaction_id`, `amfi_code`, `date`, `investor_id`, `transaction_type` (SIP, Lumpsum, Redemption), `amount`, `state`, `city_tier`, `investor_age_group`.

5. **`fact_performance`**
   * **Description**: Calculated performance metrics over various time horizons.
   * **Foreign Keys**: `amfi_code`
   * **Key Columns**: `amfi_code`, `return_1y`, `return_3y`, `return_5y`, `sharpe_ratio`, `sortino_ratio`, `alpha`, `beta`, `max_drawdown`, `fund_score`.

6. **`fact_aum`**
   * **Description**: Monthly Assets Under Management (AUM) values per fund.
   * **Foreign Keys**: `amfi_code`, `date`
   * **Key Columns**: `amfi_code`, `date`, `aum_amount`.

7. **`fact_sip_industry`**
   * **Description**: Monthly industry-wide SIP inflow, folios, and scheme counts (can be aggregated or detailed).
   * **Foreign Keys**: `date`
   * **Key Columns**: `date`, `sip_inflow`, `total_folios`, `total_schemes`.

8. **`fact_portfolio`**
   * **Description**: Periodic portfolio composition of funds (asset allocation, sector weightings).
   * **Foreign Keys**: `amfi_code`, `date`
   * **Key Columns**: `amfi_code`, `date`, `asset_class`, `sector`, `allocation_percentage`.

---

## Relationships

All relationships are formulated using a Star Schema topology with `dim_fund` and `dim_date` filtering the respective fact tables.

| From Table (Many/Fact) | From Column | To Table (One/Dim) | To Column | Cardinality | Cross Filter Direction | Active |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `fact_nav` | `amfi_code` | `dim_fund` | `amfi_code` | Many to One (*:1) | Single | Yes |
| `fact_nav` | `date` | `dim_date` | `date` | Many to One (*:1) | Single | Yes |
| `fact_transactions` | `amfi_code` | `dim_fund` | `amfi_code` | Many to One (*:1) | Single | Yes |
| `fact_transactions` | `date` | `dim_date` | `date` | Many to One (*:1) | Single | Yes |
| `fact_performance` | `amfi_code` | `dim_fund` | `amfi_code` | Many to One (*:1) | Single | Yes |
| `fact_aum` | `amfi_code` | `dim_fund` | `amfi_code` | Many to One (*:1) | Single | Yes |
| `fact_aum` | `date` | `dim_date` | `date` | Many to One (*:1) | Single | Yes |
| `fact_sip_industry` | `date` | `dim_date` | `date` | Many to One (*:1) | Single | Yes |
| `fact_portfolio` | `amfi_code` | `dim_fund` | `amfi_code` | Many to One (*:1) | Single | Yes |
| `fact_portfolio` | `date` | `dim_date` | `date` | Many to One (*:1) | Single | Yes |

## Date Table Usage
*   The `dim_date` table must be explicitly marked as the Date table in Power BI (Table tools > Mark as date table).
*   All time intelligence functions in DAX (e.g., `YTD`, `SAMEPERIODLASTYEAR`) must reference the `dim_date[date]` column.
*   Do NOT use the auto date/time hierarchy feature; ensure it is disabled in Power BI Data Load settings.
