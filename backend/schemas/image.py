from schemas.base import Schema


class Image(Schema):
    name: str
    room: str = None