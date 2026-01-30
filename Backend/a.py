import os
import pickle
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, stddev

# --- CONFIGURATION ---
# The columns must match the EXACT order used in your model training
NUMERICAL_COLS = [
    'lat', 
    'lon', 
    'duration', 
    'start_year', 
    'start_month_sin', 
    'start_month_cos'
]

PARQUET_PATH = r"C:\Users\USER\preprocessed_ghg_sequences.parquet"
OUTPUT_PATH = "models/scaler_model.pkl"

def generate_scaler():
    print(f"--- Generating Scaler from: {PARQUET_PATH} ---")
    
    # 1. Initialize Spark
    try:
        spark = SparkSession.builder \
            .appName("ScalerGenerator") \
            .config("spark.driver.memory", "4g") \
            .getOrCreate()
    except Exception as e:
        print(f"❌ Error starting Spark: {e}")
        return

    # 2. Load Data
    if not os.path.exists(PARQUET_PATH):
        print(f"❌ Fatal Error: Data file '{PARQUET_PATH}' not found.")
        print("   Make sure you are running this from the project root.")
        return

    df = spark.read.parquet(PARQUET_PATH)
    
    # 3. Calculate Statistics
    print("Calculating Mean and StdDev for 6 features...")
    
    # We build a list of aggregation expressions
    # This runs one optimized pass over the data
    exprs = []
    for c in NUMERICAL_COLS:
        exprs.append(mean(col(c)).alias(f"{c}_mean"))
        exprs.append(stddev(col(c)).alias(f"{c}_std"))
    
    stats = df.select(*exprs).collect()[0]
    
    # 4. Format into Numpy Arrays
    means_list = []
    stds_list = []
    
    print("\n--- CALCULATED VALUES ---")
    print(f"{'Feature':<20} | {'Mean':<15} | {'StdDev':<15}")
    print("-" * 55)
    
    for c in NUMERICAL_COLS:
        mu = stats[f"{c}_mean"]
        sigma = stats[f"{c}_std"]
        
        means_list.append(mu)
        stds_list.append(sigma)
        
        print(f"{c:<20} | {mu:<15.4f} | {sigma:<15.4f}")

    # 5. Create Dictionary
    scaler_data = {
        "means": np.array(means_list, dtype=np.float64),
        "stds": np.array(stds_list, dtype=np.float64)
    }
    
    # 6. Save to Pickle
    os.makedirs("models", exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump(scaler_data, f)
        
    print(f"\n✅ Success! Scaler saved to: {os.path.abspath(OUTPUT_PATH)}")
    print("   You can now restart your API to use these correct values.")
    spark.stop()

if __name__ == "__main__":
    generate_scaler()