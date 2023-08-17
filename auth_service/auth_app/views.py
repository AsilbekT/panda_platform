from fastapi import HTTPException, Header, Depends
from .models import User
from .utils import (
    hash_password,
    create_jwt_token,
    verify_jwt_token,
    verify_password,
    token_blacklist  # Import the token_blacklist
)
from .database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
import jwt
import httpx
from .schemas import StandardResponse


class UserCreate(BaseModel):
    username: str
    phone_number: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


async def register(user: UserCreate, db: Session = Depends(get_db)) -> StandardResponse:
    # Check if the user with the given username or phone number already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (
            User.phone_number == user.phone_number)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        phone_number=user.phone_number,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    url = "http://127.0.0.1:7008/users"

    # Username to send (assuming user.username is defined elsewhere in your code)
    data = {
        "username": user.username,
        "phone_number": user.phone_number,
    }

    response = httpx.post(url, json=data)

    if response.status_code != 200:
        return StandardResponse(status="error", message="Failed to create user profile")
    return StandardResponse(
        status="success", message="User created successfully", data={"username": user.username}
    )


async def login(user: UserLogin, db: Session = Depends(get_db)) -> StandardResponse:
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_data = {"sub": db_user.id, "username": db_user.username}
    token = create_jwt_token(token_data)
    return StandardResponse(status="success", message="Login successful", data={"access_token": token, "token_type": "bearer"})


def get_token(authorization: str = Header(None)) -> str:
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        return token
    raise HTTPException(status_code=401, detail="Invalid token")


async def logout(token: str = Depends(get_token)) -> StandardResponse:
    token_blacklist.add(token)  # Add the token to the blacklist
    return StandardResponse(status="success", message="Successfully logged out")


async def verify_token(token: str = Depends(get_token)) -> StandardResponse:
    if token in token_blacklist:  # Check if the token is in the blacklist
        raise HTTPException(
            status_code=401, detail="Token has been invalidated")

    try:
        payload = verify_jwt_token(token)
        return StandardResponse(status="success", message="Token is valid", data={"username": payload.get("username")})
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
