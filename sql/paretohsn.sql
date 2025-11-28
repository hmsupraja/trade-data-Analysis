-- Pareto analysis: top 25 HSN codes by total value, plus 'Others' aggregated
WITH hsn_totals AS (
    SELECT
        COALESCE(hsn_code, 'UNKNOWN') AS hsn_code,
        SUM(total_value_inr) AS total_value_inr
    FROM shipments
    GROUP BY COALESCE(hsn_code, 'UNKNOWN')
),
ranked AS (
    SELECT
        hsn_code,
        total_value_inr,
        RANK() OVER (ORDER BY total_value_inr DESC) AS rnk,
        SUM(total_value_inr) OVER () AS grand_total
    FROM hsn_totals
),
top25 AS (
    SELECT hsn_code, total_value_inr, grand_total FROM ranked WHERE rnk <= 25
),
others AS (
    SELECT 'Others' AS hsn_code, SUM(total_value_inr) AS total_value_inr, grand_total
    FROM ranked WHERE rnk > 25
)
SELECT hsn_code, total_value_inr, 100.0 * total_value_inr / grand_total AS pct_of_total
FROM (
    SELECT * FROM top25
    UNION ALL
    SELECT * FROM others
) t
ORDER BY total_value_inr DESC;
