from pydantic import BaseModel

class userCreateModel(BaseModel):
    userid :str 
    user_name : str

class userPatchModel(BaseModel):
    user_name : str | None = None