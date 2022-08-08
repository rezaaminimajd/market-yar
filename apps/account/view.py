import aiofiles
import os

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from services.sql_app.database import get_db
from . import schemas, crud, models

router = APIRouter(
    prefix='/account',
    tags=['account']
)


def check_proxy(header):
    return header['host'] == '##proxy##admin##'


@router.post('/register')
def register(user: schemas.RegisterUser, db=Depends(get_db)):
    user_db = crud.get_user(db, user.username, user.password)
    if user_db:
        raise HTTPException(status_code=400, detail="user already registered")
    crud.create_user(db, user)
    return 'user created'


@router.get('/inactive-admins')
def inactives_admins(request: Request, token: str, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.BOSS):
        raise HTTPException(status_code=401, detail="your not boss")
    return crud.get_inactive_admins(db)


@router.post('/activate-admin/{admin_id}')
def activate_admin(request: Request, admin_id: int, token: str, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.BOSS):
        raise HTTPException(status_code=401, detail="your not boss")
    crud.activate_user(db, admin_id)
    return 'admin activate!'


@router.post('/active-user/{user_id}')
def activate_user(request: Request, user_id: int, token: str, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.ADMIN):
        raise HTTPException(status_code=401, detail="your not admin")
    crud.activate_user(db, user_id)
    return 'user activate!'


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
def videos(request: Request, db=Depends(get_db)):
    print(request.headers)
    return crud.videos(db)


@router.get("/video/{video_id}", response_class=HTMLResponse)
def get_video(request: Request, video_id: int, db=Depends(get_db)):
    return crud.get_video(db, video_id, request)


@router.get("/likes/{video_id}")
def get_likes(video_id, db=Depends(get_db)):
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


@router.get("/add_new_comment/{video_id}")
def add_comment(video_id: int, token: str, comment: str, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for add comment, login first")
    crud.add_new_comment(db, video_id, comment, crud.get_token(db, token).user_id)
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


@router.post("/add_new_like/{video_id}/{token}")
def add_new_like(video_id: int, token: str, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for like or dislike, login first")
    lod = crud.get_like_or_dislike(db, video_id, crud.get_token(db, token).user_id)
    if lod:
        if lod.is_like:
            return 'you can not like/dislike twice!'
        else:
            crud.delete_like(db, lod)
    crud.add_new_like(db, video_id, crud.get_token(db, token).user_id)
    return 'like added!'


@router.post("/add_new_dislike/{video_id}/{token}")
def add_new_dislike(video_id: int, token: str, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for like or dislike, login first")
    lod = crud.get_like_or_dislike(db, video_id, crud.get_token(db, token).user_id)
    if lod:
        if not lod.is_like:
            return 'you can not like/dislike twice!'
        else:
            crud.delete_like(db, lod)
    crud.add_new_dislike(db, video_id, crud.get_token(db, token).user_id)
    return 'dislike added!'


@router.post("/upload")
async def upload_file(token: str, file: UploadFile, db=Depends(get_db)):
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for upload video, login first")
    if crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.ADMIN):
        raise HTTPException(status_code=401, detail="you are admin")
    path = f'{os.getcwd()}/static/{file.filename}'
    async with aiofiles.open(path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    v = schemas.UploadVideo(
        file_path=file.filename,
        user_id=crud.get_token(db, token).user_id
    )
    crud.upload_video(db, v)
    return f'file {file.filename} uploaded!'


@router.post("/inactivate/video/{video_id}")
def inactivate_video(request: Request, token: str, video_id: int, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.ADMIN):
        raise HTTPException(status_code=401, detail="your not admin")
    crud.inactivate_video(db, video_id)
    return 'video inactivate!'


@router.post('/label/video/{video_id}')
def label_video(request: Request, token: str, video_id: int, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="first login")
    if not crud.check_type(db, crud.get_token(db, token).user_id, models.UserType.ADMIN):
        raise HTTPException(status_code=401, detail="your not admin")
    crud.label_video(db, video_id)
    return 'add bad label!'


def create_superuser():
    crud.create_boss(next(get_db()))


create_superuser()
