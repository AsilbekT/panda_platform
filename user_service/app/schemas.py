# schemas.py

from pydantic import BaseModel
from typing import Optional, Any


class UserProfileCreate(BaseModel):
    id: Optional(int) = None
    phone_number: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    preferences: Optional[str] = None
    history: Optional[str] = None

    class Config:
        from_attributes = True


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
