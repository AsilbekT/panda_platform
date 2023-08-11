# auth_app/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    phone_number = Column(String)
    password_hash = Column(String)
    creation_date = Column(DateTime)


class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String)
    creation_date = Column(DateTime)
    expiration_date = Column(DateTime)
    user = relationship("User")
