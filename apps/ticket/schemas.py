from pydantic import BaseModel

from enum import Enum


class Status(str, Enum):
    NEW = 'NEW'
    WAITING = 'WAITING'
    DONE = 'DONE'
    CLOSED = 'CLOSED'



class New_ticket(BaseModel):
    message : str

class Answer_ticket(BaseModel):
    message : str
    parent_ticket_id: int


class New_status(BaseModel):
    ticket_id : int
    status: Status

