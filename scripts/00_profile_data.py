import pandas as pd

df = pd.read_csv("data/raw/Electric_Vehicle_Population_Data.csv")

print("="*60)
print(f"Dataset shape: {df.shape}")
print("="*60)

profile = pd.DataFrame({
    "dtype": df.dtypes,
    "missing_count": df.isna().sum(),
    "missing_pct": (df.isna().sum() / len(df) * 100).round(2),
    "n_unique": df.nunique(),
    "unique_pct": (df.nunique() / len(df) * 100).round(2),
})

# Flag likely key columns vs category columns
profile["likely_role"] = profile["unique_pct"].apply(
    lambda x: "UNIQUE KEY (≈100%)" if x > 95
    else "high-cardinality (check)" if x > 50
    else "category/dimension"
)

print(profile.to_string())

# Save profile report for documentation/README later
profile.to_csv("data/processed/data_profile_report.csv")
print("\nSaved profile report to data/processed/data_profile_report.csv")