from schemas.base import Schema


class ClassRoomBase(Schema):
    name: str
    room: str = None


class ClassRoomCreate(ClassRoomBase):
    pass


class ClassRoomUpdate(ClassRoomBase):
    pass
