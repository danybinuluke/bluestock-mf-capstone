"""
ETL Pipeline Orchestrator.
Orchestrates data ingestion, NAV fetching, and AMFI code validation.
"""
import logging
import pandas as pd
from pathlib import Path

from config import LOGS_DIR, LOGGING_FORMAT, RAW_DATA_DIR, PROCESSED_DATA_DIR
import data_ingestion
import live_nav_fetch
from utils import validate_amfi_codes

log_file = LOGS_DIR / "etl_pipeline.log"
logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Run the entire ETL pipeline."""
    logger.info("=== STARTING ETL PIPELINE ===")
    
    # 1. Run data ingestion
    logger.info("=== STEP 1: Running Data Ingestion ===")
    try:
        data_ingestion.main()
    except Exception as e:
        logger.error(f"Data ingestion failed: {e}")
    
    # 2. Run NAV fetch
    logger.info("=== STEP 2: Running Live NAV Fetch ===")
    try:
        live_nav_fetch.main()
    except Exception as e:
        logger.error(f"Live NAV fetch failed: {e}")
    
    # 3. Run validation (fund_master.csv vs nav_history.csv)
    logger.info("=== STEP 3: Validating AMFI Codes ===")
    master_path = RAW_DATA_DIR / "01_fund_master.csv"
    history_path = RAW_DATA_DIR / "02_nav_history.csv"
    
    if master_path.exists() and history_path.exists():
        try:
            master_df = pd.read_csv(master_path)
            history_df = pd.read_csv(history_path)
            
            missing_codes = validate_amfi_codes(master_df, history_df, col_name='amfi_code')
            
            if missing_codes:
                missing_df = pd.DataFrame({"missing_amfi_code": missing_codes})
                missing_path = PROCESSED_DATA_DIR / "missing_scheme_codes.csv"
                missing_df.to_csv(missing_path, index=False)
                logger.warning(f"Found {len(missing_codes)} missing AMFI codes in nav_history. Saved to {missing_path.name}")
            else:
                logger.info("Validation Successful: All AMFI codes from fund_master exist in nav_history.")
        except Exception as e:
            logger.error(f"Error during validation: {e}")
    else:
        logger.warning("Validation skipped: 01_fund_master.csv or 02_nav_history.csv not found.")
        
    logger.info("=== ETL PIPELINE COMPLETED ===")

if __name__ == "__main__":
    main()
