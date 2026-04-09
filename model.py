from pydantic import BaseModel
from typing import Any

class userCreateModel(BaseModel):
    userid :str 
    user_name : str
    is_active : bool

class userPatchModel(BaseModel):
    user_name : str | None = None
    is_active : bool

class apiResponse(BaseModel):
    status :str
    data : Any