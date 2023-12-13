from fastapi import HTTPException, Header, Depends, Request
from .models import User, UserSession
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

MAX_SESSIONS = 3


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


async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)) -> StandardResponse:
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Get device information and IP address from the request
    request_data = await request.json()
    device_info = request_data.get('device_info')
    client_host = request.client.host
    print(request)
    # Check and manage the number of active sessions
    active_sessions = db.query(UserSession).filter(
        UserSession.user_id == db_user.id,
        UserSession.logged_out == False
    ).order_by(UserSession.created_at.asc()).all()

    if len(active_sessions) >= MAX_SESSIONS:
        # Log out the oldest session if the maximum number of sessions is exceeded
        oldest_session = active_sessions[0]
        db.delete(oldest_session)

    # Create a new session
    new_session = UserSession(
        user_id=db_user.id,
        device_info=device_info,
        ip_address=client_host
    )
    db.add(new_session)

    # Create JWT token
    token_data = {"sub": db_user.id, "username": db_user.username}
    token = create_jwt_token(token_data)

    db.commit()

    return StandardResponse(
        status="success",
        message="Login successful",
        data={
            "access_token": token,
            "token_type": "bearer"
        }
    )


def get_token(authorization: str = Header(None)) -> str:
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        return token
    raise HTTPException(status_code=401, detail="Invalid token")


async def logout(token: str = Depends(get_token), db: Session = Depends(get_db)) -> StandardResponse:
    try:
        # Decode the token to get the username
        payload = verify_jwt_token(token)
        username = payload.get("username")

        # Retrieve the user based on the username
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Delete the user's session
    user_session = db.query(UserSession).filter(
        UserSession.user_id == user.id
    ).first()
    if user_session:
        db.delete(user_session)
        token_blacklist.add(token)
        db.commit()

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


async def get_active_sessions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sessions = user.get_active_sessions(db)
    return sessions  # Modify this return statement as per your response schema


async def logout_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(UserSession).get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.logout()
    db.commit()
    return {"message": "Logged out from the session successfully"}
