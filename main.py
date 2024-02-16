from os import stat
import datetime

from fastapi import FastAPI, Request,HTTPException,status,Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from typing import Optional
from pymongo import MongoClient
import uuid,os

from pymongo.compression_support import decompress

# Config
uuidsalt = uuid.UUID(os.getenv('uuidsecretanalytics'))
ziip = os.getenv("ziip")
app = FastAPI(
    title="Zi Analytics Webcounter",
    version="1.1.42")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Provide additional html info
app.mount("/static", StaticFiles(directory="docs"), name="static")

# connect to MongoDB
mongodburi = os.getenv("mongodbatlas")
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

def makeanalyticsentry(ip,agent,pageid,siteid,referer,language):
    entry = {'uid':makeuuid(ip,agent),'siteid':siteid,'date':str(datetime.date.today()), 'usergroup': get_usergroup(ip)}
    visits={'pageid':pageid,'time':datetime.datetime.now(datetime.UTC),'ref':referer,'lang':language}
    return entry,visits

def get_ip(headers):
    ip = "unknown"
    if headers.get("x-forwarded-for"):
        ip = headers["x-forwarded-for"]
    elif headers.get("x-real-ip"):
        ip = headers["x-real-ip"]
    return ip

def get_usergroup(ip):
    usergroup = "external"
    if ip == ziip:
        usergroup = "Zi"
    elif ip == "unknown":
        usergroup = "unknown"
    return usergroup

def analyzerequest(request:Request,pageid:str,siteid:str):
    return makeanalyticsentry(
        get_ip(request.headers),
        request.headers['user-agent'],
        pageid,siteid,
        request.headers.get('referer', 'test_referer'),
        request.headers.get('Accept-Language', 'German'))

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
def report_view(
    siteid:str,request: Request,response: Response, 
    pageid:Optional[str]="none",filename:Optional[str]="",cookiedissent:bool=False):
    '''
    Collects annonymous stats. If user has visited us before, the id from a stored cookie will be used. 
    Local cookie invalidates after 365 days of not visiting a site using this service.
    '''
    try:
        query,visit=analyzerequest(request,pageid,siteid)
        if ('uid' in request.cookies.keys()):
            print('found uid:',request.cookies['uid'])
            query['uid']=request.cookies['uid']
        res = collection.update_one(query,{'$push': {'visits': visit}},upsert=True)
        if not(cookiedissent):
            response.set_cookie(key='uid',value=query['uid'],samesite="None",
            expires=365*24*60*60, httponly=True,secure=False)
        if (cookiedissent and ('uid' in request.cookies.keys())):
            response.delete_cookie('uid')
        if (filename=='counter.png'):
            return FileResponse("counter.png")
        else:
            return res.acknowledged
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Request not formatted properly, see docs."
        )
