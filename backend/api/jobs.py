from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.models.schemas import SuccessResponse
from backend.services.job_queue import JobQueue
from typing import Dict, Set
import json
import asyncio

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

active_websockets: Dict[str, Set[WebSocket]] = {}


@router.get("/{job_id}", response_model=SuccessResponse)
async def get_job(job_id: str):
    job_queue = JobQueue()
    job = await job_queue.get_job(job_id)

    if not job:
        return {
            "success": False,
            "data": None,
            "message": "Job not found"
        }

    return {
        "success": True,
        "data": job,
        "message": "Success"
    }


@router.get("/{job_id}/status", response_model=SuccessResponse)
async def get_job_status(job_id: str):
    job_queue = JobQueue()
    job = await job_queue.get_job(job_id)

    if not job:
        return {
            "success": False,
            "data": None,
            "message": "Job not found"
        }

    return {
        "success": True,
        "data": {
            "status": job["status"],
            "progress": job["progress"],
            "current_step": job["current_step"]
        },
        "message": "Success"
    }


@router.post("/{job_id}/cancel", response_model=SuccessResponse)
async def cancel_job(job_id: str):
    from backend.services.job_worker import JobWorker

    job_queue = JobQueue()
    worker = JobWorker(job_queue)

    success = await worker.cancel_job(job_id)

    if success:
        return {
            "success": True,
            "data": None,
            "message": "Job cancelled successfully"
        }
    else:
        return {
            "success": False,
            "data": None,
            "message": "Job not found or already completed"
        }


@router.get("", response_model=SuccessResponse)
async def list_jobs(limit: int = 10):
    if limit > 100:
        limit = 100
    
    job_queue = JobQueue()
    jobs = await job_queue.list_jobs(limit=limit)

    return {
        "success": True,
        "data": jobs,
        "message": "Success"
    }


@router.websocket("/{job_id}")
async def job_updates_websocket(websocket: WebSocket, job_id: str):
    await websocket.accept()

    job_queue = JobQueue()

    try:
        while True:
            job = await job_queue.get_job(job_id)

            if job:
                await websocket.send_json({
                    "id": job["id"],
                    "status": job["status"],
                    "progress": job["progress"],
                    "current_step": job["current_step"],
                    "result": job.get("result"),
                    "error": job.get("error")
                })

                if job["status"] in ["completed", "failed", "cancelled"]:
                    await websocket.close()
                    break

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass


async def notify_job_update(job_id: str, job_data: dict):
    if job_id in active_websockets:
        disconnected = set()
        for websocket in active_websockets[job_id]:
            try:
                await websocket.send_json(job_data)
            except:
                disconnected.add(websocket)

        for ws in disconnected:
            active_websockets[job_id].discard(ws)
