from schemas.base import Schema
from datetime import date
from typing import Optional, List


class AccountLogin(Schema):
    password: str
    id: str
    is_teacher: bool = False


class AccountBase(Schema):
    name: str
    gender: str = None
    date_of_birth: date = None
    password: str
    mail: str = None
    phone: str = None
