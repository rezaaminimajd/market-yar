from sqlalchemy.orm import Session
from uuid import uuid4

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
    return db.query(models.User).filter(models.User.username == username, models.User.password == password).first()


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


def logout(db: Session, user_logout_token: models.UserLoginToken):
    db.delete(user_logout_token)
    db.commit()
    return user_logout_token.token


def videos(db: Session):
    return db.query(models.Video).all()


def comments(db: Session, video_id: int):
    return db.query(models.Comment).filter(models.Comment.video_id == video_id).all()


def likes(db: Session, video_id: int):
    return db.query(models.Like).filter(models.Like.is_like, models.Like.video_id == video_id).all()


def get_like(db: Session, video_id: int, user_id: int):
    return db.query(models.Like).filter(
        models.Like.is_like, models.Like.video_id == video_id, models.Like.user_id == user_id
    ).first()


def dislikes(db: Session, video_id: int):
    return db.query(models.Like).filter(models.Like.is_like != True, models.Like.video_id == video_id).all()


def get_dislike(db: Session, video_id: int, user_id: int):
    return db.query(models.Like).filter(
        models.Like.is_like != True, models.Like.video_id == video_id, models.Like.user_id == user_id
    ).first()


def get_like_or_dislike(db: Session, video_id: int, user_id: int):
    return db.query(models.Like).filter(models.Like.video_id == video_id, models.Like.user_id == user_id).first()


def delete_like(db: Session, like: models.Like):
    db.delete(like)
    db.commit()


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


def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()


def upload_video(db: Session, video: schemas.UploadVideo):
    db_video = models.Video(
        file_path=video.file_path,
        user_id=video.user_id,
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
