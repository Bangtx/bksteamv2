from schemas.base import Schema
from datetime import date


class HomeWorkBase(Schema):
    date: date
    deadline: date = None
    classroom: int
    question: str
    unit: int = None
    audio: str = None
    multi_choice: bool
    option_1: str = None
    option_2: str = None
    option_3: str = None
    option_4: str = None
    answer: str = None
    have_to_do: bool = False


class HomeWork(HomeWorkBase):
    id: int


class HomeWorkCreate(HomeWorkBase):
    pass


class HomeWorkUpdate(HomeWorkCreate):
    id: int
