-- 1. Top 5 funds by AUM
-- Retrieves the top 5 funds based on their AUM in crores from the performance fact table.
SELECT amfi_code, scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
-- Calculates the average Net Asset Value (NAV) for each month across all funds.
SELECT d.year, d.month, AVG(f.nav) as avg_nav
FROM fact_nav f
JOIN dim_date d ON f.date = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. SIP inflow YoY growth
-- (Note: Since we only have transaction data and don't have a direct YoY table, 
-- we calculate this by aggregating SIP transactions by year and month, then 
-- comparing to the same month in the previous year using a self join or window function.)
WITH monthly_sip AS (
    SELECT d.year, d.month, SUM(t.amount_inr) as total_sip
    FROM fact_transactions t
    JOIN dim_date d ON t.transaction_date = d.date_id
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year, d.month
)
SELECT m1.year, m1.month, m1.total_sip,
       m2.total_sip as prev_year_sip,
       ROUND(((m1.total_sip - m2.total_sip) * 100.0 / NULLIF(m2.total_sip, 0)), 2) as yoy_growth_pct
FROM monthly_sip m1
LEFT JOIN monthly_sip m2 ON m1.year = m2.year + 1 AND m1.month = m2.month
ORDER BY m1.year, m1.month;

-- 4. Transactions by state
-- Counts the total number of transactions and sum of amounts for each state.
SELECT state, COUNT(*) as total_transactions, SUM(amount_inr) as total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- 5. Funds with expense_ratio < 1%
-- Lists all funds that have an expense ratio strictly less than 1 percent.
SELECT amfi_code, scheme_name, category, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Top funds by Sharpe ratio
-- Identifies funds with the best risk-adjusted performance using the Sharpe ratio.
SELECT amfi_code, scheme_name, category, sharpe_ratio
FROM fact_performance
WHERE sharpe_ratio IS NOT NULL
ORDER BY sharpe_ratio DESC
LIMIT 10;

-- 7. Top funds by 3-year return
-- Lists the top performing funds based on their 3-year trailing returns.
SELECT amfi_code, scheme_name, category, return_3yr_pct
FROM fact_performance
WHERE return_3yr_pct IS NOT NULL
ORDER BY return_3yr_pct DESC
LIMIT 10;

-- 8. Fund count by category
-- Shows the distribution of mutual funds across different primary categories.
SELECT category, COUNT(*) as num_funds
FROM dim_fund
GROUP BY category
ORDER BY num_funds DESC;

-- 9. Average transaction amount by state
-- Calculates the average transaction size by investors in each state.
SELECT state, ROUND(AVG(amount_inr), 2) as avg_transaction_amount
FROM fact_transactions
GROUP BY state
ORDER BY avg_transaction_amount DESC;

-- 10. Top AMC (Asset Management Company/Fund House) by AUM
-- Aggregates the AUM at the Fund House level to find the largest AMCs.
SELECT fund_house, SUM(aum_crore) as total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC
LIMIT 10;
