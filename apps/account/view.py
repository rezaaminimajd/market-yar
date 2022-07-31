import aiofiles
import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from services.sql_app.database import get_db
from . import schemas, crud

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
