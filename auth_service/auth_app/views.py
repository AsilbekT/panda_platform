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


class UserCreate(BaseModel):
    username: str
    phone_number: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


async def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username,
                   phone_number=user.phone_number, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # response = requests.post("http://user_service/profiles", json={"username": user.username})
    # if response.status_code != 200:
    #     raise HTTPException(status_code=500, detail="Failed to create user profile")

    return {"username": user.username, "message": "User created successfully"}


async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_data = {"sub": db_user.id, "username": db_user.username}
    token = create_jwt_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


def get_token(authorization: str = Header(None)) -> str:
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        return token
    raise HTTPException(status_code=401, detail="Invalid token")


async def logout(token: str = Depends(get_token)):
    token_blacklist.add(token)  # Add the token to the blacklist
    return {"message": "Successfully logged out"}


async def verify_token(token: str = Depends(get_token)):
    if token in token_blacklist:  # Check if the token is in the blacklist
        raise HTTPException(
            status_code=401, detail="Token has been invalidated")

    try:
        payload = verify_jwt_token(token)
        return {"username": payload.get("username"), "message": "Token is valid"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
