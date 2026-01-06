from fastapi import APIRouter
from backend.models.schemas import GenerateRequest, JobResponse, SuccessResponse
from backend.services.job_queue import JobQueue
import uuid

router = APIRouter(prefix="/api/release-notes", tags=["release-notes"])


@router.post("/generate", response_model=SuccessResponse)
async def generate_release_notes(request: GenerateRequest):
    job_queue = JobQueue()

    job_id = await job_queue.create_job("generate_all", request.dict())

    return {
        "success": True,
        "data": {"job_id": job_id},
        "message": "Release notes generation job started"
    }
