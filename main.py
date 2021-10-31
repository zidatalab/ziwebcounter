from os import stat
import datetime

from fastapi import FastAPI, Request,HTTPException,status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
from pymongo import MongoClient
import uuid
from zicredentials import get_zi_secret

# Config
uuidsalt = uuid.UUID(get_zi_secret('uuidsecretanalytics'))
app = FastAPI(
    title="Zi Analytics Webcounter",
    version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# connect to MongoDB
mongodburi = get_zi_secret("zidburiwrite")
db = MongoClient(mongodburi).get_database('webtools')
collection = db.webcounter

# Functions
def makeuuid(ip,agent):
    '''
    This Functions annonymizes the host ip and agent by creating an UUID in a special namespace.
    The UUID is based on the MD5 hash of a namespace identifier (which is a secret UUID) and a 
    name which is a string (str(host)+str(user-agent)). This ensures pretty good privacy for hosts. 
    A random namespace is not used, to ensure user stability over different analytics endpoints 
    at the same time.
    '''
    global mynamesspace
    return str(uuid.uuid3(uuidsalt,ip+agent))

def makeanalyticsentry(ip,agent,pageid,siteid,referer):
    entry = {'user':makeuuid(ip,agent),'siteid':siteid,'date':str(datetime.date.today())}
    visits={'pageid':pageid,'timestamp':datetime.datetime.utcnow(),'referer':referer}
    return entry,visits

def analyzerequest(request:Request,pageid:str,siteid:str):
    return makeanalyticsentry(
        request.headers['host'],
        request.headers['user-agent'],
        pageid,siteid,
        request.headers['referer'])

# Endpoints
@app.get("/")
def endpointstatus():
    '''
    Returns Enpoint Status
    '''
    if (collection.count()>0):
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    

@app.get("/view/{siteid}/{filename}")
def report_view(siteid:str,request: Request,pageid:Optional[str]="none",filename:Optional[str]=""):
    '''
    Collects annonymous stats
    '''
    try:
        query,visit=analyzerequest(request,pageid,siteid)
        res = collection.update_one(query,{'$push': {'visits': visit}},upsert=True)
        if (filename=='counter.png'):
            return FileResponse("counter.png")
        else:
            return res.acknowledged
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
             detail="Request not formatted properly, see docs."
        )
