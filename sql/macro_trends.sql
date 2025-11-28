-- Yearly totals and YoY growth for Total Value, Duty Paid, Grand Total
WITH yearly AS (
    SELECT
        year,
        SUM(total_value_inr)   AS total_value_inr,
        SUM(duty_paid_inr)     AS duty_paid_inr,
        SUM(grand_total_inr)   AS grand_total_inr
    FROM shipments
    GROUP BY year
)
SELECT
    year,
    total_value_inr,
    duty_paid_inr,
    grand_total_inr,
    100.0 * (total_value_inr - LAG(total_value_inr) OVER (ORDER BY year))
        / NULLIF(LAG(total_value_inr) OVER (ORDER BY year),0) AS yoy_total_value_pct,
    100.0 * (duty_paid_inr - LAG(duty_paid_inr) OVER (ORDER BY year))
        / NULLIF(LAG(duty_paid_inr) OVER (ORDER BY year),0) AS yoy_duty_paid_pct,
    100.0 * (grand_total_inr - LAG(grand_total_inr) OVER (ORDER BY year))
        / NULLIF(LAG(grand_total_inr) OVER (ORDER BY year),0) AS yoy_grand_total_pct
FROM yearly
ORDER BY year;
