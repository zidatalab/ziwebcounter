from io import BytesIO
import random
from starlette.responses import StreamingResponse
from string import ascii_uppercase, digits
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Dict, Optional, List
from pymongo import MongoClient
import hashlib, uuid

from zicredentials import get_zi_secret

uuidsalt = uuid.uuid4().hex.encode('utf-8')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]

)

# connect to MongoDB via pymongo
dbclient = MongoClient(get_zi_secret("zidburiwrite")).get_database("webtools")
collection = dbclient.webcounter
counter = 1

@app.get("/view/{siteid}/{userid}/counter.png")
def report_view(siteid:str,userid:str,request: Request,pageid:str):
    print("View for "+siteid+" "+userid+" "+pageid+ "host:"+request.headers['host'])
    print(dict(request.headers).keys())
    print("host:"+ hashlib.sha224(str(request.headers['host']).encode('utf-8')+uuidsalt).hexdigest())
    counter=+1
    print(counter)
    return FileResponse("counter.png")
