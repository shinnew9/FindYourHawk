# modules/constants.py (새 파일 하나 만들기!)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OPPORTUNITIES_CSV = DATA_DIR / "opportunities.csv"
