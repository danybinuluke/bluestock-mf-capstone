import os
import sys
import logging
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_script(script_path):
    """Executes a python script and handles errors."""
    logging.info(f"Starting execution of: {script_path}")
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info(f"Successfully completed: {script_path}")
        if result.stdout:
            logging.debug(f"Output of {script_path}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while executing {script_path}")
        logging.error(f"Error output: {e.stderr}")
        raise Exception(f"Pipeline failed at step: {script_path}")
    except FileNotFoundError:
        logging.error(f"Script not found: {script_path}. Ensure the file exists.")
        raise

def main():
    """Main execution function for the pipeline."""
    logging.info("="*50)
    logging.info("STARTING BLUESTOCK MF ANALYTICS PIPELINE")
    logging.info("="*50)
    
    # Define absolute paths using Pathlib to avoid hardcoded paths
    base_dir = Path(__file__).resolve().parent
    scripts_dir = base_dir / 'scripts'
    
    # Execution Order
    steps = [
        # 1. ETL Pipeline (Data Ingestion & Cleaning)
        # 2. Database Loading (Often combined in modern ETL scripts, assuming single ETL script here)
        scripts_dir / 'etl_pipeline.py',
        
        # 3. Performance Analytics
        scripts_dir / 'performance_analytics.py',
        
        # 4. Advanced Analytics
        scripts_dir / 'advanced_analytics.py',
        
        # 5. Recommendation Engine
        scripts_dir / 'recommender.py'
    ]
    
    # Verify scripts exist before running
    for step in steps:
        if not step.exists():
            logging.warning(f"Script missing: {step}. Skipping or Pipeline may fail if required.")
            # We continue assuming the user might not have created all placeholders yet, 
            # but ideally, we should fail fast. For capstone, we will attempt to run existing ones.
    
    success_count = 0
    try:
        for script in steps:
            if script.exists():
                run_script(str(script))
                success_count += 1
            else:
                logging.error(f"File not found, skipping step: {script}")
                
        logging.info("="*50)
        logging.info(f"PIPELINE EXECUTION SUMMARY: {success_count}/{len(steps)} steps completed successfully.")
        logging.info("="*50)
        logging.info("Next Steps:")
        logging.info("- Check pipeline_execution.log for details.")
        logging.info("- Refresh Power BI Dashboard to load new data.")
        
    except Exception as e:
        logging.critical("Pipeline execution aborted due to critical error.")
        logging.critical(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
