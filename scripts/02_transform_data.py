import pandas as pd
import re

# Load raw data
df = pd.read_csv("data/raw/Electric_Vehicle_Population_Data.csv")

# --- Clean column names (lowercase, no spaces/parentheses) ---
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[^\w\s]", "", regex=True)   # remove ( ) etc
    .str.replace(" ", "_")
)
print("Cleaned columns:\n", df.columns.tolist())

# --- Rename VIN column properly ---
df = df.rename(columns={"vin_110": "vin"})

# --- Extract latitude & longitude from 'vehicle_location' ---
# Format looks like: POINT (-122.913 47.013)
def extract_coords(point_str):
    if pd.isna(point_str):
        return (None, None)
    match = re.match(r"POINT \(([-\d.]+) ([-\d.]+)\)", point_str)
    if match:
        lon, lat = match.groups()
        return (float(lat), float(lon))
    return (None, None)

coords = df["vehicle_location"].apply(extract_coords)
df["latitude"] = coords.apply(lambda x: x[0])
df["longitude"] = coords.apply(lambda x: x[1])

# --- Drop rows with no VIN (shouldn't be any, but safety check) ---
df = df.dropna(subset=["vin"])

# --- Drop exact duplicate VINs, keep first ---
# --- Drop rows with no VIN (shouldn't be any, but safety check) ---
df = df.dropna(subset=["vin"])

# --- Drop true duplicate vehicle records (by dol_vehicle_id, the real unique ID) ---
before = len(df)
df = df.drop_duplicates(subset=["dol_vehicle_id"], keep="first")
after = len(df)
print(f"Dropped {before - after} duplicate dol_vehicle_id rows (true duplicates)")

# --- Fill missing electric_range / base_msrp with 0 (data quality note) ---
# Treat both missing AND 0 as "unknown" (0 isn't a real range for an EV)
df["electric_range"] = df["electric_range"].replace(0, pd.NA)
df["base_msrp"] = df["base_msrp"].fillna(0)

# --- Save cleaned full table to processed folder ---
df.to_csv("data/processed/ev_cleaned.csv", index=False)
print("Saved cleaned data:", df.shape)

# --- Table 1: vehicles = one row per unique configuration (vin = first-10, i.e. make/model/trim) ---
vehicles = df[[
    "vin", "make", "model", "model_year",
    "electric_vehicle_type", "electric_range",
    "base_msrp", "clean_alternative_fuel_vehicle_cafv_eligibility"
]].drop_duplicates(subset=["vin"])

# --- Table 2: registrations = one row per PHYSICAL vehicle (dol_vehicle_id is the real PK) ---
registrations = df[[
    "dol_vehicle_id", "vin", "county", "city", "state", "postal_code",
    "legislative_district", "electric_utility",
    "2020_census_tract", "latitude", "longitude"
]]

vehicles.to_csv("data/processed/vehicles.csv", index=False)
registrations.to_csv("data/processed/registrations.csv", index=False)

print("Saved vehicles.csv:", vehicles.shape)
print("Saved registrations.csv:", registrations.shape)

