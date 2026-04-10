from fastapi import HTTPException 
from model import apiResponse
from db_model import User ,GroupMember

# ***********
# 创建user
# ***********
def userCreate(db ,userid ,user_name ,is_active):
    userid = userid.strip()
    user_name = user_name.strip()

    old_user = db.query(User).filter(User.userid == userid).first()
    if old_user :
        raise HTTPException(status_code=400,detail="user was been added")
    new_user =User(
        userid = userid,
        user_name = user_name ,
        is_active = is_active
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
                "user_name":user_data.user_name,
                "updated_at":user_data.updated_at,
                "is_active":user_data.is_active
            })
    else :
        user = db.query(User).all()
        for user_data in user:
            result.append({
                "id":user_data.id,
                "userid":user_data.userid,
                "user_name":user_data.user_name ,
                "updated_at":user_data.updated_at,
                "is_active":user_data.is_active
            })

    return apiResponse(
        status = "ok" ,
        data = {
            "fetched":True ,
            "data":result
        } 
    )  

# ***********
# 更新/修改user数据(status更新)
# ***********    
def userPatch(db ,userid ,is_active,user_name):
    userid = userid.strip()
    
    # 查找老userid
    old_user = db.query(User).filter(User.userid == userid ,User.user_name == user_name).first()
    if not old_user:
        raise HTTPException(status_code=404,detail="user is not found")
    if is_active is None:
        raise HTTPException(status_code=400 ,detail="user_name is required")
    else:
        old_user.is_active = is_active
        db.commit()
        db.refresh(old_user)

        return apiResponse(
        status = "ok" ,
        data = {
            "updated":True ,
            "data":user_data(old_user)
            }
    )

# ***********
# 获取user,数据比较用
# ***********
def userAllGetCompare(db):
    result = []
    user = db.query(User).all()
    for user_data in user:
        result.append({
            "id":user_data.id,
            "userid":user_data.userid,
            "user_name":user_data.user_name ,
            "is_active":user_data.is_active,
            "updated_at":user_data.updated_at
        })

    return result

# ***********
# 获取群组用
# ***********
def groupMemberList(db):
    result = []
    members = db.query(GroupMember).all()
    for member in members :
        result.append({
            "id":member.id,
            "userid":member.userid,
            "user_name":member.user_name ,
            "group_name":member.group_name ,
            "updated_at":member.updated_at
        })
    
    return result

# ***********
# 在群组中新增用户
# ***********
def groupMembersCreate(db,userid,user_name,group_name):
    old_user = db.query(GroupMember).filter(GroupMember.userid == userid)
    if not old_user :
        raise HTTPException(status_code=404 ,detail="") 
    new_user =GroupMember(
        userid = userid,
        user_name = user_name,
        group_name = group_name 
    ) 

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return apiResponse(
        status = "ok" ,
        data = {
            "created":True ,
            "data":{
                "id": new_user.id,
                "userid": new_user.userid,
                "user_name": new_user.user_name,
                "group_name":new_user.group_name,
                "updated_at":new_user.updated_at   
            }
        }
    )

# ***********
# 从群组中移除用户
# ***********
def groupMembersDelete(db ,userid):
    old_user = db.query(GroupMember).filter(GroupMember.userid == userid).first()
    if not old_user :
        raise HTTPException(status_code=404 ,detail="") 
    
    db.delete(old_user)
    db.commit()

    return apiResponse(
        status = "ok" ,
        data = {
            "deleted":True
        }
    ) 


# 返回对象dict化模板
# 传参不一定需要和声明函数时一模一样的参数名字，调用函数写别的名字，函数本体会自动给转换成需要的函数的原始形态
def user_data(user):
     return {
        "id": user.id,
        "userid": user.userid,
        "user_name": user.user_name,
        "is_active":user.is_active,
        "updated_at":user.updated_at    
    }  