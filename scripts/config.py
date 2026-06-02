"""
Configuration settings for the Bluestock Mutual Fund Capstone Project.
"""
from pathlib import Path

# Project Root Directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
LIVE_NAV_DIR = RAW_DATA_DIR / "live_nav"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DB_DIR = DATA_DIR / "db"

# Logs and Reports Directory
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Ensure all structural directories exist
for directory in [RAW_DATA_DIR, LIVE_NAV_DIR, PROCESSED_DATA_DIR, DB_DIR, LOGS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Mutual Fund API Base URL
MF_API_BASE_URL = "https://api.mfapi.in/mf"

# Target Schemes for Live NAV Fetching
TARGET_SCHEMES = [
    "125497",  # HDFC Top 100 Direct
    "119551",  # SBI Bluechip
    "120503",  # ICICI Bluechip
    "118632",  # Nippon Large Cap
    "119092",  # Axis Bluechip
    "120841"   # Kotak Bluechip
]

# Logging Format
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
