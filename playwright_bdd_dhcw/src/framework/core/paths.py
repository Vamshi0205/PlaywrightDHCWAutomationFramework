from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]        # Defining the root directory of the project 
ARTIFACTS = ROOT / "artifacts" # Defining the artifacts directory path
ARTIFACTS.mkdir(parents=True, exist_ok=True) # Creating the artifacts directory if it doesn't exist
