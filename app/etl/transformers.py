import pandas as pd
from typing import List, Dict

# Simple "step interpreter" for transforms (expand as needed)
def apply_transform_steps(df: pd.DataFrame, steps: List[Dict]) -> pd.DataFrame:
    for step in steps:
        op = step.get("op")
        if op == "dropna":
            df = df.dropna(subset=step.get("subset"))
        elif op == "rename":
            df = df.rename(columns=step.get("columns", {}))
        elif op == "filter":
            # step: {"op":"filter","expr":"col1 > 100"}
            df = df.query(step.get("expr"))
        elif op == "aggregate":
            groupby = step["groupby"]
            agg = step["agg"]
            df = df.groupby(groupby).agg(agg).reset_index()
        elif op == "cast":
            for col, dtype in step.get("columns", {}).items():
                df[col] = df[col].astype(dtype)
        # add more ops as needed
    return df
