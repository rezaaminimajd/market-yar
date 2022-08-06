import aiofiles
import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from services.sql_app.database import get_db
from . import schemas, crud, models

router = APIRouter(
    prefix='/account',
    tags=['account']
)


@router.post('/register')
def register(user: schemas.RegisterUser, db=Depends(get_db)):
    user_db = crud.get_user(db, user.username, user.password)
    if user_db:
        raise HTTPException(status_code=400, detail="user already registered")
    crud.create_user(db, user)
    return 'user created'


@router.get('/inactive-admins')
def inactives_addmins(token: str, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.BOSS):
        raise HTTPException(status_code=401, detail="your not boss")
    return crud.get_inactive_admins(db)


@router.post('/active-admin/{admin_id}')
def activate_admin(admin_id: int, token: str, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.BOSS):
        raise HTTPException(status_code=401, detail="your not boss")
    crud.activate_user(db, admin_id)


@router.post('/active-user/{user_id}')
def activate_user(user_id: int, token: str, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.ADMIN):
        raise HTTPException(status_code=401, detail="your not admin")
    crud.activate_user(db, user_id)


@router.post('/login')
def login(user: schemas.UserLogin, db=Depends(get_db)):
    user_login = crud.get_user(db, username=user.username, password=user.password)
    if not user_login or not user_login.is_active:
        raise HTTPException(status_code=400, detail="user not exist! or not active")
    return crud.login(db, user_login.id)


@router.post('/logout')
def logout(user: schemas.UserLogout, db=Depends(get_db)):
    user_logout = crud.get_token(db, token=user.token)
    if not user_logout:
        raise HTTPException(status_code=400, detail="token not exist!")
    return crud.logout(db, user_logout)


@router.get("/videos")
def videos(db=Depends(get_db)):
    return crud.videos(db)


@router.get("/video/{video_id}")
def get_video(video_id: int, db=Depends(get_db)):
    return crud.get_video(db, video_id)


@router.get("/likes/{video_id}")
def get_likes(video_id: int, db=Depends(get_db)):
    return crud.likes(db, video_id)


@router.get("/dislikes/{video_id}")
def get_dislikes(video_id: int, db=Depends(get_db)):
    return crud.dislikes(db, video_id)


@router.get("/comments/{video_id}")
def get_comments(video_id: int, db=Depends(get_db)):
    return crud.comments(db, video_id)


@router.post("/add_comment/{token}")
def add_comment(token: str, comment: schemas.Comment, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for add comment, login first")
    crud.add_comment(db, comment, crud.get_token(db, token).user_id)
    return 'comment added!'


@router.post("/add_like/{token}")
def add_like(token: str, like: schemas.Like, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for like or dislike, login first")
    lod = crud.get_like_or_dislike(db, like.video_id, crud.get_token(db, token).user_id)
    if lod:
        if lod.is_like == like.is_like:
            return 'you can not like/dislike twice!'
        else:
            crud.delete_like(db, lod)
    crud.add_like(db, like, crud.get_token(db, token).user_id)
    return 'like added!'


@router.post("/upload")
async def upload_file(token: str, file: UploadFile, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for upload video, login first")
    path = f'{os.getcwd()}/videos/{file.filename}'
    async with aiofiles.open(path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    v = schemas.UploadVideo(
        file_path=path,
        user_id=crud.get_token(db, token).user_id
    )
    crud.upload_video(db, v)
    return f'file {file.filename} uploaded!'


@router.post("/inactivate/video/{video_id}")
def inactivate_video(token: str, video_id: int, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.ADMIN):
        raise HTTPException(status_code=401, detail="your not admin")


def create_superuser():
    crud.create_boss(next(get_db()))


create_superuser()
