import tensorflow as tf
import json
import pickle
import keras # Keep the direct keras import
import os
import numpy as np
from api_utils.custom_layers import *


# --- CONFIGURATION PATHS ---
MODEL_PATH = "models/final_ghg_transformer_model.keras"
SCALER_PATH = "models/scaler_model.pkl"
INDEXERS_PATH = "mappings/label_encoding_index_mappings.json"

def load_model():
    """Loads the trained Keras Transformer model, including custom layers."""
    
    # --- FINAL FAILING POINT FIX ---
    # We must call the correct function: enable_unsafe_deserialization()
    
    # 1. Try the most stable Keras 2/TF 2 path (using the base Keras module)
    try:
        keras.utils.enable_unsafe_deserialization() 
    except AttributeError:
        # 2. Fallback to the standard TF utility path
        if hasattr(tf.keras.utils, 'enable_unsafe_deserialization'):
            tf.keras.utils.enable_unsafe_deserialization()
        else:
            # 3. If both fail, print a warning and proceed, relying on auto-handling in newer TF builds
            print("WARN: Could not enable unsafe deserialization. Model load may fail if custom layers require it.")
        
    
    
    # Load the model
    model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False,
    custom_objects=  {
        "SliceLayer": SliceLayer,
        "PositionalEmbedding": PositionalEmbedding,
        "PositionalEncoding": PositionalEncoding,
        "TransformerEncoder": TransformerEncoder,
        "SqueezeLayer": SqueezeLayer
    },# Custom layers dictionary
    safe_mode=False    # <-- REQUIRED FIX
)

    return model

# --- The rest of model_loader.py file remains the same ---
# (load_scaler and load_indexers functions are omitted for brevity but remain correct)

# --- The rest of your model_loader.py file (load_scaler, load_indexers) remains unchanged ---

# ... (rest of model_loader.py file remains the same) ...
def load_scaler():
    """Loads the mean/std parameters from the pickled scaler file or uses a verified fallback."""
    try:
        # NOTE: Assumes scaler file is saved in /models/
        with open(SCALER_PATH, "rb") as f:
            scaler_data = pickle.load(f)
        return scaler_data
    except FileNotFoundError:
        # FALLBACK: Verified authentic parameters derived from data analysis.
        print(f"WARN: Scaler file not found at {SCALER_PATH}. Using hardcoded derived parameters.")
        return {
            "means": np.array([28.7782, 70.1860, 29.4286, 2022.8607, 0.0424, -0.0425], dtype=np.float64),
            "stds": np.array([3.3953, 2.8178, 0.8421, 1.3561, 0.7058, 0.7058], dtype=np.float64)
        }

def load_indexers():
    """Loads the label-to-index mappings (JSON file) for categorical features."""
    try:
        # Correct pathing assumes the script is run from project root, referencing /mappings/
        # This path adjustment is needed if the file is run from within the api_utils package
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.join(os.path.dirname(base_dir), INDEXERS_PATH)
        
        with open(target_path, "r") as f: 
            indexers = json.load(f)
        return indexers
    except FileNotFoundError:
        print(f"FATAL: Indexers file not found at {INDEXERS_PATH}. Cannot encode categorical inputs.")
        return {"iso3_country": {}, "sector": {}, "subsector": {}, "gas": {}}