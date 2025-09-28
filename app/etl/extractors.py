import pandas as pd
import requests
from sqlalchemy import create_engine
from app.core.config import settings

def extract_csv(path_or_fileobj, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path_or_fileobj, **kwargs)

def extract_api(url: str, method="GET", params=None, headers=None) -> pd.DataFrame:
    resp = requests.request(method, url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Assumption: JSON is a list of dicts or single dict with records field
    if isinstance(data, dict) and "records" in data:
        data = data["records"]
    return pd.DataFrame(data)

def extract_db(conn_str: str, query: str) -> pd.DataFrame:
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
