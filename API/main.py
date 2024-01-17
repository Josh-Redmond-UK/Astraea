from typing import Union
from src.download_utils import *
from src.date_time_utils import *
from src.earth_engine_utils import *
from src.api_utils import *
ee.Initialize()

from fastapi import FastAPI

ee.Initialize()

app = FastAPI()

active_map = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/mapping")
def generate_maps(params):
    params = json.loads(params)
    result = handle_request(params)
    return result

