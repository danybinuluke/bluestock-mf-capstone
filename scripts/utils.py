"""
Utility functions for data validation and general operations.
"""
import pandas as pd
from typing import List
import logging

logger = logging.getLogger(__name__)

def validate_amfi_codes(master_df: pd.DataFrame, history_df: pd.DataFrame, col_name: str = 'amfi_code') -> List[int]:
    """
    Validate that every AMFI code in fund_master exists in nav_history.
    
    Args:
        master_df (pd.DataFrame): The fund_master dataframe.
        history_df (pd.DataFrame): The nav_history dataframe.
        col_name (str): The column name representing the AMFI code.
        
    Returns:
        List[int]: A list of missing AMFI codes.
    """
    if col_name not in master_df.columns or col_name not in history_df.columns:
        logger.error(f"Column '{col_name}' missing from datasets.")
        return []
        
    master_codes = set(master_df[col_name].dropna().astype(int))
    history_codes = set(history_df[col_name].dropna().astype(int))
    
    missing_codes = master_codes - history_codes
    return list(missing_codes)
