import traceback
from fastapi import HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import decode_jwt_token
from .models import UserProfile
from .database import get_db
from .schemas import UserProfileCreate, StandardResponse
from sqlalchemy.future import select
from sqlalchemy import or_

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_token_from_header(authorization: str = Depends(api_key_header)) -> str:
    if authorization is None:
        raise HTTPException(
            status_code=401, detail="You must be logged in to access this resource")

    try:
        token_type, token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authorization type")
        return token
    except ValueError:
        raise HTTPException(
            status_code=401, detail="Invalid authorization header")


async def create_profile(profile: UserProfileCreate, db: AsyncSession = Depends(get_db)) -> StandardResponse:
    # Check for existing user with the same username or phone number
    existing_user = (
        await db.execute(
            select(UserProfile).filter(
                or_(
                    UserProfile.username == profile.username,
                    UserProfile.phone_number == profile.phone_number
                )
            )
        )
    ).scalar_one_or_none()

    if existing_user:
        # Determine which field is causing the conflict
        conflict_field = "username" if existing_user.username == profile.username else "phone number"
        raise HTTPException(
            status_code=400, detail=f"{conflict_field.capitalize()} already exists")

    db_profile = UserProfile(
        phone_number=profile.phone_number,
        name=profile.name,
        username=profile.username,
        avatar=profile.avatar,
        preferences=profile.preferences,
        history=profile.history
    )

    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)

    return StandardResponse(status="success", message="User created successfully")


async def get_profile(token: str = Depends(get_token_from_header), db: AsyncSession = Depends(get_db)) -> StandardResponse:
    try:
        token_data = decode_jwt_token(token)
    except Exception as e:
        print(f"An error occurred while decoding the token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    username = token_data['username']

    db_profile = (await db.execute(select(UserProfile).filter(UserProfile.username == username))).scalar_one_or_none()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    response_data = UserProfileCreate.from_orm(db_profile)

    return StandardResponse(status="success", message="Profile retrieved successfully", data=response_data)


async def update_profile(profile_update: UserProfileCreate, token: str = Depends(get_token_from_header), db: AsyncSession = Depends(get_db)) -> StandardResponse:
    token_data = decode_jwt_token(token)
    username = token_data['username']
    result = await db.execute(select(UserProfile).filter(UserProfile.username == username))
    db_profile = result.scalar_one_or_none()

    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in profile_update.dict().items():
        if hasattr(db_profile, key) and value is not None:
            setattr(db_profile, key, value)

    await db.commit()
    await db.refresh(db_profile)
    response_data = UserProfileCreate.from_orm(
        db_profile)  # Use your response model here
    return StandardResponse(status="success", message="Profile updated successfully", data=response_data)


async def delete_profile(token: str = Depends(get_token_from_header), db: AsyncSession = Depends(get_db)) -> StandardResponse:
    token_data = decode_jwt_token(token)
    username = token_data['username']
    result = await db.execute(select(UserProfile).filter(UserProfile.username == username))
    db_profile = result.scalar_one_or_none()
    print(db_profile)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    await db.delete(db_profile)
    await db.commit()
    return StandardResponse(status="success", message="Profile deleted successfully")
