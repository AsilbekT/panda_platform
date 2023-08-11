# views.py

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from .models import UserProfile
from .database import get_db
from .schemas import UserProfileCreate, UserProfileResponse
# from .utils import verify_jwt_token


def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserProfile).filter(
        (UserProfile.username == profile.username) |
        (UserProfile.phone_number == profile.phone_number)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_profile = UserProfile(
        phone_number=profile.phone_number,
        name=profile.name,
        username=profile.username,
        avatar=profile.avatar,
        preferences=profile.preferences,
        history=profile.history
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return {"message": "User created successfully"}


def get_profile(id: int, db: Session = Depends(get_db)) -> UserProfileResponse:
    db_profile = db.query(UserProfile).filter(UserProfile.id == id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


def update_profile(id: int, profile_update: UserProfileCreate, db: Session = Depends(get_db)) -> UserProfileResponse:
    db_profile = db.query(UserProfile).filter(UserProfile.id == id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    for key, value in profile_update.dict().items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(id: int, db: Session = Depends(get_db)):
    db_profile = db.query(UserProfile).filter(UserProfile.id == id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(db_profile)
    db.commit()
    return {"message": "Profile deleted successfully"}
