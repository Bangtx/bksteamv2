from schemas.base import Schema


class Slide(Schema):
    title: str
    remark: str = None
    url: str
    classroom: int


class SlideUpdate(Schema):
    title: str
    remark: str = None
    url: str
    classroom: int
    id: int
