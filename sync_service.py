from service import userAllGetCompare
from test_data import get_external_users
from service import userPatch ,userCreate ,groupMembersCreate ,groupMembersDelete ,groupMemberList
from datetime import datetime

def sync_users(db):

    user_datas = userAllGetCompare(db)
    test_datas = get_external_users()
    member_datas = groupMemberList(db)

    db_user_map ={}
    db_member_map ={}
    update_count = 0

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
                response = userPatch(
                        db = db,
                        userid=test_userid ,
                        user_name=test_user_name,
                        is_active=is_active
                        )
                print("user patch is sussess")
                update_count += 1
            else :
                pass
        else :
            response = userCreate(db ,userid=test_userid ,user_name=test_user_name,is_active=is_active)
            update_count += 1
            print("user_create is sussess")   
        

        # 核心思路是。通过布尔值来判断，这一条数据，到底该不该存在于member里面。所以这就需要两个db表的数据以及一个外部测试数据，来作三方的对比
        if is_active:
            if test_userid in db_member_map :
                print("True is sussess")
                pass
            else:
                response = groupMembersCreate(
                        db =db ,
                        userid=test_userid ,
                        user_name=test_user_name,
                        group_name =group_name
                    )
                print("member_create is sussess")    
        else :
            if test_userid in db_member_map :
                response = groupMembersDelete(
                        db =db ,
                        userid=test_userid ,
                    )
                print("member delete is sussess")
            else:
                pass  
                print("False is sussess")

    return {
         "sync":"ok",
         "hit":update_count,
        #  "data":response
         }

