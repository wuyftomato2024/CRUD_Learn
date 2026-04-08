from fastapi import HTTPException 
from model import apiResponse
from db_model import User

# ***********
# 创建user
# ***********
def userCreate(db ,userid ,user_name):
    userid = userid.strip()
    user_name = user_name.strip()

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
            "created":True ,
            "data":user_data(new_user)
        }
    ) 

# ***********
# 删除user
# ***********
def userDelete(db ,userid):
    userid = userid.strip()

    old_user = db.query(User).filter(User.userid == userid).first()
    if not old_user:
        raise HTTPException(status_code=404,detail="user is not found")

    db.delete(old_user)
    db.commit()

    return apiResponse(
        status = "ok" ,
        data = {
            "deleted":True
        }
    ) 

# ***********
# 获取user（userid）
# ***********
def userGet(db,userid):
    userid = userid.strip()

    old_user = db.query(User).filter(User.userid == userid).first()
    if not old_user:
        raise HTTPException(status_code=404,detail="user is not found")
    
    # old_user 不是普通 dict。它是 <class 'db_model.User'>，把它手动改成 dict 再返回
    return apiResponse(
        status = "ok" ,
        data = {
            "fetched":True ,
            "data":user_data(old_user)
        }         
    )    

# ***********
# 获取user（username），没有的时候全数据获取
# ***********
def userAllGet(db ,user_name):
    result = []

    if user_name is not None:
        # strip() 会去掉前后面的 空格 换行 tab
        user_name = user_name.strip()

    if user_name :
        user = db.query(User).filter(User.user_name == user_name).all()
        if not user:
            raise HTTPException(status_code=404,detail="user is not found")
        for user_data in user :
            result.append({
                "id":user_data.id,
                "userid":user_data.userid,
                "user_name":user_data.user_name
            })
    else :
        user = db.query(User).all()
        for user_data in user:
            result.append({
                "id":user_data.id,
                "userid":user_data.userid,
                "user_name":user_data.user_name
            })

    return apiResponse(
        status = "ok" ,
        data = {
            "fetched":True ,
            "data":result
        } 
    )  

# ***********
# 更新/修改user数据
# ***********    
def userPatch(db ,userid ,user_name):
    userid = userid.strip()
    user_name = user_name.strip()

    old_user = db.query(User).filter(User.userid == userid).first()
    if not old_user:
        raise HTTPException(status_code=404,detail="user is not found")
    if not user_name:
        raise HTTPException(status_code=400 ,detail="user_name is required")
    old_user_name = db.query(User).filter(User.user_name == user_name , User.userid != userid).first()
    if old_user_name:
        raise HTTPException(status_code=400 ,detail="user_name already exists")
    else:
        old_user.user_name = user_name
        db.commit()
        db.refresh(old_user)

        return apiResponse(
        status = "ok" ,
        data = {
            "updated":True ,
            "data":user_data(old_user)
            }
    ) 

# 返回对象dict化模板
# 传参不一定需要和声明函数时一模一样的参数名字，调用函数写别的名字，函数本体会自动给转换成需要的函数的原始形态
def user_data(user):
     return {
        "id": user.id,
        "userid": user.userid,
        "user_name": user.user_name
    }  