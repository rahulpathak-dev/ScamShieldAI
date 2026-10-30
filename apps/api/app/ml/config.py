from pathlib import Path

API_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = API_ROOT.parent
ML_ROOT = PROJECT_ROOT / "ml"
DATA_ROOT = ML_ROOT / "data"
RAW_DATA_DIR = DATA_ROOT / "raw"
PROCESSED_DATA_DIR = DATA_ROOT / "processed"
MODEL_DIR = ML_ROOT / "models"
REPORT_DIR = ML_ROOT / "reports"

DEFAULT_DATASET_PATH = PROCESSED_DATA_DIR / "scam_messages.csv"
DEFAULT_CLASSICAL_MODEL_PATH = MODEL_DIR / "classical" / "best_model.joblib"
DEFAULT_MODEL_CARD_PATH = MODEL_DIR / "classical" / "model_card.json"

SCAM_LABEL = "scam"
SAFE_LABEL = "safe"
LABEL_TO_ID = {SAFE_LABEL: 0, SCAM_LABEL: 1}
ID_TO_LABEL = {0: SAFE_LABEL, 1: SCAM_LABEL}


def ensure_ml_directories() -> None:
    for path in (RAW_DATA_DIR, PROCESSED_DATA_DIR, MODEL_DIR, REPORT_DIR, MODEL_DIR / "classical", MODEL_DIR / "transformers"):
        path.mkdir(parents=True, exist_ok=True)