# Data Validation Report

## 1. Database Row Counts
| Table | DB Row Count |
|-------|--------------|
| dim_fund | 40 |
| dim_date | 1331 |
| fact_nav | 46000 |
| fact_transactions | 32778 |
| fact_performance | 40 |
| fact_aum | 90 |

## 2. Duplicate Primary Keys Check
- **dim_fund**: No duplicate amfi_code found. ✅
- **dim_date**: No duplicate date_id found. ✅
- **fact_nav**: No duplicate id found. ✅
- **fact_transactions**: No duplicate transaction_id found. ✅
- **fact_performance**: No duplicate amfi_code found. ✅
- **fact_aum**: No duplicate id found. ✅

## 3. Null Key Fields Check
- **dim_fund**: No NULL amfi_code found. ✅
- **dim_date**: No NULL date_id found. ✅
- **fact_nav**: No NULL id found. ✅
- **fact_transactions**: No NULL transaction_id found. ✅
- **fact_performance**: No NULL amfi_code found. ✅
- **fact_aum**: No NULL id found. ✅

## 4. Source vs Cleaned vs DB Row Counts Summary
The row counts matched successfully as verified in `reports/database_load_summary.md` during the loading phase. Initial data inspection highlighted duplicates which were successfully removed in the cleaned datasets prior to DB ingestion.