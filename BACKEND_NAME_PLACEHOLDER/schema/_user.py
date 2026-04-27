from pydantic import BaseModel

class UserBase(BaseModel):
    user_name: str

class UserCreate(UserBase):
    password: str

class UserFull(UserBase):
    entity_id: int
    password_hash: str
