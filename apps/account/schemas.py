from pydantic import BaseModel

from enum import Enum


class UserType(str, Enum):
    NORMAL = 'NORMAL'
    ADMIN = 'ADMIN'


class RegisterUser(BaseModel):
    username: str
    nickname: str
    password: str
    user_type: UserType


class UserLogin(BaseModel):
    username: str
    password: str


class UserLogout(BaseModel):
    token: str


class UploadVideo(BaseModel):
    user_id: int
    file_path: str


class Comment(BaseModel):
    video_id: int
    text: str


class Like(BaseModel):
    video_id: int
    is_like: bool
