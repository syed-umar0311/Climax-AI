from api_utils.xai_inference import run_xai_inference
from flask import Flask, request, jsonify
from flask_cors import CORS 
import numpy as np
import os
import sys
import copy  # <--- NEW IMPORT needed for copying dictionaries

# 1. Setup Path to import from api_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Import your custom logic
from api_utils.model_loader import load_model, load_scaler, load_indexers
from api_utils.inference import run_inference

# 3. Initialize Flask Application
app = Flask(__name__)
CORS(app) 

# --- GLOBAL ASSET LOADING ---
print("--- Initializing API Server ---")
try:
    print("Loading Model and Scalers...")
    MODEL = load_model()
    SCALER = load_scaler()
    INDEXERS = load_indexers()
    print("✅ System Ready. Model loaded successfully.")
except Exception as e:
    print(f"❌ FATAL ERROR: Could not load assets. Server cannot start.\n{e}")
    exit(1)

# --- API ENDPOINTS ---

@app.route('/api/explain', methods=['POST'])
def explain_prediction():
    """
    Returns feature importance scores explaining WHY the model made its prediction.
    """
    try:
        data = request.json
        
        user_input = {
            'country': data['country'],
            'sector': data['sector'],
            'gas': data['gas'],
            'year': int(data.get('year', 2025)),
            'month': int(data.get('month', 1)),
            'lat': data.get('lat'), 
            'lon': data.get('lon')
        }
        
        explanation = run_xai_inference(user_input, MODEL, SCALER, INDEXERS)
        
        if "error" in explanation:
            return jsonify(explanation), 400
            
        return jsonify({
            "status": "success",
            "meta": user_input,
            "data": explanation
        })

    except Exception as e:
        print(f"XAI Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online", "message": "GHG Prediction API is running"})

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint.
    Returns:
    1. Detailed predictions for the REQUESTED gas.
    2. A new 'gas_composition' object with ratios for CO2, CH4, N2O.
    """
    try:
        # A. Parse Input
        data = request.json
        print(f"\n📩 Received Request: {data}")

        required = ['country', 'sector', 'gas']
        if not all(k in data for k in required):
            return jsonify({"error": "Missing required fields (country, sector, gas)"}), 400

        # C. Prepare Input for Inference Engine
        user_input = {
            'country': data['country'],
            'sector': data['sector'],
            'gas': data['gas'],
            'year': int(data.get('year', 2025)),
            'month': int(data.get('month', 1)),
            'lat': data.get('lat'), 
            'lon': data.get('lon')
        }

        # --- STEP 1: Main Prediction (For the requested Gas) ---
        results = run_inference(user_input, MODEL, SCALER, INDEXERS)

        # --- STEP 2: Gas Ratio Calculation (Multi-Pass Inference) ---
        # We run the model 3 times (CO2, CH4, N2O) to compare their totals
        gas_types = ['co2', 'ch4', 'n2o']
        gas_totals = {}
        
        print(f"   ... Calculating ratios for {user_input['sector']} ...")
        
        for g in gas_types:
            # Create a temporary input just for this calculation
            temp_input = copy.deepcopy(user_input)
            temp_input['gas'] = g
            
            # Run inference quietly
            try:
                res = run_inference(temp_input, MODEL, SCALER, INDEXERS)
                gas_totals[g] = float(res['total_emissions'])
            except Exception:
                # If model fails (e.g., sector doesn't emit this gas), assume 0
                gas_totals[g] = 0.0

        # Calculate Percentages
        grand_total_all_gases = sum(gas_totals.values())
        gas_ratios = {}
        
        if grand_total_all_gases > 0:
            for g, total in gas_totals.items():
                percent = (total / grand_total_all_gases) * 100
                gas_ratios[g] = round(percent, 2)
        else:
            # Handle edge case where all predictions are 0
            gas_ratios = {g: 0.0 for g in gas_types}

        # --- STEP 3: Structure Response ---
        response = {
            "status": "success",
            "meta": {
                "country": user_input['country'],
                "sector": user_input['sector'],
                "year": user_input['year'],
                "requested_gas": user_input['gas']
            },
            "data": {
                # Original Data for the requested gas
                "total_emissions": float(results['total_emissions']),
                "monthly_trends": [float(x) for x in results['monthly_emissions']],
                "subsector_breakdown": [],
                
                # NEW: Gas Composition Data
                "gas_composition": {
                    "ratios": gas_ratios,           # e.g., {"co2": 80.5, "ch4": 19.5, "n2o": 0}
                    "absolute_totals": gas_totals,  # e.g., {"co2": 5000.0, "ch4": 1200.0...}
                    "total_combined": float(grand_total_all_gases)
                }
            }
        }

        # Format subsector data nicely for charts
        for sub, details in results['subsector_emissions'].items():
            response["data"]["subsector_breakdown"].append({
                "name": sub,
                "total": float(details['total_emissions']),
                "monthly": [float(x) for x in details['monthly_emissions']]
            })

        return jsonify(response)

    except Exception as e:
        print(f"❌ Error processing request: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Server starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)