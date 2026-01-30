import numpy as np
from .preprocessing import preprocess_input

def run_inference(user_input, model, scaler_model, indexers):
    """
    Runs the forward pass on the model for all relevant subsectors.
    FIXED: Splits inputs into the 5 tensors the model expects.
    """
    
    # 1. Generate sequences
    preprocessed_data = preprocess_input(user_input, scaler_model, indexers)

    response = {
        "subsector_emissions": {},
        "monthly_emissions": [0.0] * 12,
        "total_emissions": 0.0
    }

    # 2. Loop through each subsector found
    for subsector, sequence in preprocessed_data.items():
        # Sequence shape: (12, 10) -> We add batch dim: (1, 12, 10)
        sequence = np.expand_dims(sequence, axis=0)

        # --- CRITICAL FIX: Split inputs to match Model Architecture ---
        # The model expects 5 separate inputs, NOT 2.
        
        # inputs=[cat_input_country, cat_input_sector, cat_input_subsector, cat_input_gas, num_input]
        
        # Extract columns based on preprocessing order: [country, sector, subsector, gas, ...numerical...]
        cat_country   = sequence[:, :, 0]  # Shape (1, 12)
        cat_sector    = sequence[:, :, 1]
        cat_subsector = sequence[:, :, 2]
        cat_gas       = sequence[:, :, 3]
        
        num_input     = sequence[:, :, 4:] # Shape (1, 12, 6)

        # 3. Predict
        try:
            predictions = model.predict(
                [cat_country, cat_sector, cat_subsector, cat_gas, num_input], 
                verbose=0
            )[0] # Get first batch result -> Shape (12,)
        except Exception as e:
            print(f"Prediction Error for {subsector}: {e}")
            continue
        
        # 4. Inverse Transformation (Log -> Actual)
        # Ensure no negative emissions due to float precision
        emissions = np.maximum(np.expm1(predictions), 0).tolist()

        total = sum(emissions)
        response["subsector_emissions"][subsector] = {
            "monthly_emissions": emissions,
            "total_emissions": total
        }

        # 5. Aggregate
        response["monthly_emissions"] = [sum(x) for x in zip(response["monthly_emissions"], emissions)]
        response["total_emissions"] += total

    return response