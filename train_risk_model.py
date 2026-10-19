import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

DB_NAME = "namibia_risk_platform.db"

def train_sector_risk_model():
    print("--- Loading Data from Database for Model Training ---")
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM economic_nodes_log", conn)
    conn.close()

    if df.empty:
        print("[ERROR] No data found in the database. Run the ingestion and pipeline scripts first.")
        return

    # Feature Engineering: 
    # Let's simulate a target variable 'vulnerability_index' based on temperature and precipitation stress,
    # representing how vulnerable a sector's supply chain or operations are at that moment.
    # Higher temperature anomalies or zero precipitation increase agricultural and logistics stress.
    df['temp_stress'] = abs(df['temperature_celsius'] - 22.0)  # Deviation from baseline comfortable temp
    df['water_stress'] = df['precipitation_mm'].apply(lambda x: 10.0 if x == 0.0 else 1.0)
    
    # Synthetic Target: Sector Vulnerability Index (scale 0-100)
    df['vulnerability_index'] = (df['temp_stress'] * 2.5) + (df['water_stress'] * 4.0) + (df['humidity_percent'] * 0.1)

    # Features and Target
    X = df[['temperature_celsius', 'humidity_percent', 'precipitation_mm', 'temp_stress', 'water_stress']]
    y = df['vulnerability_index']

    # Train a Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    print("[SUCCESS] Machine Learning Model Trained Successfully!")
    
    # Let's run a prediction sample across our nodes
    df['predicted_vulnerability'] = model.predict(X)
    
    print("\n--- Model Predictions & Sector Risk Assessment ---")
    output_display = df[['node', 'primary_sector', 'temperature_celsius', 'precipitation_mm', 'predicted_vulnerability']]
    print(output_display.to_string())

if __name__ == "__main__":
    train_sector_risk_model()