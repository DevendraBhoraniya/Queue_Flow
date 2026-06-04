from typing import Optional
from pydantic import BaseModel, ConfigDict , EmailStr as email
from  datetime import datetime

# ----------------------------------
# User Schemas
# ----------------------------------
class UserBase(BaseModel):
    username: str
    email: email
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: email
    created_at: datetime
    queues: list[str] = []
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: email
    password: str

class UserLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str

class UserMini(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

# ----------------------------------
# Queue Schemas
# ----------------------------------
class QueueBase(BaseModel):
    name: str
    average_service_time: int

class QueueResponse(BaseModel):
    id: int
    name: str
    average_service_time: int
    created_by_id: int
    created_by: UserMini
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
