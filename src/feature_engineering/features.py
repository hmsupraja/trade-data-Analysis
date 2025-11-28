-- Supplier activity: Active in 2025 vs historical
WITH supplier_years AS (
    SELECT supplier_name, ARRAY_AGG(DISTINCT year) AS years, MAX(year) AS last_year
    FROM shipments
    GROUP BY supplier_name
)
SELECT
    supplier_name,
    years,
    CASE WHEN 2025 = ANY(years) THEN 'Active_2025' ELSE 'Not_Active_2025' END AS status_2025,
    CASE WHEN last_year < 2025 THEN 'Churned' WHEN last_year = 2025 THEN 'Active' ELSE 'Historic' END AS life_stage
FROM supplier_years
ORDER BY status_2025 DESC, supplier_name;
