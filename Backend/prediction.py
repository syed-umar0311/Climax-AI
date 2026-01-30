import os
import sys
import calendar
import copy  # <--- Needed for duplicating input
import numpy as np

# Ensure we can import from api_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_utils.model_loader import load_model, load_scaler, load_indexers
from api_utils.inference import run_inference

if __name__ == '__main__':
    print("\n--- Initializing Prediction Pipeline ---")

    # 1. Load Assets
    try:
        MODEL = load_model()
        SCALER = load_scaler()
        INDEXERS = load_indexers()
        print("✅ Model and assets loaded successfully.")
    except Exception as e:
        print(f"❌ FATAL ERROR loading assets: {e}")
        exit(1)

    # 2. Define User Input
    USER_INPUT = {
        'country': 'PAK',
        'sector': 'transportation',  # Ensure correct spelling/case
        'gas': 'n2o',                # This is the primary gas for the detailed report
        'year': 2030,
        'month': 1
    }

    # 3. Run Prediction
    print(f"\n--- RUNNING PREDICTION FOR {USER_INPUT['country']} ---")
    
    try:
        # --- A. Main Inference (For the detailed report) ---
        results = run_inference(USER_INPUT, MODEL, SCALER, INDEXERS)
        
        # --- B. Gas Composition Analysis (Multi-Pass) ---
        # We run the model 3 times to get the ratios
        print("   ... Calculating gas composition ratios ...")
        gas_types = ['co2', 'ch4', 'n2o']
        gas_totals = {}
        
        for g in gas_types:
            # Create temp input
            temp_input = copy.deepcopy(USER_INPUT)
            temp_input['gas'] = g
            
            # Run quiet inference
            try:
                res = run_inference(temp_input, MODEL, SCALER, INDEXERS)
                gas_totals[g] = float(res['total_emissions'])
            except Exception:
                gas_totals[g] = 0.0

        grand_total = sum(gas_totals.values())

        # --- C. DISPLAY RESULTS ---
        print("\n" + "="*60)
        print(f"FINAL PREDICTION SUMMARY: {USER_INPUT['sector'].upper()} SECTOR")
        print("="*60)
        print(f"Region: {USER_INPUT['country']}")
        print(f"Forecast Start: {USER_INPUT['year']} - Month {USER_INPUT['month']}")
        
        # 1. GAS COMPOSITION TABLE (New Section)
        print("\n" + "-"*60)
        print("🧪 GAS COMPOSITION ANALYSIS")
        print("-" * 60)
        print(f"{'Gas Type':<10} | {'Total Emissions (Tonnes)':<25} | {'Composition %':<15}")
        print("-" * 60)
        
        if grand_total > 0:
            for g in gas_types:
                val = gas_totals[g]
                pct = (val / grand_total) * 100
                print(f"{g.upper():<10} | {val:,.2f}{'':<18} | {pct:>6.2f}%")
            
            print("-" * 60)
            print(f"{'TOTAL':<10} | {grand_total:,.2f}{'':<18} | 100.00%")
        else:
            print("⚠️ No emissions detected for any gas type.")

        # 2. DETAILED BREAKDOWN (For the primary requested gas)
        total_primary = results['total_emissions']
        if total_primary > 0:
            print("\n" + "-"*60)
            print(f"📅 DETAILED FORECAST FOR REQUESTED GAS: {USER_INPUT['gas'].upper()}")
            print("-" * 60)
            
            # Aggregate Monthly
            start_m = USER_INPUT['month']
            start_y = USER_INPUT['year']
            
            print("\n(Monthly Trends - All Subsectors Combined)")
            for i, emission_val in enumerate(results['monthly_emissions']):
                curr_m_idx = ((start_m + i - 1) % 12) + 1
                curr_y = start_y + ((start_m + i - 1) // 12)
                month_name = calendar.month_name[curr_m_idx]
                print(f"  {month_name} {curr_y}: \t{emission_val:,.2f}")

            # Subsector Breakdown
            print("\n(Breakdown by Subsector)")
            for sub, data in results['subsector_emissions'].items():
                sub_total = data['total_emissions']
                print(f"\n🔹 {sub.upper()} (Total: {sub_total:,.2f})")
                
                # Small table for subsector months
                # print(f"   {'Month':<15} | {'Emissions':<15}")
                # (Optional: Uncomment below to see every month for every subsector)
                # for i, emission_val in enumerate(data['monthly_emissions']):
                #     curr_m_idx = ((start_m + i - 1) % 12) + 1
                #     month_name = calendar.month_name[curr_m_idx]
                #     print(f"   {month_name[:3]:<15} | {emission_val:,.2f}")

        else:
            print(f"\n⚠️ No data found for the specific requested gas: {USER_INPUT['gas']}")

    except Exception as e:
        print(f"❌ Error during inference: {e}")
        import traceback
        traceback.print_exc()