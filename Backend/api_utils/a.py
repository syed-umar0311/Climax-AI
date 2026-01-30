import sys
import platform
import tensorflow as tf
import keras

print("--- Installed Versions ---")
print(f"Python Version: {platform.python_version()} (Running on {sys.executable})")
print(f"TensorFlow Version: {tf.__version__}")
print(f"Keras Version: {keras.__version__}")