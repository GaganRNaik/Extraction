# Snowflake loader (uses write_pandas)
import pandas as pd

def load_snowflake(df: pd.DataFrame, conn_params: dict, table: str):
    import snowflake.connector
    from   snowflake.connector.pandas_tools import write_pandas
    conn = snowflake.connector.connect(**conn_params)
    success, nchunks, nrows, _ = write_pandas(conn, df, table,auto_create_table=True)
    return {"success": success, "nrows": nrows}

def load_redshift(df: pd.DataFrame, conn_str: str, table: str):
    # Simple but not optimized - for production use COPY via S3.
    from sqlalchemy import create_engine
    engine = create_engine(conn_str)
    df.to_sql(table, engine, index=False, if_exists="append", method="multi")
    return {"success": True, "nrows": len(df)}

def load_bigquery(df: pd.DataFrame, project: str, dataset: str, table: str):
    from google.cloud import bigquery
    client = bigquery.Client(project=project)
    table_id = f"{project}.{dataset}.{table}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    return {"success": True, "nrows": len(df)}
