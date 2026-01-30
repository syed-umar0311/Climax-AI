from datetime import datetime
import numpy as np
from .utils import get_month_duration, get_default_lat_lon, get_subsectors
import math as m

def preprocess_input(user_input, scaler_model, indexers):
    """
    Inference Preprocessing Pipeline:
    1. Standardizes Inputs (Country to Upper, others to Lower).
    2. Scales Lat, Lon, Duration, Year using scaler.pkl statistics.
    3. Generates Raw Cyclic Sine/Cosine (Skipping scaler to match training).
    """
    
    # --- 1. Extract and Normalize Inputs ---
    country = user_input.get('country')
    sector = user_input.get('sector')
    gas = user_input.get('gas')
    
    # Normalization (Crucial for dictionary lookups)
    country_normalized = country.upper() 
    sector_normalized = sector.lower()   
    gas_normalized = gas.lower()         

    start_year = user_input.get('year', datetime.now().year) 
    start_month = user_input.get('month', datetime.now().month + 1)
    
    # Handle month rollover
    if start_month > 12:
        start_year += 1
        start_month = 1

    lat = user_input.get('lat')
    lon = user_input.get('lon')

    # Default Lat/Lon fallback
    if lat is None or lon is None:
        lat, lon = get_default_lat_lon(country)

    subsectors = get_subsectors(sector_normalized) 
    results = {}

    # --- 2. Encode Categorical Features ---
    iso3_country_index = indexers["iso3_country"].get(country_normalized, -1)
    sector_index = indexers["sector"].get(sector_normalized, -1)
    gas_index = indexers["gas"].get(gas_normalized, -1)
    
    # Validation
    if iso3_country_index == -1:
        print(f"❌ Error: Country '{country_normalized}' not found in training data.")
        return {}
    if sector_index == -1:
        print(f"❌ Error: Sector '{sector_normalized}' not found in training data.")
        return {}
    if gas_index == -1:
        print(f"❌ Error: Gas '{gas_normalized}' not found in training data.")
        return {}
    
    # --- CRITICAL FIX: Slicing the Scaler ---
    # We only want to scale: [Lat, Lon, Duration, Year] (Indices 0, 1, 2, 3)
    # We deliberately IGNORE indices 4 and 5 (Sin/Cos) from the scaler file.
    means = scaler_model["means"][:4]
    stds = scaler_model["stds"][:4]
    
    # --- 3. Generate Sequence for Each Subsector ---
    for subsector in subsectors:
        subsector_index = indexers["subsector"].get(subsector, -1)

        if subsector_index == -1:
            # Skip unknown subsectors silently or with warning
            continue

        sequence = []

        # Generate 12-month sequence
        for month_offset in range(12): 
            current_month = start_month + month_offset
            current_year = start_year + (current_month - 1) // 12
            
            # 1-based index (1=Jan, 12=Dec)
            month_cycle_idx = (current_month - 1) % 12 + 1
            
            # --- Feature Group A: Scaled Features ---
            duration = get_month_duration(current_year, month_cycle_idx)
            
            # Create array for [Lat, Lon, Duration, Year]
            feats_to_scale = np.array([lat, lon, duration, current_year], dtype=np.float64)
            
            # Apply Standardization: (X - Mean) / Std
            scaled_part = (feats_to_scale - means) / stds
            
            # --- Feature Group B: Raw Cyclic Features ---
            # Calculated directly (-1.0 to 1.0) without scaling
            month_sin = np.sin(2 * m.pi * month_cycle_idx / 12)
            month_cos = np.cos(2 * m.pi * month_cycle_idx / 12)
            
            raw_seasonality = np.array([month_sin, month_cos], dtype=np.float64)
            
            # --- Combine ---
            final_numerical = np.concatenate([scaled_part, raw_seasonality])

            timestep = [
                iso3_country_index,
                sector_index,
                subsector_index,
                gas_index,
                *final_numerical.tolist(),
            ]

            sequence.append(timestep)
            
        results[subsector] = np.array(sequence)
        
    return results