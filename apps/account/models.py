from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey
from services.sql_app.database import Base
from sqlalchemy.dialects.postgresql import ENUM


class UserType(Enum):
    NORMAL = 'NORMAL'
    ADMIN = 'ADMIN'
    BOSS = 'BOSS'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    nickname = Column(String)
    hashed_password = Column(String)
    user_type = Column(ENUM(UserType), nullable=False)


class UserLoginToken(Base):
    __tablename__ = "login_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, unique=True)
