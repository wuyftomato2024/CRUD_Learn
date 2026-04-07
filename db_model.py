from database import Base
from sqlalchemy import Column ,Integer ,String

# 定义表的格式
class User(Base):
    __tablename__ = "users"

    # 数字类型(int)配合主key，会自动分配数字
    id = Column(Integer ,primary_key=True ,index=True)
    userid = Column(String(50) ,unique=True,nullable=False)
    user_name = Column(String(100) ,nullable=False)

    # __tablename__ = 这张表叫什么
    # unique=True = 不能重复
    # index=True = 更方便查找