from typing import Optional, Dict, List
from pydantic import BaseModel

class PipelineCreate(BaseModel):
    name: str
    source_type: str
    source_config: Dict
    transform_config: Dict = {}
    target_type: str
    target_config: Dict
    schedule_cron: Optional[str] = None

class PipelineRead(PipelineCreate):
    id: int

class RunRead(BaseModel):
    id: int
    pipeline_id: int
    status: str
    started_at: Optional[str]
    finished_at: Optional[str]
    logs: Optional[str]
    metrics: Optional[Dict]
