from fastapi import FastAPI
from app.api import pipelines
from app.db.session import init_db
from app.core.logger import logger

app = FastAPI(title="ETL Orchestrator")

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("DB initialized")

app.include_router(pipelines.router)
