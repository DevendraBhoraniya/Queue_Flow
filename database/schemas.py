from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, EmailStr as email, Field, field_validator
from enum import Enum
from datetime import datetime


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
    queues: list[str] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

    @field_validator("queues", mode="before")
    @classmethod
    def coerce_queues(cls, v: Any):
        if isinstance(v, list) and v and not isinstance(v[0], str):
            return [q.name for q in v]
        return v


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
# Queue & Queue Token Schemas
# ----------------------------------
class QueueBase(BaseModel):
    name: str
    average_service_time: int = Field(gt=0)


class QueueTokenBase(BaseModel):
    queue_id: int
    joiner_name: str = Field(min_length=2, max_length=100)


class QueueResponse(BaseModel):
    id: int
    name: str
    average_service_time: int = Field(gt=0)
    created_by_id: int
    created_by: UserMini
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class QueueStatus(str, Enum):
    waiting = "waiting"
    serving = "serving"
    completed = "completed"
    cancelled = "cancelled"


class QueueTokenResponse(BaseModel):
    id: int
    token: str
    queue_id: int
    joiner_name: str
    position: int
    estimated_wait_time: int | None = None
    status: QueueStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class QueueId(BaseModel):
    id: int