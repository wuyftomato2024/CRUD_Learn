from fastapi import FastAPI ,HTTPException 
from fastapi.responses import JSONResponse
from service import userCreate ,userDelete ,userGet,userAllGet,userPatch
from model import userCreateModel ,userPatchModel
import uvicorn

app = FastAPI()

@app.exception_handler(HTTPException)
def setError(request ,exc:HTTPException):
    return JSONResponse(
        status_code = exc.status_code ,
        content= {
            "status":"fail",
            "data" : None,
            "detail":exc.detail
        }
    )

@app.exception_handler(Exception)
def error(request ,exc:Exception):
    return JSONResponse(
        status_code = 500 ,
        content={
            "status":"fail",
            "data" : None,
            "detail":str(exc)
        }
    )

@app.get("/")
def index():
    return "fastapi was running"

@app.get("/user/{userid}")
def getUser(userid :str):
    response = userGet(userid=userid)
    return response

@app.get("/get")
def getAllUser():
    response = userAllGet()
    return response

@app.post("/user")
def postUser(body : userCreateModel):
    response = userCreate(
        userid = body.userid ,
        user_name = body.user_name
    )
    return response

@app.delete("/user/{userid}")
def deleteUser(userid :str):
    response = userDelete(userid=userid)
    return response

@app.patch("/user/{userid}")
def patchUser(userid:str,body :userPatchModel):
    response = userPatch(
        userid=userid ,
        body =body
        )
    return response


