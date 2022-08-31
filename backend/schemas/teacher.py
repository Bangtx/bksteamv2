from schemas.login import AccountBase
from datetime import date
from schemas.base import Schema
from typing import List, Optional


class TeacherBase(AccountBase):
    pass


class Teacher(TeacherBase):
    id: int
    name: str
    gender: str = None
    date_of_birth: date = None
    mail: str = None
    phone: str = None
    classrooms: List[int] = []


class TeacherCreate(TeacherBase):
    classrooms: List[int] = []


class TeacherUpdate(Schema):
    name: str
    gender: str = None
    date_of_birth: date = None
    mail: str = None
    phone: str = None
    classrooms: List[int] = []
