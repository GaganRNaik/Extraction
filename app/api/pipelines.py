from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from app.db.session import engine
from app.db.models import Pipeline, RunHistory
from app.schemas import PipelineCreate, PipelineRead, RunRead
# from app.etl.tasks import run_pipeline
from app.core.logger import logger
from datetime import datetime
import app.etl.extractors as extractors
import app.etl.loaders as loaders


from sqlmodel import SQLModel
from app.db.session import engine

SQLModel.metadata.create_all(engine)

app = APIRouter()

@app.get("/")
def greet():
    return {"message": "Welcome to the ETL Pipeline API"}

@app.post("/pipelines", response_model=PipelineRead)
def create_pipeline(p: PipelineCreate):
    with Session(engine) as session:
        pl = Pipeline(**p.dict())
        session.add(pl)
        session.commit()
        session.refresh(pl)
        return pl

@app.get("/pipelines")
def list_pipelines():
    with Session(engine) as session:
        return session.exec(select(Pipeline)).all()
    
@app.post("/pipelines/{pipelineid}")
def trigger_pipeline(pipelineid: int):
    with Session(engine) as session:
        pipeline = session.exec(select(Pipeline).where(Pipeline.id == pipelineid)).one_or_none()

    
        if not pipeline:
            logger.error("Pipeline %s not found", pipelineid)
            return {"error": "pipeline not found"}
        # return {"message": f"Pipeline {pipelineid} triggered"}
    
        run = RunHistory(pipeline_id=pipelineid, status="running", started_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        session.add(run)
        session.commit()
        session.refresh(run)
        run_id = run.id

        logs = []
        try:
            src_type = pipeline.source_type
            src_cfg = pipeline.source_config
            if src_type == "csv":
                logger.info("Extracting CSV from %s", src_cfg["path"])
                df = extractors.extract_csv(src_cfg["path"])
                # return {"data": df.head().to_dict()}
            elif src_type == "api":
                df = extractors.extract_api(src_cfg["url"], method=src_cfg.get("method","GET"))
            elif src_type == "db":
                df = extractors.extract_db(src_cfg["conn_str"], src_cfg["query"])
            else:
                raise ValueError("unsupported source")
           
            tgt_type = pipeline.target_type
            tgt_cfg = pipeline.target_config
            if tgt_type == "Snowflake":
                res = loaders.load_snowflake(df, tgt_cfg["conn_str"], tgt_cfg["table"])
            elif tgt_type == "redshift":
                res = loaders.load_redshift(df, tgt_cfg["conn_str"], tgt_cfg["table"])
            elif tgt_type == "bigquery":
                res = loaders.load_bigquery(df, tgt_cfg["project"], tgt_cfg["dataset"], tgt_cfg["table"])

            logs.append(f"loaded {res.get('nrows')} rows to {tgt_type}")

            with Session(engine) as session:
                run = session.get(RunHistory, run_id)
                run.status = "success"
                run.finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                run.logs = "\n".join(logs)
                run.metrics = {"rows_loaded": res.get("nrows")}
                session.add(run)
                session.commit()

            return {"run_id": run_id, "status": "success", "logs": logs}
        
        except Exception as e:
             
             logger.exception("Pipeline run failed")
             with Session(engine) as session:
                run = session.get(RunHistory, run_id)
                run.status = "failed"
                run.finished_at = datetime.utcnow()
                run.logs = "\n".join(logs) + f"\nERROR: {str(e)}"
                session.add(run)
                session.commit()
                # let Celery handle retries (autoretry_for given)
             raise
            # err = f"Extraction failed: {e}"
            # logger.error(err)
            # logs.append(err)

        
        
        


# @app.post("/pipelines/{pipeline_id}/run")
# def trigger_run(pipeline_id: int, async_mode: bool = True):
#     # async_mode True => enqueue to Celery
#     if async_mode:
#         async_result = run_pipeline.delay(pipeline_id)
#         return {"task_id": async_result.id}
#     else:
#         # for debugging: run synchronously (not recommended for long jobs)
#         res = run_pipeline.run(pipeline_id)
#         return res

# @app.get("/runs/{run_id}", response_model=RunRead)
# def get_run(run_id: int):
#     with Session(engine) as session:
#         run = session.get(RunHistory, run_id)
#         if not run:
#             raise HTTPException(status_code=404, detail="run not found")
#         return run
