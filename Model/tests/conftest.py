import os
import sys


MODEL_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if MODEL_ROOT not in sys.path:
    sys.path.insert(0, MODEL_ROOT)
