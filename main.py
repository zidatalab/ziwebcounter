from os import stat
import datetime

from fastapi import FastAPI, Request,HTTPException,status,Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
from pymongo import MongoClient
import uuid,os

from pymongo.compression_support import decompress

# Config
uuidsalt = uuid.UUID(os.getenv('uuidsecretanalytics'))
app = FastAPI(
    title="Zi Analytics Webcounter",
    version="1.1.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# connect to MongoDB
mongodburi = os.getenv("zidburiwrite")
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
    if (collection.estimated_document_count()>0):
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    

@app.get("/view/{siteid}/{filename}")
def report_view(siteid:str,request: Request,response: Response, pageid:Optional[str]="none",filename:Optional[str]=""):
    '''
    Collects annonymous stats. If user has visited us before, the id from a stored cookie will be used. 
    Local cookie invalidates after 365 days of not visiting a site using this service.
    '''
    try:
        query,visit=analyzerequest(request,pageid,siteid)
        if ('uid' in request.cookies.keys()):
            print('found uid:',request.cookies['uid'])
            query['user']=request.cookies['uid']
        res = collection.update_one(query,{'$push': {'visits': visit}},upsert=True)
        response.set_cookie(key='uid',value=query['user'],domain="ziapp.de",samesite="None",expires=365*24*60*60, httponly=True,secure=True)
        if (filename=='counter.png'):
            return FileResponse("counter.png")
        else:
            return res.acknowledged
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Request not formatted properly, see docs."
        )
