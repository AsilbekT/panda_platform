from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, unique=True,
                          nullable=True)  # Can be null
    name = Column(String, nullable=True)  # Can be null
    username = Column(String, unique=True, nullable=True)  # Must not be null
    avatar = Column(String, nullable=True)  # Can be null
    preferences = Column(String, nullable=True)  # Can be null
    history = Column(String, nullable=True)  # Can be null
