from fastapi import HTTPException 

db = {}
next_id = 1

def userCreate(userid,user_name):
    global next_id
    users ={"id":next_id,"userid":userid,"user_name":user_name}
    db[userid] = users
    next_id += 1
    
    return users

def userDelete(userid):
    if userid not in db:
        raise HTTPException(status_code=404,detail="user is not found")
    del db[userid]
    return {"deleted":True}

def userGet(userid):
    if userid not in db :
        raise HTTPException(status_code=404,detail="user is not found")
    return db[userid]

def userAllGet():
    if not db :
        raise HTTPException(status_code=404,detail="user is not found")
    return list(db.values())

def userPatch(userid,body):
    if userid not in db :
        raise HTTPException(status_code=404,detail="user is not found")
    if body.user_name is not None:
        db[userid]["user_name"]=body.user_name
    return  {
        "patch" : True ,
        "data":db[userid]
        }