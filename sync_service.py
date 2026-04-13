from service import userAllGetCompare
from test_data import get_external_users
from service import userPatch ,userCreate ,groupMembersCreate ,groupMembersDelete ,groupMemberList
from datetime import datetime
from db_model import GroupMember ,User

def sync_users(db):

    user_datas = userAllGetCompare(db)
    test_datas = get_external_users()
    member_datas = groupMemberList(db)

    db_user_map ={}
    db_member_map ={}

    # 计数器的初始化
    update_count = 0
    user_patch = 0
    user_create = 0
    member_create = 0
    member_delete = 0

    # 取出db里面的每个值，并且存进去dict里面
    for user_data in user_datas:

        db_userid =user_data["userid"]
        db_user_map[db_userid] = user_data

    for member_data in member_datas:

        member_userid = member_data["userid"]
        db_member_map[member_userid] = member_data

    for test_data in test_datas:

        test_userid = test_data["userid"]
        test_user_name = test_data["user_name"]
        test_time = datetime.fromisoformat(test_data["updated_at"])
        is_active = test_data["is_active"]
        group_name = "teacher"

        if test_userid in db_user_map :
            if db_user_map[test_userid]["updated_at"] < test_time:                    
                userPatch(
                    db = db,
                    userid=test_userid ,
                    user_name=test_user_name,
                    is_active=is_active
                    )
                
                # 更新map的数据，以达到最新状态
                user = db.query(User).filter(User.userid == test_userid).first()
                db_user_map[test_userid] ={
                    "userid" :user.userid ,
                    "user_name" :user.user_name,
                    "is_active" :user.is_active,
                    "updated_at" :user.updated_at
                }

                update_count += 1
                user_patch += 1
                print("user is updated")  
            else :
                pass
        else :
            userCreate(
                db ,
                userid=test_userid ,
                user_name=test_user_name,
                is_active=is_active
                )
            
            # 更新map的数据，以达到最新状态
            user = db.query(User).filter(User.userid == test_userid).first()
            db_user_map[test_userid] ={
                "userid" :user.userid ,
                "user_name" :user.user_name ,
                "is_active" :user.is_active ,
                "updated_at" :user.updated_at
            }

            update_count += 1
            user_create += 1
            print("user is created")   
        

        # 核心思路是。通过布尔值来判断，这一条数据，到底该不该存在于member里面。所以这就需要两个db表的数据以及一个外部测试数据，来作三方的对比
        if is_active:
            if test_userid in db_member_map :
                print("True is sussess")
                pass
            else:
                groupMembersCreate(
                    db =db ,
                    userid=test_userid ,
                    user_name=test_user_name,
                    group_name =group_name
                )

                # 更新map的数据，以达到最新状态
                user = db.query(GroupMember).filter(GroupMember.userid ==test_userid).first()
                
                db_member_map[test_userid] = {
                    "userid": user.userid,
                    "user_name": user.user_name,
                    "group_name": user.group_name ,
                    "updated_at" :user.updated_at
                }

                update_count += 1
                member_create += 1 
                print("member was created")                   
        else :
            if test_userid in db_member_map :
                groupMembersDelete(
                    db =db ,
                    userid=test_userid ,
                )
                
                # 更新map的数据，以达到最新状态
                del db_member_map[test_userid]

                update_count += 1
                member_delete += 1 
                print("member was deleted")
            else:
                pass  
                print("False is sussess")

    result = {
         "sync":"ok",
         "hit":update_count
         }
    
    if user_patch >0 :
        result["user_patch"] = user_patch
    if user_create >0 :
        result["user_create"] = user_create
    if member_create >0 :
        result["member_create"] = member_create
    if member_delete >0 :
        result["member_delete"] = member_delete

    return result
         

