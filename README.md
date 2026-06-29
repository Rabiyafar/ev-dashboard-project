# EV Market & NVH Sensor Analytics Pipeline

An end-to-end data pipeline and dashboard project: raw vehicle registration data is cleaned and validated in Python, loaded into a relational MySQL database, and visualized in Tableau — including a synthetic vehicle sensor (NVH) module modeling vibration/anomaly monitoring.

Built as a self-directed learning project to practice the ETL → relational database → BI dashboard workflow end-to-end.

## Project Overview

This project uses the [Washington State EV Population dataset](https://catalog.data.gov/dataset/electric-vehicle-population-data) (135,038 registered electric vehicles) to build a full analytics pipeline:

1. **Extract** — raw CSV ingestion and profiling
2. **Transform** — cleaning, validation, and relational schema design in Python
3. **Load** — MySQL database with proper keys and foreign key constraints
4. **Analyze** — SQL queries (joins, aggregations, anomaly detection)
5. **Visualize** — three Tableau dashboards covering market overview, geographic/data-quality deep-dive, and synthetic sensor monitoring

## Why This Project

This was built to practice the specific workflow described in a Data Science internship in vehicle NVH (Noise, Vibration, Harshness) analytics — ETL pipeline development, Power BI/BI dashboarding, SQL and relational databases, and sensor data processing. Since proprietary vehicle sensor data isn't publicly available, a synthetic sensor dataset was generated to demonstrate that part of the workflow specifically.

## Architecture

```
Raw CSV (data.gov)
      │
      ▼
Python ETL (pandas)
  ├── Data profiling (cardinality checks before any cleaning)
  ├── Cleaning & validation
  └── Relational split: vehicles + registrations
      │
      ▼
MySQL Database
  ├── vehicles (PK: vin)
  ├── registrations (PK: dol_vehicle_id, FK: vin)
  └── sensor_readings (FK: vin) — synthetic NVH data
      │
      ▼
SQL Analysis (JOINs, GROUP BY, anomaly detection)
      │
      ▼
Tableau Dashboards
  ├── EV Market Overview
  ├── Deep Dive & Data Quality
  └── NVH Sensor Monitoring
```

## Key Findings

- **Geographic concentration**: King County accounts for ~52% of all registered EVs in the dataset, far outweighing any other county — consistent with Seattle-metro EV infrastructure and adoption patterns.
- **Tesla dominance**: Tesla represents ~46% of all registered EVs in the dataset, with a strong average range (~240 miles) once data quality issues were corrected (see below).
- **A real data quality bug, caught and fixed**: an early transform step filled missing `electric_range` values with `0`. Because `0` is not a valid range for a real EV, this silently corrupted averages — Ford BEVs appeared to average 6.2 miles of range (physically implausible). The fix (treating `0`/missing as `NULL` instead of a literal zero) corrected averages across every affected manufacturer; Rivian, which had no range data recorded for any vehicle, now correctly shows `NULL` rather than a misleading `0`.
- **Primary key discovery**: the dataset's `VIN (1-10)` field looked like a natural unique identifier but was only 6.7% unique — it identifies a vehicle *configuration* (make/model/trim), not an individual physical vehicle. `DOL Vehicle ID` (100% unique) is the true primary key. This was confirmed via a data profiling step before any schema design, rather than assumed.

## Dashboards

**1. EV Market Overview** — KPI summary (total vehicles, counties, average range), top counties and manufacturers by registration count, adoption trend by model year, BEV vs. PHEV split.

**2. Deep Dive & Data Quality** — geographic distribution map, price-vs-range scatter plot by manufacturer, and a dedicated view of the missing-range data quality issue described above.

**3. NVH Sensor Monitoring** — synthetic vibration sensor readings (10,000 readings across 50 vehicles) with anomaly detection, modeling the kind of vibration/noise monitoring relevant to vehicle NVH analysis.

## Tech Stack

- **Python** (pandas) — data cleaning, validation, and transformation
- **MySQL** — relational storage with primary/foreign key constraints
- **SQLAlchemy** — Python-to-MySQL data loading
- **SQL** — joins, aggregations, anomaly-detection queries
- **Tableau Public** — dashboard visualization

## Project Structure

```
ev_dashboard_project/
├── data/
│   ├── raw/              # Original downloaded dataset (not committed — see below)
│   └── processed/        # Cleaned, transformed CSVs (not committed)
├── scripts/
│   ├── 00_profile_data.py            # Data profiling — run before any cleaning
│   ├── 02_transform_data.py          # Cleaning, validation, relational split
│   ├── 03_load_to_mysql.py           # Load cleaned data into MySQL
│   ├── 04_export_for_dashboard.py    # Export joined data for Tableau
│   ├── 05_generate_nvh_sensor_data.py # Synthetic sensor data generation
│   ├── 06_load_sensor_data.py        # Load sensor data into MySQL
│   └── 07_export_sensor_for_dashboard.py
├── sql/
│   ├── schema.sql                # Table definitions (vehicles, registrations, sensor_readings)
│   └── practice_queries.sql      # Analysis queries (JOINs, GROUP BY, anomaly detection)
├── dashboard/             # Exported CSVs feeding Tableau (not committed)
└── README.md
```

## Running This Project

1. Download the [EV Population dataset](https://catalog.data.gov/dataset/electric-vehicle-population-data) and place it in `data/raw/`
2. Create a virtual environment and install dependencies: `pandas`, `numpy`, `sqlalchemy`, `mysql-connector-python`
3. Create a MySQL database named `ev_dashboard`, then run the schema: `mysql -u root ev_dashboard < sql/schema.sql`
4. Run the scripts in order: `00_profile_data.py` → `02_transform_data.py` → `03_load_to_mysql.py` → `05_generate_nvh_sensor_data.py` → `06_load_sensor_data.py` → `04_export_for_dashboard.py` / `07_export_sensor_for_dashboard.py`
5. Open the exported CSVs in `dashboard/` with Tableau Public

## Notes on Data

- Raw and processed data files are excluded from this repository (see `.gitignore`) since they're large and regeneratable from the source scripts.
- Sensor/NVH data is **synthetic** — generated to simulate realistic vibration, temperature, and RPM readings with injected anomalies, since real proprietary sensor data isn't publicly available.