import pandas as pd
import io
from fastapi import UploadFile, HTTPException

async def load_data(file: UploadFile) -> pd.DataFrame:
    """
    Reads an uploaded file into a Pandas DataFrame.
    Supports CSV, JSON, and Excel.
    """
    content = await file.read()
    filename = file.filename.lower()
    
    try:
        if filename.endswith('.csv'):
            # Attempt to read with utf-8, fallback to latin1 if needed
            try:
                df = pd.read_csv(io.BytesIO(content))
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(content), encoding='latin1')
        elif filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(content))
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(content))
        elif filename.endswith('.parquet'):
             df = pd.read_parquet(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV, JSON, Excel, or Parquet.")
        
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

def profile_dataset(df: pd.DataFrame) -> dict:
    """
    Extracts metadata from the dataframe.
    Returns column stats, null counts, types, etc.
    Ensures NO raw PII is stored/returned in the output, only stats.
    """
    profile = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": {}
    }
    
    columns_profile = {}
    
    # Common Patterns (simplified)
    patterns = {
        "email": r"[^@]+@[^@]+\.[^@]+",
        "phone": r"^\+?1?\d{9,15}$",
        "iso_date": r"^\d{4}-\d{2}-\d{2}$",
        "currency_code": r"^[A-Z]{3}$",
        "country_code": r"^[A-Z]{2,3}$"
    }

    for col in df.columns:
        col_series = df[col]
        col_type = str(col_series.dtype)
        
        stats = {
            "dtype": col_type,
            "null_count": int(col_series.isnull().sum()),
            "null_percentage": float(round(col_series.isnull().mean() * 100, 2)),
            "unique_count": int(col_series.nunique()),
            "is_numeric": pd.api.types.is_numeric_dtype(col_series)
        }
        
        if pd.api.types.is_numeric_dtype(col_series):
            clean_series = col_series.dropna()
            if not clean_series.empty:
                stats.update({
                    "min": float(clean_series.min()),
                    "max": float(clean_series.max()),
                    "mean": float(clean_series.mean()),
                    "negative_count": int((clean_series < 0).sum())
                })
        else:
            # String checks
            clean_series = col_series.dropna().astype(str)
            if not clean_series.empty:
                for pat_name, pat_regex in patterns.items():
                    match_count = clean_series.str.match(pat_regex).sum()
                    stats[f"{pat_name}_match_count"] = int(match_count)
                    stats[f"{pat_name}_match_percentage"] = float(round((match_count / len(df)) * 100, 2))
                
                # Attempt Date Parsing for min/max
                # Only if it looks like a date (to avoid parsing random strings)
                if stats.get("iso_date_match_percentage", 0) > 50:
                    try:
                        date_series = pd.to_datetime(clean_series, errors='coerce').dropna()
                        if not date_series.empty:
                            stats["min_date"] = date_series.min().isoformat()
                            stats["max_date"] = date_series.max().isoformat()
                    except:
                        pass

        columns_profile[col] = stats
        
    profile["columns"] = columns_profile
    return profile
