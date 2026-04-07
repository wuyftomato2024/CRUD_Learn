from pydantic import BaseModel
from typing import Any

class userCreateModel(BaseModel):
    userid :str 
    user_name : str

class userPatchModel(BaseModel):
    user_name : str | None = None

class apiResponse(BaseModel):
    status :str
    data : Any