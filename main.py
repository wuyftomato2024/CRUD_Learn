from fastapi import FastAPI ,HTTPException ,Depends
from fastapi.responses import JSONResponse
from service import userCreate ,userDelete ,userGet,userAllGet,userPatch
from model import userCreateModel ,userPatchModel
import uvicorn
from database import engine ,Base ,SessionLocal
# from db_model import User

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
        user_name = body.user_name
    )
    return response

@app.delete("/user/{userid}")
def deleteUser(userid :str ,db =Depends(get_db)):
    response = userDelete(
        userid=userid , 
        db=db)
    return response

@app.patch("/user/{userid}")
def patchUser(userid:str,body :userPatchModel,db = Depends(get_db)):
    response = userPatch(
        userid = userid ,
        user_name = body.user_name,
        db = db
        )
    return response