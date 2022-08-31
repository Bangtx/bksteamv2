from schemas.base import Schema
from datetime import date
from typing import Optional, List


class HomeWorkFileBase(Schema):
    date: date
    deadline: Optional[date]
    classroom: int
    unit: int = None
    file_url: str
    description: str = None
    is_global: bool = False
    student_ids: List[int] = []
    have_to_do: bool = False


class HomeWorkFile(HomeWorkFileBase):
    id: int


class HomeWorkFileCreate(HomeWorkFileBase):
    pass


class HomeWorkFileUpdate(HomeWorkFileCreate):
    id: int

        