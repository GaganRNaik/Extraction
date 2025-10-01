from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import pipelines
from app.db.session import init_db
from app.core.logger import logger


app = FastAPI(title="ETL Orchestrator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("DB initialized")

app.include_router(pipelines.router)
