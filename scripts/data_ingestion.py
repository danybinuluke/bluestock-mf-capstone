"""
Data Ingestion Script.
Scans data/raw for CSV files, generating a dataset summary and data quality report.
"""
import pandas as pd
from pathlib import Path
import logging
import json
from typing import Dict, Any, List

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, LOGS_DIR, LOGGING_FORMAT, PROJECT_ROOT

# Configure Logging
log_file = LOGS_DIR / "data_ingestion.log"
logging.basicConfig(
    level=logging.INFO,
    format=LOGGING_FORMAT,
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def detect_potential_columns(df: pd.DataFrame, keywords: List[str]) -> List[str]:
    """Identify columns that might match specific concepts based on name."""
    return [col for col in df.columns if any(kw in col.lower() for kw in keywords)]

def process_csv_file(file_path: Path) -> Dict[str, Any]:
    """Process a single CSV file and return summary metrics."""
    logger.info(f"Processing file: {file_path.name}")
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        logger.warning(f"File is empty: {file_path.name}")
        return {}
    except Exception as e:
        logger.error(f"Failed to read {file_path.name}: {e}")
        return {}

    # Print requested details to console
    print(f"\n{'='*50}\nFilename: {file_path.name}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data Types:\n{df.dtypes}")
    print(f"First 5 Rows:\n{df.head(5)}")

    # Calculate metrics
    missing_vals = int(df.isnull().sum().sum())
    dup_rows = int(df.duplicated().sum())
    memory_usage = float(df.memory_usage(deep=True).sum() / (1024 * 1024)) # MB
    
    date_cols = detect_potential_columns(df, ['date', 'month', 'year'])
    id_cols = detect_potential_columns(df, ['id', 'code', 'amfi'])

    return {
        'filename': file_path.name,
        'rows': df.shape[0],
        'columns': df.shape[1],
        'missing_values': missing_vals,
        'duplicate_rows': dup_rows,
        'memory_usage_mb': memory_usage,
        'potential_date_cols': date_cols,
        'potential_id_cols': id_cols,
        'dtypes_dict': df.dtypes.astype(str).to_dict()
    }

def generate_quality_report(summaries: List[Dict[str, Any]], report_path: Path) -> None:
    """Generate a Markdown data quality report."""
    if not summaries:
        logger.warning("No summaries generated.")
        return
        
    total_datasets = len(summaries)
    total_rows = sum(s['rows'] for s in summaries)
    
    with open(report_path, 'w') as f:
        f.write("# Data Quality Summary\n\n")
        f.write(f"- **Total Datasets**: {total_datasets}\n")
        f.write(f"- **Total Rows**: {total_rows}\n\n")
        
        f.write("## Dataset Summaries\n\n")
        for s in summaries:
            f.write(f"### {s['filename']}\n")
            f.write(f"- **Null Summary**: {s['missing_values']} missing values\n")
            f.write(f"- **Duplicate Summary**: {s['duplicate_rows']} duplicate rows\n")
            
            f.write(f"- **Key Findings**:\n")
            f.write(f"  - Detected Date Columns: {', '.join(s['potential_date_cols']) if s['potential_date_cols'] else 'None'}\n")
            f.write(f"  - Detected ID Columns: {', '.join(s['potential_id_cols']) if s['potential_id_cols'] else 'None'}\n")
            f.write(f"  - Memory footprint: {s['memory_usage_mb']:.2f} MB\n")
            
            f.write("- **Datatype Observations**:\n")
            for col, dtype in s['dtypes_dict'].items():
                f.write(f"  - `{col}`: {dtype}\n")
            f.write("\n")

def main():
    """Main execution function for data ingestion."""
    logger.info("Starting Data Ingestion")
    
    csv_files = [f for f in RAW_DATA_DIR.iterdir() if f.is_file() and f.suffix == '.csv']
    if not csv_files:
        logger.warning(f"No CSV files found in {RAW_DATA_DIR}")
        return
        
    summaries = []
    for file_path in csv_files:
        summary = process_csv_file(file_path)
        if summary:
            summaries.append(summary)
            
    if summaries:
        summary_df = pd.DataFrame(summaries)[['filename', 'rows', 'columns', 'missing_values', 'duplicate_rows']]
        summary_csv_path = PROCESSED_DATA_DIR / "dataset_summary.csv"
        summary_df.to_csv(summary_csv_path, index=False)
        logger.info(f"Saved dataset summary to {summary_csv_path}")
        
        report_path = PROJECT_ROOT / "data_quality_summary.md"
        generate_quality_report(summaries, report_path)
        logger.info(f"Saved data quality report to {report_path}")

    logger.info("Data Ingestion Completed")

if __name__ == "__main__":
    main()
