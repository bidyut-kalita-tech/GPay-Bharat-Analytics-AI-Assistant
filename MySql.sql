CREATE DATABASE gpay_db;
USE gpay_db;

-- 1. Merchant Category Ranking by Total Spend & Share
SELECT 
    merchant_category,
    COUNT(`transaction id`) AS total_txns,
    SUM(`amount (INR)`) AS total_revenue,
    ROUND((SUM(`amount (INR)`) / (SELECT SUM(`amount (INR)`) FROM upi_transactions)) * 100, 2) AS revenue_share_pct,
    DENSE_RANK() OVER (ORDER BY SUM(`amount (INR)`) DESC) AS category_rank
FROM upi_transactions
WHERE transaction_status = 'SUCCESS'
GROUP BY merchant_category;

-- 2. State-Wise Performance & Fraud Breakdown
SELECT 
    sender_state,
    COUNT(*) AS total_volume,
    SUM(`amount (INR)`) AS total_spend,
    SUM(fraud_flag) AS fraud_cases,
    ROUND((SUM(fraud_flag) / COUNT(*)) * 100, 3) AS fraud_percentage
FROM upi_transactions
GROUP BY sender_state
ORDER BY total_spend DESC;