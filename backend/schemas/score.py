from schemas.base import Schema
from datetime import date
from typing import List


class ScoreBase(Schema):
    date: date
    classroom: int
    student: int
    teacher: int = None
    specking: float = None
    reading: float = None
    writing: float = None
    listening: float = None


class Score(ScoreBase):
    id: int


class ScoreCreate(ScoreBase):
    pass
