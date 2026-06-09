import pandas as pd
import numpy as np

def load_data():
    """Load the necessary datasets for recommendation."""
    try:
        # Load fund master for risk categories
        funds = pd.read_csv('data/processed/clean_fund_master.csv')
        # Load scorecards
        scores = pd.read_csv('data/processed/fund_scorecard.csv')
        # Load sharpe ratios
        sharpes = pd.read_csv('data/processed/sharpe_values.csv')
        
        # Merge datasets
        merged = pd.merge(funds[['amfi_code', 'scheme_name', 'risk_category']], scores[['amfi_code', 'score']], on='amfi_code', how='inner')
        merged = pd.merge(merged, sharpes[['amfi_code', 'sharpe_ratio']], on='amfi_code', how='inner')
        
        return merged
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def recommend_funds(risk_appetite: str) -> pd.DataFrame:
    """
    Recommend top 3 funds based on the investor's risk appetite.
    
    Args:
        risk_appetite (str): 'Low', 'Moderate', or 'High'
        
    Returns:
        pd.DataFrame: Top 3 recommended funds.
    """
    df = load_data()
    if df.empty:
        return pd.DataFrame()
    
    # Map input risk appetite to fund risk categories
    risk_map = {
        'Low': ['Low', 'Moderately Low'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High': ['High', 'Very High']
    }
    
    # Standardize input
    risk_appetite = risk_appetite.capitalize()
    if risk_appetite not in risk_map:
        raise ValueError("Invalid risk_appetite. Must be 'Low', 'Moderate', or 'High'.")
    
    allowed_categories = risk_map[risk_appetite]
    
    # Filter funds by matching risk categories
    filtered = df[df['risk_category'].isin(allowed_categories)].copy()
    
    # Rank by 1. Sharpe Ratio (descending), 2. Fund Score (descending)
    filtered.sort_values(by=['sharpe_ratio', 'score'], ascending=[False, False], inplace=True)
    
    # Select Top 3
    top_3 = filtered.head(3)
    
    # Format output
    return top_3[['scheme_name', 'risk_category', 'sharpe_ratio', 'score']].reset_index(drop=True)

if __name__ == "__main__":
    print("+-------------------+")
    print("| Recommended Funds |")
    print("+-------------------+\n")
    
    print("Example 1: Low Risk Appetite")
    low_recs = recommend_funds("Low")
    print(low_recs.to_string(index=False))
    print("\n")
    
    print("Example 2: Moderate Risk Appetite")
    mod_recs = recommend_funds("Moderate")
    print(mod_recs.to_string(index=False))
    print("\n")
    
    print("Example 3: High Risk Appetite")
    high_recs = recommend_funds("High")
    print(high_recs.to_string(index=False))
    print("\n")
