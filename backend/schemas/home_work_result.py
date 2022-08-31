from schemas.base import Schema


class HomeWorkResultBase(Schema):
    home_work: int
    student: int
    answer: str
    is_correct: bool = False


class HomeWorkResult(HomeWorkResultBase):
    id: int


class HomeWorkResultCreate(HomeWorkResultBase):
    id: int = None


class HomeWorkResultUpdate(HomeWorkResultCreate):
    pass


    