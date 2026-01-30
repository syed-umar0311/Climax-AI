import json
import calendar
import os

# Define absolute path to mappings to avoid FileNotFoundError
# Assumes this file is in project_root/api_utils/utils.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Points to project_root/mappings/
MAPPINGS_DIR = os.path.join(BASE_DIR, "..", "mappings")

def load_json_mapping(filename):
    """
    Helper to load a JSON file from the mappings directory.
    """
    target_path = os.path.join(MAPPINGS_DIR, filename)
    try:
        with open(target_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ WARN: Mapping file '{filename}' not found at {target_path}.")
        return {}
    except json.JSONDecodeError:
        print(f"❌ ERROR: Could not decode JSON from '{filename}'.")
        return {}

# --- LOAD MAPPINGS FROM JSON FILES ---

# 1. Subsector Mapping (Sector -> List of Subsectors)
# Filename: subsector_mapping.json
# Structure: {"power": ["coal_fired_power", ...], ...}
SUBSECTOR_MAPPING = load_json_mapping("subsector_mapping.json")

# 2. Default Lat/Lon Mapping (Country -> {'lat': ..., 'lon': ...})
# Filename: default_lat_lon.json
# Structure: {"PAK": {"lat": 30.3753, "lon": 69.3451}, ...}
DEFAULT_LAT_LON = load_json_mapping("default_lat_lon.json")

# 3. Label Encoding Index Mappings (Category -> {Label: Index})
# Filename: label_encoding_index_mappings.json
# Structure: {"iso3_country": {"PAK": 0}, "sector": {...}, ...}
INDEX_MAPPINGS = load_json_mapping("label_encoding_index_mappings.json")


# --- UTILITY FUNCTIONS ---

def get_subsectors(sector):
    """
    Returns a list of subsectors for a given sector.
    Handles case sensitivity by converting input to lowercase keys if needed.
    """
    # Try exact match first
    if sector in SUBSECTOR_MAPPING:
        return SUBSECTOR_MAPPING[sector]
    
    # Fallback: Try lowercase match (e.g., "Power" -> "power")
    sector_lower = sector.lower()
    return SUBSECTOR_MAPPING.get(sector_lower, [])

def get_default_lat_lon(country):
    """
    Returns (lat, lon) tuple for a given country code (e.g., 'PAK').
    Returns (0.0, 0.0) if not found.
    """
    # The JSON structure is expected to be: {"PAK": {"lat": ..., "lon": ...}}
    country_data = DEFAULT_LAT_LON.get(country, {})
    
    # Extract lat/lon with defaults
    lat = country_data.get('lat', 0.0)
    lon = country_data.get('lon', 0.0)
    
    return (lat, lon)

def get_month_duration(year, month):
    """
    Returns the number of days in a specific month of a specific year.
    """
    return calendar.monthrange(year, month)[1]