from service import userAllGetCompare
from test_data import get_external_users
from service import userPatch ,userCreate
from datetime import datetime

def sync_users(db):
    user_datas = userAllGetCompare(db)
    test_datas = get_external_users()

    db_user_map ={}
    update_count = 0

    # 取出db里面的每个值，并且存进去dict里面
    for user_data in user_datas:
        db_userid =user_data["userid"]
        db_user_map[db_userid] = user_data
        
    for test_data in test_datas:
        test_userid = test_data["userid"]
        test_user_name = test_data["user_name"]
        test_time = datetime.fromisoformat(test_data["updated_at"])
        is_active = test_data["is_active"]

        if test_userid in db_user_map :
                if db_user_map[test_userid]["updated_at"] < test_time:                    
                    response = userPatch(db ,userid=test_userid ,user_name=test_user_name,is_active=is_active)
                    update_count += 1
                else :
                    response = None
        else :
            response = userCreate(db ,userid=test_userid ,user_name=test_user_name,is_active=is_active)
            update_count += 1

    return {
         "sync":"ok",
         "hit":update_count,
         "data":response
         }

