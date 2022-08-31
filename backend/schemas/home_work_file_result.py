from schemas.base import Schema


class HomeWorkFileResultBase(Schema):
    home_work_file: int
    student: int
    file_result_url: str
    score: float = None


class Score(Schema):
    score: float = None
    id: int


class HomeWorkFileResult(HomeWorkFileResultBase):
    id: int


class HomeWorkFileResultCreate(HomeWorkFileResultBase):
    pass


class HomeWorkFileResultUpdate(HomeWorkFileResultBase):
    id: int


