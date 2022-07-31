from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
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
    password = Column(String)
    user_type = Column(ENUM(UserType), nullable=False, default=UserType.NORMAL.value)
    is_active = Column(Boolean)


class UserLoginToken(Base):
    __tablename__ = "login_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String, unique=True)


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_path = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String, nullable=False)


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_like = Column(Boolean, nullable=False)
