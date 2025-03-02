from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
import asyncio
import uuid
import logging
import json
from typing import Dict
from backend.models import ArchitectureRequest, ArchitectureResponse, InvokeRequest, InvokeResponse, JobStatus
from backend.prompt_generator import generate_architecture_details, generate_prompt
from backend.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Use Redis for job persistence if available; otherwise, fallback to an in-memory store.
try:
    import redis
    redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
    _redis_available = True
except Exception as e:
    logger.warning("Redis not available, using in-memory job store. Error: %s", e)
    _redis_available = False
    jobs = {}

@router.post("/generate-prompt", response_model=ArchitectureResponse)
async def generate_prompt_endpoint(request: Request, payload: ArchitectureRequest):
    try:
        logger.info("Received generate-prompt request.")
        if payload.functional_requirement and payload.functional_requirement.strip():
            mode = "functional"
        elif payload.architecture:
            mode = "guided"
        else:
            raise HTTPException(status_code=400, detail="Insufficient input provided.")
        prompt_output = generate_prompt(mode, payload.dict())
        logger.info("Architecture generation complete.")
        return ArchitectureResponse(architecture=prompt_output)
    except Exception as e:
        logger.exception("Error generating architecture.")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/invoke-ai", response_model=InvokeResponse)
async def invoke_ai_endpoint(request: Request, payload: InvokeRequest, background_tasks: BackgroundTasks):
    logger.info("Received invoke-ai request.")
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    
    job_id = str(uuid.uuid4())
    job_data = {
        "status": JobStatus.PENDING,
        "result": None,
        "error": None,
        "progress": 0
    }
    
    if _redis_available:
        redis_client.setex(job_id, 86400, json.dumps(job_data))  # 24h TTL
    else:
        jobs[job_id] = job_data
    
    background_tasks.add_task(process_architecture_generation, job_id, payload.prompt)
    
    return InvokeResponse(job_id=job_id, status=JobStatus.PENDING, message="Architecture generation started")

@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    if _redis_available:
        job_str = redis_client.get(job_id)
        if not job_str:
            raise HTTPException(status_code=404, detail="Job not found")
        job = json.loads(job_str)
    else:
        job = jobs.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
    return job

async def process_architecture_generation(job_id: str, prompt: str):
    try:
        if _redis_available:
            job = json.loads(redis_client.get(job_id))
        else:
            job = jobs[job_id]
        job["status"] = JobStatus.PROCESSING
        job["progress"] = 10  # Start progress
        
        # Run generation in a background thread for real processing.
        architecture_details = await asyncio.to_thread(generate_architecture_details, prompt)
        
        job["status"] = JobStatus.COMPLETED
        job["result"] = architecture_details
        job["progress"] = 100
        
        if _redis_available:
            with redis_client.pipeline() as pipe:
                while True:
                    try:
                        pipe.watch(job_id)
                        pipe.multi()
                        pipe.setex(job_id, 86400, json.dumps(job))
                        pipe.execute()
                        break
                    except redis.WatchError:
                        continue
        else:
            jobs[job_id] = job
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        job["status"] = JobStatus.FAILED
        job["error"] = str(e)
        job["progress"] = 100
        if _redis_available:
            redis_client.setex(job_id, 86400, json.dumps(job))
        else:
            jobs[job_id] = job
