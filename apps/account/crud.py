from pyexpat import model
from unittest import mock
from sqlalchemy.orm import Session
from uuid import uuid4
from sqlalchemy import desc

from . import models, schemas


def create_user(db: Session, user: schemas.RegisterUser):
    db_user = models.User(
        username=user.username,
        password=user.password,
        nickname=user.nickname,
        user_type=user.user_type,
        is_active=True if user.user_type == schemas.UserType.NORMAL.value else False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str, password: str):
    return db.query(models.User).filter(models.User.username == username and models.User.password == password).first()



def get_token(db: Session, token: str):
    return db.query(models.UserLoginToken).filter(models.UserLoginToken.token == token).first()


def login(db: Session, user_id: int):
    db_user_login = db.query(models.UserLoginToken).filter(models.UserLoginToken.user_id == user_id).first()
    if db_user_login:
        return db_user_login.token
    db_user_login = models.UserLoginToken(
        user_id=user_id,
        token=uuid4()
    )
    db.add(db_user_login)
    db.commit()
    db.refresh(db_user_login)
    return db_user_login.token


def is_user(db: Session, token: str):
    user = db.query(models.UserLoginToken).filter(models.UserLoginToken.token == token).first()
    if user:
        return True
    else:
        return False

def check_type(db: Session, user_id: int, type: models.UserType):
    user = db.query(models.User).filter(models.User.id == user_id).one()
    if user.user_type == type:
        return True
    return False

def get_inactive_admins(db: Session):
    admins = db.query(models.User).filter(models.User.user_type == models.UserType.ADMIN and models.User.is_active == False).all()
    return admins
    
def activate_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).update({models.User.is_active: True})
    db.commit()
    


def logout(db: Session, user_logout_token: models.UserLoginToken):
    db.delete(user_logout_token)
    db.commit()
    return user_logout_token.token


def videos(db: Session):
    return db.query(models.Video).filter(models.Video.is_active).all()


def comments(db: Session, video_id: int):
    return db.query(models.Comment).filter(models.Comment.video_id == video_id).all()


def likes(db: Session, video_id: int):
    return db.query(models.Like).filter(models.Like.is_like and models.Like.video_id == video_id).all()


def dislikes(db: Session, video_id: int):
    return db.query(models.Like).filter(not models.Like.is_like and models.Like.video_id == video_id).all()


def add_comment(db: Session, comment: schemas.Comment, user_id: int):
    db_comment = models.Comment(
        text=comment.text,
        video_id=comment.video_id,
        user_id=user_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def add_like(db: Session, like: schemas.Like, user_id: int):
    db_like = models.Like(
        is_like=like.is_like,
        video_id=like.video_id,
        user_id=user_id,
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

#check func
def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id and models.Video.is_active).first()


def upload_video(db: Session, video: schemas.UploadVideo):
    db_video = models.Video(
        file_path=video.file_path,
        user_id=video.user_id,
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def inactivate_video(db: Session, video_id):
    video = db.query(models.Video).filter(models.Video.id == video_id).one()
    videos = db.query(models.Video).filter(models.Video.user_id == video.user_id).order_by(desc(models.Video.id))
    if videos[0].is_active == False:
       db.query(models.User).filter(models.User.id == video.user_id).update({models.User.is_active: False})
    db.query(models.Video).filter(models.Video.id == video_id).update({models.Video.is_active: False})
    db.commit()
    
def create_boss(db: Session):
    user = db.query(models.User).filter(models.User.user_type == models.UserType.BOSS).first()
    
    if user:
        return
    boss = models.User(username='manager',
                        password='supreme_manager#2022',
                        nickname='boss',
                        user_type=models.UserType.BOSS,
                        is_active=True)
    db.add(boss)
    db.commit()

    
