from schemas.base import Schema
from datetime import date


class RollCallBase(Schema):
    date: date
    classroom: int
    student: int
    teacher: int = None
    absent_type: int = None


class RollCall(RollCallBase):
    pass


class RollCallCreate(Schema):
    date: date
    payload: dict
    classroom: int
    teacher: int
