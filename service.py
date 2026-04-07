from fastapi import HTTPException 
from model import apiResponse
from db_model import User

db = {}
next_id = 1

# def userCreate(userid,user_name):
#     if userid in db:
#          raise HTTPException(status_code=400,detail="user was been added")
#     global next_id
#     users ={"id":next_id,"userid":userid,"user_name":user_name}
#     db[userid] = users
#     next_id += 1
    
#     return apiResponse(
#         status = "ok" ,
#         data = users
#     ) 

def userCreate(db ,userid ,user_name):
    old_user = db.query(User).filter(User.userid == userid).first()
    if old_user :
        raise HTTPException(status_code=400,detail="user was been added")
    new_user =User(
        userid = userid,
        user_name = user_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return apiResponse(
        status = "ok" ,
        data = {
            "id": new_user.id,
            "userid": new_user.userid,
            "user_name": new_user.user_name
        }
    ) 

def userDelete(userid):
    if userid not in db:
        raise HTTPException(status_code=404,detail="user is not found")
    del db[userid]

    return apiResponse(
        status = "ok" ,
        data ={
            "deleted":True
            }
    ) 

def userGet(userid):
    if userid not in db :
        raise HTTPException(status_code=404,detail="user is not found")
    
    return apiResponse(
        status = "ok" ,
        data = db[userid]
    ) 

def userAllGet(user_name):
    db_data = []
    if not db :
        raise HTTPException(status_code=404,detail="user is not found")
    if user_name :
        for db_userid,db_user in db.items():
            if db_user["user_name"] == user_name:
                db_data.append(db_user)
    else:
        db_data = list(db.values())

    return apiResponse(
        status = "ok" ,
        data = db_data
    )   

def userPatch(userid,body):
    if userid not in db :
        raise HTTPException(status_code=404,detail="user is not found")
    
    if not body.user_name:
        raise HTTPException(status_code=400 ,detail="please input")
    elif body.user_name == db[userid]["user_name"]:
        raise HTTPException(status_code=400 ,detail="please input")     
    elif body.user_name is not None :
        db[userid]["user_name"]=body.user_name
     
    
    return apiResponse(
        status = "ok" ,
        data = {
        "patch" : True ,
        "data":db[userid]
        }
    )    