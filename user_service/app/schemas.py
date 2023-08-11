# schemas.py

from pydantic import BaseModel
from typing import Optional


class UserProfileCreate(BaseModel):
    phone_number: str
    name: str
    username: str
    avatar: Optional[str] = None
    preferences: Optional[str] = None
    history: Optional[str] = None


class UserProfileResponse(UserProfileCreate):
    id: int
