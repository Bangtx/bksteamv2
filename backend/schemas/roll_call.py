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


class RollCallCreate(RollCallBase):
    pass


class RollCallUpdate(RollCallBase):
    pass