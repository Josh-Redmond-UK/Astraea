from typing import Union
from pydantic import BaseModel
import uuid
from src.download_utils import *
from src.date_time_utils import *
from src.earth_engine_utils import *
from src.api_utils import *
import asyncio
ee.Initialize()

from fastapi import FastAPI

ee.Initialize()

app = FastAPI()

active_map = {}


class MapJob(BaseModel):
    job_id: str
    job_status: str
    tracking: str
    params: dict

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/mapping/createjob")
async def create_job(params):
    params = json.loads(params)
    job = MapJob(job_id=id, job_status="pending", tracking=f"api/mapping/{id}", params=params)
    return job

@app.get("/api/mapping/", status_code=202)
async def generate_maps(job:MapJob):
    
    print("PRINTING PARAMS", params)
    params = json.loads(params)
    result = await handle_request(params)
    #asyncio.run(result)
    return job

@app.get("/api/mapping/start/", status_code=202)
async def start_job(job:MapJob):
    job.job_status = "running"
    res = generate_maps(job)
    return res




@app.get("/api/mapping/get/{job_id}")
async def get_map(job_id):
    return active_map[job_id]