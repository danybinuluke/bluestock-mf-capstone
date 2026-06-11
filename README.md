# Bluestock Mutual Fund Analytics Platform

## Project Overview
The Bluestock Mutual Fund Analytics Platform is a comprehensive data engineering and business intelligence capstone project. It is designed to ingest, process, analyze, and visualize large volumes of mutual fund data. The platform provides stakeholders with advanced risk-adjusted performance metrics, investor behavioral insights, and market trend analysis.

## Business Objective
To build a centralized, automated analytics platform that empowers investors, fund managers, and analysts to make data-driven decisions. The project solves the problem of fragmented data by providing a unified SQLite data warehouse, advanced Python-based analytics (VaR, Alpha, Beta, Cohort Analysis), and an interactive Power BI dashboard.

## Project Architecture
1. **Extraction:** Raw data is extracted from CSV/Excel files using Pandas.
2. **Transformation:** Data cleaning, missing value imputation (e.g., forward-filling weekend NAVs), and anomaly detection.
3. **Loading:** Transformed data is loaded into an optimized SQLite Star Schema database via SQLAlchemy.
4. **Analytics:** Advanced metrics (Sharpe, VaR, HHI) are computed using NumPy/Pandas and exported as CSV reports.
5. **Visualization:** A Power BI dashboard connects to the database and CSV outputs to render interactive visualizations.

## Folder Structure
```text
bluestock_mf_capstone/
├── data/                 # Raw and cleaned datasets
├── docs/                 # Documentation and checklists
├── notebooks/            # Jupyter notebooks (EDA, Performance, Advanced Analytics)
├── reports/              # Final reports and presentation materials
├── scripts/              # Python ETL and analytical scripts
├── sql/                  # SQL schema and queries
├── dashboard/            # Power BI dashboard files
├── run_pipeline.py       # Master execution script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Dependencies
- Python 3.9+
- pandas
- numpy
- sqlalchemy
- plotly
- seaborn
- matplotlib
- jupyter

## Installation & Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/danybinuluke/bluestock-mf-capstone.git
   cd bluestock_mf_capstone
   ```

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

### Master Execution
To run the entire pipeline (ETL, Database Creation, Analytics Generation) in one go, use the master script:
```bash
python run_pipeline.py
```

### Running Steps Individually
If you prefer to run the modules separately:

1. **Running ETL:**
   ```bash
   python scripts/etl_pipeline.py
   ```
2. **Running Analytics:**
   ```bash
   python scripts/performance_analytics.py
   python scripts/advanced_analytics.py
   python scripts/recommender.py
   ```

### Running the Dashboard
1. Open Power BI Desktop.
2. Open the file located at `dashboard/Bluestock_MF_Dashboard.pbix`.
3. If necessary, update the Data Source settings to point to the local `data/bluestock_mf.db` database and the output CSV files in the `data/` folder.
4. Click "Refresh" to load the latest data.

## Output Files
The pipeline generates several key output files used for reporting and dashboarding:
- `data/bluestock_mf.db` (SQLite Database)
- `data/fund_scorecard.csv`
- `data/alpha_beta.csv`
- `data/var_cvar_report.csv`
- `data/cohort_analysis.csv`
- `data/sector_hhi.csv`

## Technologies Used
- **Language:** Python
- **Libraries:** Pandas, NumPy, SQLAlchemy, Matplotlib, Seaborn
- **Database:** SQLite
- **BI Tool:** Power BI
- **Version Control:** Git & GitHub

## Note on `.db` Files
The SQLite database `bluestock_mf.db` is generated dynamically by the ETL pipeline. It is intentionally excluded from version control via `.gitignore` to keep the repository lightweight. Ensure you run the pipeline locally to generate the database.
