import pickle
from pathlib import Path
import os

# Path to the root of the project (the folder containing "report", "python-package", etc.)
project_root = Path(__file__).resolve().parents[1]

# Path to the model.pkl inside the assets directory
model_path = project_root / "assets" / "model.pkl"

def load_model():
    with model_path.open('rb') as file:
        model = pickle.load(file)
    return model