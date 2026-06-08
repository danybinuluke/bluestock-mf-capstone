# DAX Measures Inventory

This document contains the Data Analysis Expressions (DAX) used to calculate the Key Performance Indicators (KPIs) and metrics for the Bluestock Mutual Fund Analytics Platform.

## 1. Industry KPIs

```dax
// Total Assets Under Management (AUM)
Total AUM = SUM('fact_aum'[aum_crore])

// Total SIP Inflow
Total SIP Inflow = SUM('fact_sip_industry'[sip_inflow])

// Total Folios
Total Folios = SUM('fact_sip_industry'[total_folios])

// Total Schemes
Total Schemes = DISTINCTCOUNT('dim_fund'[amfi_code])

// Average Expense Ratio
Average Expense Ratio = AVERAGE('dim_fund'[expense_ratio])
```

## 2. Performance Metrics

```dax
// Average Return (using 3-year return as default average return metric)
Average Return = AVERAGE('fact_performance'[return_3y])

// Average Sharpe Ratio
Average Sharpe Ratio = AVERAGE('fact_performance'[sharpe_ratio])

// Average Sortino Ratio
Average Sortino Ratio = AVERAGE('fact_performance'[sortino_ratio])

// Average Alpha
Average Alpha = AVERAGE('fact_performance'[alpha])

// Average Beta
Average Beta = AVERAGE('fact_performance'[beta])

// Average Max Drawdown
Average Max Drawdown = AVERAGE('fact_performance'[max_drawdown])

// Top Fund Score (Maximum score among selected funds)
Top Fund Score = MAX('fact_performance'[fund_score])
```

## 3. Investor Metrics

```dax
// Total Investors
Total Investors = DISTINCTCOUNT('fact_transactions'[investor_id])

// Total Transactions
Total Transactions = COUNTROWS('fact_transactions')

// Average SIP Amount
Average SIP Amount = 
CALCULATE(
    AVERAGE('fact_transactions'[amount]),
    'fact_transactions'[transaction_type] = "SIP"
)

// Average Transaction Amount
Average Transaction Amount = AVERAGE('fact_transactions'[amount])

// Redemption Rate (Redemption amount vs Total amount)
Redemption Rate = 
DIVIDE(
    CALCULATE(SUM('fact_transactions'[amount]), 'fact_transactions'[transaction_type] = "Redemption"),
    CALCULATE(SUM('fact_transactions'[amount]), 'fact_transactions'[transaction_type] IN {"SIP", "Lumpsum"})
)
```

## 4. Market Metrics

```dax
// Assuming benchmark performance is available either in fact_performance or a dedicated benchmark table linked by date.
// Here we assume a 'fact_benchmark' table with standard relationships, or columns in fact_performance.

// Nifty 50 Return
Nifty 50 Return = CALCULATE(AVERAGE('fact_performance'[benchmark_3yr_pct]), 'dim_fund'[benchmark] = "NIFTY 50 TRI")

// Nifty 100 Return
Nifty 100 Return = CALCULATE(AVERAGE('fact_performance'[benchmark_3yr_pct]), 'dim_fund'[benchmark] = "NIFTY 100 TRI")

// Fund vs Benchmark Difference
Fund vs Benchmark Difference = [Average Return] - [Nifty 50 Return]
```
