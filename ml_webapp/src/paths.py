import os

# Root directory (project root, 2 levels above src/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Artifacts paths
ARTIFACTS_DIR = os.path.join(ROOT_DIR, "artifacts")
BEST_MODEL_PATH = os.path.join(ARTIFACTS_DIR, "best_model.pkl")
PREPROCESSOR_PATH = os.path.join(ARTIFACTS_DIR, "preprocessor.pkl")

# Ensure artifacts folder exists
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
