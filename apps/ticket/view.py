from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from slowapi.util import get_remote_address
from slowapi import Limiter
from services.sql_app.database import get_db
from . import schemas, crud
from apps.account import crud as account_crud

router = APIRouter(
    prefix='/ticket',
    tags=['ticket']
)
limiter = Limiter(key_func=get_remote_address)



def check_proxy(header):
    return header['host'] == '##proxy##admin##'


@router.post("/new")
def create_item(token: str, req: schemas.New_ticket, db=Depends(get_db)):
    if not account_crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for create ticket, login first")
    return crud.create_ticket(db, req, account_crud.get_token(db, token).user_id)


@router.get('/all')
def get_tickets(token: str, db=Depends(get_db)):
    if not account_crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for get tickets, login first")
    return crud.get_ticket(db, account_crud.get_token(db, token).user_id)


@router.get('/all/asadmin')
def get_tickets(request: Request, token: str, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not account_crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for get tickets, login first")
    return crud.get_ticket_admin(db, account_crud.get_token(db, token).user_id)


@router.post('/answer')
def answer_ticket(token: str, req: schemas.Answer_ticket, db=Depends(get_db)):
    if not account_crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for answer ticket, login first")
    return crud.answer(db, req, account_crud.get_token(db, token).user_id)


@router.post('/answer/asadmin')
def answer_ticket(request: Request, token: str, req: schemas.Answer_ticket, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not account_crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for answer ticket, login first")
    return crud.answer_admin(db, req, account_crud.get_token(db, token).user_id)


@router.post('/set-status')
def set_status(token: str, req: schemas.New_status, db=Depends(get_db)):
    if not account_crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for set ticket status, login first")
    return crud.set_status(db, req, account_crud.get_token(db, token).user_id)


@router.post('/set-status/asadmin')
def set_status(request: Request, token: str, req: schemas.New_status, db=Depends(get_db)):
    if not check_proxy(request.headers):
        raise HTTPException(status_code=403, detail="invalid hostname")
    if not account_crud.is_user(db, token):
        raise HTTPException(status_code=401, detail="for set ticket status, login first")
    return crud.set_status_admin(db, req, account_crud.get_token(db, token).user_id)
