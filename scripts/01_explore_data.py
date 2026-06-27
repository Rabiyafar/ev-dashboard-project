import pandas as pd

df = pd.read_csv("data/raw/Electric_Vehicle_Population_Data.csv")

print("Shape:", df.shape)
print("\nColumns:\n", df.columns.tolist())
print("\nData types:\n", df.dtypes)
print("\nMissing values per column:\n", df.isna().sum())
print("\nFirst 5 rows:\n", df.head())