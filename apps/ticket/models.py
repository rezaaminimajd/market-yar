from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, null
from services.sql_app.database import Base
from sqlalchemy.dialects.postgresql import ENUM
from apps.account import models as account_models


class Status(Enum):
    NEW = 'NEW'
    WAITING = 'WAITING'
    DONE = 'DONE'
    CLOSED = 'CLOSED'


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key = True, index = True)
    message = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator_type = Column(ENUM(account_models.UserType))
    parent_ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable = True, default = null())
    status = Column(ENUM(Status), default = Status.NEW)