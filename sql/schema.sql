-- EV Dashboard Project - Database Schema
-- Run with: mysql -u root ev_dashboard < sql/schema.sql

CREATE TABLE vehicles (
    vin VARCHAR(10) PRIMARY KEY,
    make VARCHAR(50),
    model VARCHAR(50),
    model_year INT,
    electric_vehicle_type VARCHAR(50),
    electric_range INT,
    base_msrp DECIMAL(10,2),
    cafv_eligibility VARCHAR(100)
);

CREATE TABLE registrations (
    dol_vehicle_id BIGINT PRIMARY KEY,
    vin VARCHAR(10),
    county VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(10),
    postal_code VARCHAR(10),
    legislative_district INT,
    electric_utility VARCHAR(200),
    census_tract VARCHAR(20),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    FOREIGN KEY (vin) REFERENCES vehicles(vin)
);

CREATE TABLE sensor_readings (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    vin VARCHAR(10),
    timestamp DATETIME,
    vibration_g DECIMAL(6,3),
    temperature_c DECIMAL(5,2),
    motor_rpm DECIMAL(6,1),
    is_anomaly BOOLEAN,
    FOREIGN KEY (vin) REFERENCES vehicles(vin)
);