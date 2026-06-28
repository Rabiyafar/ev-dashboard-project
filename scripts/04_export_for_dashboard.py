import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:@localhost/ev_dashboard")

query = """
SELECT 
    r.dol_vehicle_id,
    v.vin,
    v.make,
    v.model,
    v.model_year,
    v.electric_vehicle_type,
    v.electric_range,
    v.base_msrp,
    v.cafv_eligibility,
    r.county,
    r.city,
    r.state,
    r.postal_code,
    r.legislative_district,
    r.electric_utility,
    r.latitude,
    r.longitude
FROM registrations r
JOIN vehicles v ON r.vin = v.vin
"""

df = pd.read_sql(query, engine)
print("Exported rows:", df.shape)

df.to_csv("dashboard/ev_dashboard_data.csv", index=False)
print("Saved to dashboard/ev_dashboard_data.csv")