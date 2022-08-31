from models.base import BaseModel
from peewee import (
    CharField
)


class Classroom(BaseModel):
    name = CharField()
    room = CharField()

    class Meta:
        db_table = 'classroom'
