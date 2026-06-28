import pandas as pd
import numpy as np

np.random.seed(42)  # reproducible results

# --- Load a sample of real vehicles to attach sensor data to ---
vehicles = pd.read_csv("data/processed/vehicles.csv")

# Use a manageable subset (simulating sensors only exist on test/sample units)
sample_vehicles = vehicles.sample(n=50, random_state=42)["vin"].tolist()

records = []
readings_per_vehicle = 200  # simulates 200 timestamped sensor readings per vehicle

for vin in sample_vehicles:
    base_vibration = np.random.uniform(0.5, 2.0)   # baseline vibration level (g-force units)
    base_temp = np.random.uniform(25, 35)           # baseline motor temp (Celsius)
    base_rpm = np.random.uniform(150, 300)           # baseline motor RPM

    for i in range(readings_per_vehicle):
        timestamp = pd.Timestamp("2026-01-01") + pd.Timedelta(seconds=i * 5)

        # Normal signal = baseline + small random noise (simulates real sensor jitter)
        vibration = base_vibration + np.random.normal(0, 0.15)
        temperature = base_temp + np.random.normal(0, 0.5) + (i * 0.01)  # slight warm-up trend
        rpm = base_rpm + np.random.normal(0, 10)

        # Inject occasional anomaly spikes (simulates a real NVH event, e.g. loose component)
        is_anomaly = np.random.random() < 0.02  # 2% chance per reading
        if is_anomaly:
            vibration += np.random.uniform(2, 5)  # sudden vibration spike

        records.append({
            "vin": vin,
            "timestamp": timestamp,
            "vibration_g": round(vibration, 3),
            "temperature_c": round(temperature, 2),
            "motor_rpm": round(rpm, 1),
            "is_anomaly": is_anomaly
        })

sensor_df = pd.DataFrame(records)
sensor_df.to_csv("data/processed/sensor_readings.csv", index=False)

print("Generated sensor readings:", sensor_df.shape)
print("Anomalies flagged:", sensor_df["is_anomaly"].sum())
print(sensor_df.head())