from fastapi import FastAPI ,HTTPException ,Depends
from fastapi.responses import JSONResponse
from service import userCreate ,userDelete ,userGet,userAllGet,userPatch ,groupMembersCreate ,groupMembersDelete ,groupMemberList
from model import userCreateModel ,userPatchModel ,userActivePatchModel ,groupMemberCreateModel
import uvicorn
from database import engine ,Base ,SessionLocal
from sync_service import sync_users

app = FastAPI()

# 创建所有继承自Base的所有表，路径是bind=engine这个接口
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

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
def getUser(userid :str ,db =Depends(get_db)):
    response = userGet(
        userid=userid ,
        db = db)
    return response

@app.get("/get")
# 意为user_name的类型是str或者空值 ，默认是 没东西
def getAllUser(user_name :str|None  =None ,db = Depends(get_db)):
    response = userAllGet(
        user_name = user_name,
        db = db
        )
    return response

@app.post("/user")
# db 这个参数由 FastAPI 通过 Depends(get_db) 自动提供
def postUser(body : userCreateModel ,db =Depends(get_db)):
    response = userCreate(
        db = db ,
        userid = body.userid ,
        user_name = body.user_name,
        is_active = body.is_active
    )
    return response

@app.delete("/user/{userid}")
def deleteUser(userid :str ,db =Depends(get_db)):
    response = userDelete(
        userid=userid , 
        db=db
        )
    return response

@app.patch("/user/{userid}")
def patchUser(userid:str,user_name:str,body :userActivePatchModel,db = Depends(get_db)):
    response = userPatch(
        userid = userid ,
        is_active = body.is_active,
        user_name = user_name,
        db = db
        )
    return response

@app.get("/data")
def test_data_app(db=Depends(get_db)):
    response = sync_users(db = db)
    return response

@app.get("/group")
def getGroupMemberUser(db = Depends(get_db)):
    response = groupMemberList(db=db)
    return response

@app.post("/group")
# db 这个参数由 FastAPI 通过 Depends(get_db) 自动提供
def postGroupMemberUser(body : groupMemberCreateModel ,db =Depends(get_db)):
    response = groupMembersCreate(
        db = db ,
        userid = body.userid ,
        user_name = body.user_name,
        group_name = body.group_name
    )
    return response

@app.delete("/group/{userid}")
def deleteGroupMemberUser(userid :str ,db = Depends(get_db)):
    response = groupMembersDelete(
        db = db ,
        userid = userid
    )
    return response