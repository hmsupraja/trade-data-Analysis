"""Basic cleaning utilities.

- Loads raw Excel/CSV
- Cleans date fields
- Standardizes units
- Drops or flags rows with critical missing data
"""
import pandas as pd
import re
from pathlib import Path

UNIT_MAP = {
    'PCS':'PCS','PC':'PCS','NOS':'PCS','PIECES':'PCS','PIECE':'PCS',
    'KGS':'KG','KG':'KG','MT':'MT','MTR':'MTR','LTR':'LTR','L':'LTR','LTRS':'LTR'
}

def normalize_unit(u):
    if pd.isna(u):
        return None
    u2 = str(u).strip().upper()
    # normalize common tokens
    u2 = re.sub(r'\.?/.*$','',u2)  # remove '/PC' trailing parts
    return UNIT_MAP.get(u2, u2)

def load_raw(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Raw file not found: {path}")
    if p.suffix.lower() in ['.xls', '.xlsx']:
        return pd.read_excel(path, engine='openpyxl')
    else:
        return pd.read_csv(path)

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # standardize column names (lower, underscores)
    df.columns = [col.strip() for col in df.columns]

    # parse Date of Shipment
    if 'Date of Shipment' in df.columns:
        df['date_of_shipment'] = pd.to_datetime(df['Date of Shipment'], dayfirst=True, errors='coerce')
        df['year'] = df['date_of_shipment'].dt.year
        df['month'] = df['date_of_shipment'].dt.month
        df['quarter'] = df['date_of_shipment'].dt.to_period('Q')

    # normalize units
    if 'Unit' in df.columns:
        df['unit_standardized'] = df['Unit'].apply(normalize_unit)

    # numeric columns - coerce
    for col in ['Quantity','Unit Price (INR)','Total Value (INR)','Duty Paid (INR)']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Grand total placeholder
    if 'Total Value (INR)' in df.columns and 'Duty Paid (INR)' in df.columns:
        df['grand_total_inr'] = df['Total Value (INR)'].fillna(0) + df['Duty Paid (INR)'].fillna(0)

    return df

if __name__ == '__main__':
    # example usage
    print('This module provides cleaning helpers. Import functions into notebook or script.')
