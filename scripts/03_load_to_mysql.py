import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:@localhost/ev_dashboard")

vehicles = pd.read_csv("data/processed/vehicles.csv")
registrations = pd.read_csv("data/processed/registrations.csv")

# --- Fix column name mismatch between CSV and MySQL schema ---
vehicles = vehicles.rename(columns={
    "clean_alternative_fuel_vehicle_cafv_eligibility": "cafv_eligibility"
})
registrations = registrations.rename(columns={
    "2020_census_tract": "census_tract"
})

print("Vehicles to load:", vehicles.shape)
print("Registrations to load:", registrations.shape)

vehicles.to_sql("vehicles", engine, if_exists="append", index=False)
print("Loaded vehicles table.")

registrations.to_sql("registrations", engine, if_exists="append", index=False)
print("Loaded registrations table.")