-- Q1: Show vehicle make/model alongside the county it's registered in
SELECT 
    r.dol_vehicle_id,
    v.make,
    v.model,
    v.model_year,
    r.county
FROM registrations r
JOIN vehicles v ON r.vin = v.vin
LIMIT 10;

-- Q2: Count how many EVs are registered per county, top 10 counties
SELECT 
    county,
    COUNT(*) AS vehicle_count
FROM registrations
GROUP BY county
ORDER BY vehicle_count DESC
LIMIT 10;

-- Q3: Which make has the most registered EVs, combining both tables
SELECT 
    v.make,
    COUNT(*) AS vehicle_count,
    ROUND(AVG(v.electric_range), 1) AS avg_range
FROM registrations r
JOIN vehicles v ON r.vin = v.vin
GROUP BY v.make
ORDER BY vehicle_count DESC
LIMIT 10;

-- Q4: Same as Q3, but split out BEV vs PHEV — fairer comparison
SELECT 
    v.make,
    v.electric_vehicle_type,
    COUNT(*) AS vehicle_count,
    ROUND(AVG(v.electric_range), 1) AS avg_range
FROM registrations r
JOIN vehicles v ON r.vin = v.vin
GROUP BY v.make, v.electric_vehicle_type
ORDER BY vehicle_count DESC
LIMIT 15;

-- Q5: How many rows actually have electric_range = 0?
SELECT 
    make, electric_vehicle_type,
    COUNT(*) AS total,
    SUM(CASE WHEN electric_range = 0 THEN 1 ELSE 0 END) AS zero_range_count
FROM vehicles
WHERE make IN ('FORD', 'RIVIAN')
GROUP BY make, electric_vehicle_type;