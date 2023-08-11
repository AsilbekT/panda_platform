# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, unique=True)
    name = Column(String)
    username = Column(String, unique=True)
    avatar = Column(String, nullable=True)
    preferences = Column(String, nullable=True)
    history = Column(String, nullable=True)
    # password_hash = Column(String)
