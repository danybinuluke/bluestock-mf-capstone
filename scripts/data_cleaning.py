import pandas as pd
import logging
from pathlib import Path
import os
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# Ensure processed directory exists
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names: lowercase, strip whitespace, replace spaces with underscores."""
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_').str.replace(r'[^a-z0-9_]', '', regex=True)
    return df

def remove_duplicates_and_log(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """Remove duplicates and log the count."""
    initial_len = len(df)
    df = df.drop_duplicates()
    final_len = len(df)
    if initial_len != final_len:
        logger.info(f"{dataset_name}: Removed {initial_len - final_len} duplicates.")
    return df

def parse_dates(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """Parse specified columns or auto-detect date columns."""
    if columns is None:
        columns = [col for col in df.columns if 'date' in col.lower() or 'month' in col.lower() or 'time' in col.lower()]
    for col in columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], format='mixed', dayfirst=True)
            except Exception as e:
                logger.warning(f"Could not parse date column {col}: {e}")
    return df

def clean_nav_history() -> None:
    logger.info("Cleaning nav_history.csv...")
    try:
        df = pd.read_csv(RAW_DIR / "02_nav_history.csv")
        df = standardize_columns(df)
        df = parse_dates(df, ["date"])
        
        # Sort by amfi_code and date
        if 'amfi_code' in df.columns and 'date' in df.columns:
            df = df.sort_values(by=["amfi_code", "date"])
        
        df = remove_duplicates_and_log(df, "nav_history")
        
        # Validate NAV > 0
        if 'nav' in df.columns:
            df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
            invalid_nav_count = len(df[df['nav'] <= 0])
            if invalid_nav_count > 0:
                logger.warning(f"Found {invalid_nav_count} invalid NAV values (<=0). Setting to NaN.")
                df.loc[df['nav'] <= 0, 'nav'] = pd.NA
            
            # Forward-fill missing NAV values for weekends/holidays per amfi_code
            if 'amfi_code' in df.columns:
                df['nav'] = df.groupby('amfi_code')['nav'].ffill()
                df['nav'] = df.groupby('amfi_code')['nav'].bfill() # bfill just in case first is nan
        
        df.to_csv(PROCESSED_DIR / "clean_nav_history.csv", index=False)
        logger.info("Saved clean_nav_history.csv")
    except Exception as e:
        logger.error(f"Error cleaning nav_history: {e}")

def clean_investor_transactions() -> None:
    logger.info("Cleaning investor_transactions.csv...")
    try:
        df = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
        df = standardize_columns(df)
        df = parse_dates(df, ["transaction_date"])
        
        # Standardize transaction_type
        if 'transaction_type' in df.columns:
            valid_types = ['SIP', 'Lumpsum', 'Redemption']
            # Uppercase SIP, Capitalize others
            df['transaction_type'] = df['transaction_type'].str.title()
            df.loc[df['transaction_type'].str.upper() == 'SIP', 'transaction_type'] = 'SIP'
            # Filter only allowed values
            df = df[df['transaction_type'].isin(valid_types)]
            logger.info(f"Transaction types standardized. Value counts: \n{df['transaction_type'].value_counts()}")
            
        # Validate amount_inr > 0
        if 'amount_inr' in df.columns:
            df['amount_inr'] = pd.to_numeric(df['amount_inr'], errors='coerce')
            invalid_amount = len(df[df['amount_inr'] <= 0])
            if invalid_amount > 0:
                logger.warning(f"Found {invalid_amount} invalid amount_inr values (<=0).")
                df = df[df['amount_inr'] > 0]
                
        # Validate KYC status
        if 'kyc_status' in df.columns:
            valid_kyc = ['Verified', 'Pending']
            df['kyc_status'] = df['kyc_status'].str.capitalize()
            df.loc[~df['kyc_status'].isin(valid_kyc), 'kyc_status'] = 'Pending' # Defaulting or could mark as invalid
            
        df = remove_duplicates_and_log(df, "investor_transactions")
        
        df.to_csv(PROCESSED_DIR / "clean_investor_transactions.csv", index=False)
        logger.info("Saved clean_investor_transactions.csv")
    except Exception as e:
        logger.error(f"Error cleaning investor_transactions: {e}")

def clean_scheme_performance() -> None:
    logger.info("Cleaning scheme_performance.csv...")
    try:
        df = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")
        df = standardize_columns(df)
        
        numeric_cols = [
            'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 
            'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio', 
            'std_dev_ann_pct', 'max_drawdown_pct', 'expense_ratio_pct'
        ]
        
        # Validate numeric columns
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Validate expense_ratio_pct BETWEEN 0.1 AND 2.5
        if 'expense_ratio_pct' in df.columns:
            invalid_er = len(df[(df['expense_ratio_pct'] < 0.1) | (df['expense_ratio_pct'] > 2.5)])
            if invalid_er > 0:
                logger.warning(f"Found {invalid_er} expense_ratio_pct outside [0.1, 2.5]. Setting to NaN.")
                df.loc[(df['expense_ratio_pct'] < 0.1) | (df['expense_ratio_pct'] > 2.5), 'expense_ratio_pct'] = pd.NA
        
        # Flag anomalies (e.g., returns > 100% or < -100%) - simple boolean flag column
        df['anomaly_flag'] = False
        if 'return_1yr_pct' in df.columns:
            df.loc[(df['return_1yr_pct'] > 100) | (df['return_1yr_pct'] < -100), 'anomaly_flag'] = True
        
        df = remove_duplicates_and_log(df, "scheme_performance")
        
        df.to_csv(PROCESSED_DIR / "clean_scheme_performance.csv", index=False)
        logger.info("Saved clean_scheme_performance.csv")
    except Exception as e:
        logger.error(f"Error cleaning scheme_performance: {e}")

def clean_generic(filename: str) -> None:
    dataset_name = filename.replace('.csv', '')
    logger.info(f"Cleaning {filename}...")
    try:
        df = pd.read_csv(RAW_DIR / filename)
        df = standardize_columns(df)
        df = parse_dates(df)
        df = remove_duplicates_and_log(df, dataset_name)
        
        clean_filename = f"clean_{filename.split('_', 1)[-1]}" if filename[0].isdigit() else f"clean_{filename}"
        if filename[0].isdigit() and filename[1].isdigit() and filename[2] == '_':
             clean_filename = f"clean_{filename[3:]}"
             
        df.to_csv(PROCESSED_DIR / clean_filename, index=False)
        logger.info(f"Saved {clean_filename}")
    except Exception as e:
        logger.error(f"Error cleaning {filename}: {e}")

def main():
    logger.info("Starting data cleaning process...")
    
    special_files = ["02_nav_history.csv", "08_investor_transactions.csv", "07_scheme_performance.csv"]
    
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    
    # Process remaining files
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv") and file not in special_files:
            clean_generic(file)
            
    logger.info("Data cleaning completed successfully.")

if __name__ == "__main__":
    main()
