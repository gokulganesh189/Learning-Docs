
SELECT
    sale_id,
    product_id,
    sale_date,
    amount,
    AVG(amount) OVER (
        PARTITION BY product_id
        ORDER BY sale_date
        RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW
    ) AS avg_amount_7_days