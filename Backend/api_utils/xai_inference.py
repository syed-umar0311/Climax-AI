import numpy as np
import tensorflow as tf
from .preprocessing import preprocess_input
from .xai_model_wrapper import get_differentiable_model
from .xai_core import compute_integrated_gradients

def run_xai_inference(user_input, model, scaler, indexers):
    """
    Main XAI Pipeline:
    1. Preprocess Input -> Indices & Scaled Numbers
    2. Extract Embeddings (Target) & Zeros (Baseline)
    3. Run Integrated Gradients
    4. Aggregate scores into human-readable format
    """
    
    # --- 1. Preprocess Single Input ---
    preprocessed_dict = preprocess_input(user_input, scaler, indexers)
    
    if not preprocessed_dict:
        return {"error": "Invalid input features"}
        
    # Just grab the first subsector available to explain
    target_sub = list(preprocessed_dict.keys())[0]
    sequence_data = preprocessed_dict[target_sub] # Shape (12, 10)
    
    # Expand dims to make it a batch of 1: (1, 12, 10)
    sequence_data = np.expand_dims(sequence_data, axis=0)
    
    # Separate Features
    idx_country = sequence_data[:, :, 0]
    idx_sector = sequence_data[:, :, 1]
    idx_sub = sequence_data[:, :, 2]
    idx_gas = sequence_data[:, :, 3]
    val_numerical = sequence_data[:, :, 4:].astype(np.float32)

    # --- 2. Get Embeddings (Target) ---
    emb_c = model.get_layer("emb_country")(idx_country)
    emb_s = model.get_layer("emb_sector")(idx_sector)
    emb_sub = model.get_layer("emb_subsector")(idx_sub)
    emb_g = model.get_layer("emb_gas")(idx_gas)
    
    target_inputs = [emb_c, emb_s, emb_sub, emb_g, tf.convert_to_tensor(val_numerical)]
    
    # --- 3. Create Baselines (Zero Information) ---
    baseline_inputs = [tf.zeros_like(t) for t in target_inputs]
    
    # --- 4. Run Integrated Gradients ---
    xai_model = get_differentiable_model(model)
    attrs = compute_integrated_gradients(xai_model, baseline_inputs, target_inputs)
    
    # --- 5. Aggregation (FIXED SLICING) ---
    # attrs[4] is the numerical attribution with shape (12, 6) -> (Time, Features)
    # Previous code tried [:, :, 0:2] which assumed (Batch, Time, Features)
    
    results = {
        "features": {
            "Country": float(np.sum(np.abs(attrs[0]))),
            "Sector": float(np.sum(np.abs(attrs[1]))),
            "Subsector": float(np.sum(np.abs(attrs[2]))),
            "Gas": float(np.sum(np.abs(attrs[3]))),
        },
        "numerical_breakdown": {
            # FIXED: Removed the extra colon. Now indexing [Time, Feature]
            "Location (Lat/Lon)": float(np.sum(np.abs(attrs[4][:, 0:2]))), # Indices 0,1
            "Year Trend": float(np.sum(np.abs(attrs[4][:, 3]))),           # Index 3
            "Seasonality": float(np.sum(np.abs(attrs[4][:, 4:6])))         # Indices 4,5 (Sin/Cos)
        }
    }
    
    # Normalize to percentages
    total_score = sum(results["features"].values()) + sum(results["numerical_breakdown"].values())
    if total_score == 0: total_score = 1 
    
    final_explanation = {}
    for k, v in results["features"].items():
        final_explanation[k] = round((v / total_score) * 100, 2)
        
    for k, v in results["numerical_breakdown"].items():
        final_explanation[k] = round((v / total_score) * 100, 2)

    return {
        "target_subsector": target_sub,
        "importance_scores": final_explanation
    }