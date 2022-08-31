from schemas.login import AccountBase
from datetime import date
from schemas.base import Schema
from typing import List, Optional


class StudentBase(AccountBase):
    status: Optional[int]


class StudentCreate(StudentBase):
    classrooms: List[int] = []


class Student(Schema):
    id: int
    name: str
    gender: str = None
    date_of_birth: date = None
    mail: str = None
    phone: str = None
    classrooms: List[int] = []


class StudentUpdate(Schema):
    name: str
    gender: str = None
    date_of_birth: date = None
    mail: str = None
    phone: str = None
    classrooms: List[int] = []
    status: Optional[int]
