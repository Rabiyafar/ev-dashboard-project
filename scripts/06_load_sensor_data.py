import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:@localhost/ev_dashboard")

sensor_df = pd.read_csv("data/processed/sensor_readings.csv")

sensor_df.to_sql("sensor_readings", engine, if_exists="append", index=False)
print("Loaded sensor_readings:", sensor_df.shape)