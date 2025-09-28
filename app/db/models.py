from typing import Optional, Dict
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON


class Pipeline(SQLModel, table=True):
    print("Create tables if not exist")
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    source_type: str  # "csv","api","db"
    source_config: Dict = Field(sa_column=Column(JSON), default={})
    transform_config: Dict = Field(sa_column=Column(JSON), default={})
    target_type: str  # "snowflake","redshift","bigquery"
    target_config: Dict = Field(sa_column=Column(JSON), default={})
    schedule_cron: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RunHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pipeline_id: int = Field(foreign_key="pipeline.id")
    status: str  # pending, running, success, failed
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    logs: Optional[str] = None
    metrics: Optional[Dict] = Field(sa_column=Column(JSON), default={})
