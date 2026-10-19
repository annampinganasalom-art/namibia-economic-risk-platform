import json
import sqlite3
import pandas as pd

# 1. Initialize local SQLite Database (simulating a Cloud Database like PostgreSQL/AWS RDS)
DB_NAME = "namibia_risk_platform.db"


def init_database():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  # Create structured table for economic nodes and risk metrics
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS economic_nodes_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node TEXT NOT NULL,
            region TEXT NOT NULL,
            primary_sector TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            temperature_celsius REAL,
            humidity_percent REAL,
            precipitation_mm REAL
        )
    """)
  conn.commit()
  conn.close()
  print("[SUCCESS] Database schema initialized successfully.")


def load_json_to_database():
  # Load the raw JSON file generated in Step 1
  try:
    with open("raw_namibia_ingestion.json", "r") as f:
      records = json.load(f)
  except FileNotFoundError:
    print("[ERROR] 'raw_namibia_ingestion.json' not found. Run Step 1 first.")
    return

  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  # Insert each record into the database table
  for record in records:
    cursor.execute(
        """
            INSERT INTO economic_nodes_log (
                node, region, primary_sector, timestamp, 
                temperature_celsius, humidity_percent, precipitation_mm
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["node"],
            record["region"],
            record["primary_sector"],
            record["timestamp"],
            record["temperature_celsius"],
            record["humidity_percent"],
            record["precipitation_mm"],
        ),
    )

  conn.commit()

  # Query back to verify storage
  df_verification = pd.read_sql_query(
      "SELECT * FROM economic_nodes_log", conn
  )
  conn.close()

  print("\n--- Data Successfully Stored & Queried from Database ---")
  print(df_verification.to_string())


if __name__ == "__main__":
  init_database()
  load_json_to_database()