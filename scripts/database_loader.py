import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import logging
from pathlib import Path
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("data/db")
DB_PATH = DB_DIR / "bluestock_mf.db"
SCHEMA_PATH = Path("sql/schema.sql")

def setup_database():
    """Create database and execute schema.sql"""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run schema script
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    logger.info("Database initialized with schema.")

def populate_dim_date(engine, df_list):
    """Extract unique dates from multiple dataframes and populate dim_date"""
    logger.info("Populating dim_date...")
    all_dates = pd.Series(dtype='datetime64[ns]')
    
    for df, col in df_list:
        if col in df.columns:
            # Ensure datetime type
            df[col] = pd.to_datetime(df[col], errors='coerce')
            all_dates = pd.concat([all_dates, df[col].dropna()])
    
    unique_dates = all_dates.drop_duplicates()
    
    dim_date = pd.DataFrame({
        'date_id': unique_dates.dt.strftime('%Y-%m-%d'),
        'year': unique_dates.dt.year,
        'month': unique_dates.dt.month,
        'day': unique_dates.dt.day,
        'quarter': unique_dates.dt.quarter,
        'day_of_week': unique_dates.dt.dayofweek,
        'is_weekend': unique_dates.dt.dayofweek >= 5
    })
    
    dim_date = dim_date.drop_duplicates('date_id').dropna(subset=['date_id'])
    
    # Load into DB
    dim_date.to_sql('dim_date', con=engine, if_exists='append', index=False)
    logger.info(f"Loaded {len(dim_date)} records into dim_date.")
    return len(dim_date)

def load_data():
    setup_database()
    engine = create_engine(f'sqlite:///{DB_PATH}')
    
    # Load processed CSVs
    try:
        df_fund = pd.read_csv(PROCESSED_DIR / "clean_fund_master.csv")
        df_nav = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv")
        df_transactions = pd.read_csv(PROCESSED_DIR / "clean_investor_transactions.csv")
        df_perf = pd.read_csv(PROCESSED_DIR / "clean_scheme_performance.csv")
        df_aum = pd.read_csv(PROCESSED_DIR / "clean_aum_by_fund_house.csv")
    except Exception as e:
        logger.error(f"Error reading processed CSVs: {e}")
        return

    # Populate dim_date first
    populate_dim_date(engine, [
        (df_nav, 'date'),
        (df_transactions, 'transaction_date'),
        (df_aum, 'date'),
        (df_fund, 'launch_date')
    ])
    
    # Format dates in facts to string format YYYY-MM-DD
    if 'date' in df_nav.columns:
        df_nav['date'] = pd.to_datetime(df_nav['date']).dt.strftime('%Y-%m-%d')
    if 'transaction_date' in df_transactions.columns:
        df_transactions['transaction_date'] = pd.to_datetime(df_transactions['transaction_date']).dt.strftime('%Y-%m-%d')
    if 'date' in df_aum.columns:
        df_aum['date'] = pd.to_datetime(df_aum['date']).dt.strftime('%Y-%m-%d')
    if 'launch_date' in df_fund.columns:
         df_fund['launch_date'] = pd.to_datetime(df_fund['launch_date']).dt.strftime('%Y-%m-%d')

    tables_to_load = {
        'dim_fund': df_fund,
        'fact_nav': df_nav,
        'fact_transactions': df_transactions,
        'fact_performance': df_perf,
        'fact_aum': df_aum
    }
    
    summary = ["# Database Load Summary", ""]
    summary.append("| Table Name | CSV Rows | DB Rows | Match |")
    summary.append("|------------|----------|---------|-------|")
    
    for table_name, df in tables_to_load.items():
        logger.info(f"Loading {table_name}...")
        csv_rows = len(df)
        
        # Load to DB
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        
        # Verify
        with engine.connect() as conn:
            db_rows = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()[0]
        
        match = "Yes" if csv_rows == db_rows else "No"
        summary.append(f"| {table_name} | {csv_rows} | {db_rows} | {match} |")
        logger.info(f"{table_name}: CSV={csv_rows}, DB={db_rows}, Match={match}")
        
    # Write summary
    summary_path = Path("reports/database_load_summary.md")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w') as f:
        f.write("\n".join(summary))
    logger.info(f"Load summary written to {summary_path}")

if __name__ == "__main__":
    load_data()
