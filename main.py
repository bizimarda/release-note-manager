from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from backend.core.config import settings
from backend.core.database import init_db
from backend.api import release_notes, jobs, export, github, config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

worker = None

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered release notes generation from Jira and GitHub"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(release_notes.router)
app.include_router(jobs.router)
app.include_router(export.router)
app.include_router(github.router)
app.include_router(config.router)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    await init_db()

    from backend.services.job_queue import JobQueue
    from backend.services.job_worker import JobWorker
    import asyncio

    global worker
    job_queue = JobQueue()
    worker = JobWorker(job_queue)

    asyncio.create_task(worker.start())

    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    global worker
    if 'worker' in globals():
        worker.stop()
    logger.info("Application stopped")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/templates/index.html", "r") as f:
        return f.read()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
