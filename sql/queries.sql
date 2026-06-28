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

-- Q6: Which vehicles have the most anomalies, and what's their average vibration?
SELECT 
    v.vin,
    vh.make,
    vh.model,
    COUNT(*) AS total_readings,
    SUM(CASE WHEN v.is_anomaly = 1 THEN 1 ELSE 0 END) AS anomaly_count,
    ROUND(AVG(v.vibration_g), 3) AS avg_vibration
FROM sensor_readings v
JOIN vehicles vh ON v.vin = vh.vin
GROUP BY v.vin, vh.make, vh.model
ORDER BY anomaly_count DESC
LIMIT 10;