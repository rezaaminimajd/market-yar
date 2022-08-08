from sqlalchemy.orm import Session
from sqlalchemy import null
from . import models, schemas
from apps.account import models as account_models

from apps import ticket


def create_ticket(db: Session, new_ticket_request: schemas.New_ticket, user_id: int):
    user = db.query(account_models.User).filter(account_models.User.id == user_id).one()
    ticket = models.Ticket(message=new_ticket_request.message, creator_id=user_id, creator_type=user.user_type)
    db.add(ticket)
    db.commit()
    "done"


def get_ticket(db: Session, user_id: int):
    tickets = []
    user = db.query(account_models.User).filter(account_models.User.id == user_id).one()
    if user.user_type == account_models.UserType.NORMAL:
        tickets += get_user_tickets(db, user_id)
    return tickets


def get_ticket_admin(db: Session, user_id: int):
    tickets = []
    user = db.query(account_models.User).filter(account_models.User.id == user_id).one()
    if user.user_type == account_models.UserType.ADMIN:
        tickets += get_addmin_tickets(db, user_id)
    elif user.user_type == account_models.UserType.BOSS:
        tickets += get_boss_tickets(db, user_id)
    return tickets



def get_boss_tickets(db, user_id: int):
    all_tickets = []
    all_tickets += db.query(models.Ticket).filter(
        models.Ticket.creator_type == account_models.UserType.ADMIN, models.Ticket.parent_ticket_id == null()).all()
    return all_tickets


def get_addmin_tickets(db, user_id: int):
    all_tickets = []
    all_tickets += get_user_tickets(db, user_id)
    all_tickets += db.query(models.Ticket).filter(models.Ticket.creator_type == account_models.UserType.NORMAL).all()
    return all_tickets


def get_user_tickets(db, user_id: int):
    all_tickets = []
    tickets = db.query(models.Ticket).filter(models.Ticket.creator_id == user_id).all()
    all_tickets += tickets
    for ticket in tickets:
        all_tickets += db.query(models.Ticket).filter(models.Ticket.parent_ticket_id == ticket.id).all()
    return all_tickets


def answer(db: Session, answer: schemas.Answer_ticket, user_id: int):
    user = db.query(account_models.User).filter(account_models.User.id == user_id).one()
    tickets = get_ticket(db, user_id)
    for ticket in tickets:
        if ticket.id == answer.parent_ticket_id:
            ticket = models.Ticket(message=answer.message, creator_id=user_id, parent_ticket_id=answer.parent_ticket_id,
                           creator_type=user.user_type)
            db.add(ticket)
            db.commit()
            return "done"
    return "Access Denied"

def answer_admin(db: Session, answer: schemas.Answer_ticket, user_id: int):
    user = db.query(account_models.User).filter(account_models.User.id == user_id).one()
    tickets = get_ticket_admin(db, user_id)
    for ticket in tickets:
        if ticket.id == answer.parent_ticket_id:
            ticket = models.Ticket(message=answer.message, creator_id=user_id, parent_ticket_id=answer.parent_ticket_id,
                           creator_type=user.user_type)
            db.add(ticket)
            db.commit()
            return "done"
    return "Access Denied"


def set_status(db: Session, new_status: schemas.New_status, user_id: int):
    tickets = get_ticket(db, user_id)
    for ticket in tickets:
        if ticket.id == new_status.ticket_id:
            db.query(models.Ticket).filter(models.Ticket.id == new_status.ticket_id).update(
                {models.Ticket.status: new_status.status})
            db.commit()
            return "done"
    return "Access Denied"

def set_status_admin(db: Session, new_status: schemas.New_status, user_id: int):
    tickets = get_ticket_admin(db, user_id)
    for ticket in tickets:
        if ticket.id == new_status.ticket_id:
            db.query(models.Ticket).filter(models.Ticket.id == new_status.ticket_id).update(
                {models.Ticket.status: new_status.status})
            db.commit()
            return "done"
    return "Access Denied"
