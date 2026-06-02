"""
Live NAV Fetching Script.
Retrieves and saves NAV history and metadata for target schemes from mfapi.in.
"""
import requests
import pandas as pd
import logging
import time
from typing import Dict, Any, Optional, List

from config import LIVE_NAV_DIR, MF_API_BASE_URL, TARGET_SCHEMES, LOGS_DIR, LOGGING_FORMAT

log_file = LOGS_DIR / "live_nav_fetch.log"
logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_nav_data(scheme_code: str, retries: int = 3, timeout: int = 15) -> Optional[Dict[str, Any]]:
    """Fetch NAV data from the API with retries and timeout."""
    url = f"{MF_API_BASE_URL}/{scheme_code}"
    
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Fetching NAV for {scheme_code} (Attempt {attempt}/{retries})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "SUCCESS":
                return data
            else:
                logger.warning(f"API success status missing for {scheme_code}")
                return None
        except requests.exceptions.Timeout:
            logger.error(f"Timeout occurred for {scheme_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {scheme_code}: {e}")
            
        time.sleep(2)  # Delay between retries
        
    return None

def main():
    """Execute live NAV fetching pipeline."""
    logger.info("Starting Live NAV Fetching")
    
    metadata_records: List[Dict[str, Any]] = []
    
    for scheme_code in TARGET_SCHEMES:
        data = fetch_nav_data(scheme_code)
        if data:
            meta = data.get("meta", {})
            nav_data = data.get("data", [])
            
            # Extract metadata
            metadata_records.append({
                "scheme_code": meta.get("scheme_code", scheme_code),
                "scheme_name": meta.get("scheme_name", ""),
                "fund_house": meta.get("fund_house", ""),
                "scheme_type": meta.get("scheme_type", ""),
                "scheme_category": meta.get("scheme_category", "")
            })
            
            # Extract and Save NAV history
            if nav_data:
                nav_df = pd.DataFrame(nav_data)
                nav_csv_path = LIVE_NAV_DIR / f"nav_{scheme_code}.csv"
                nav_df.to_csv(nav_csv_path, index=False)
                logger.info(f"Saved NAV data to {nav_csv_path.name}")
            else:
                logger.warning(f"No NAV historical data found for {scheme_code}")
                
    if metadata_records:
        meta_df = pd.DataFrame(metadata_records)
        meta_csv_path = LIVE_NAV_DIR / "nav_metadata.csv"
        meta_df.to_csv(meta_csv_path, index=False)
        logger.info(f"Saved aggregated metadata to {meta_csv_path.name}")

    logger.info("Live NAV Fetching Completed")

if __name__ == "__main__":
    main()
