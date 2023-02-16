from models.base import BaseModel
from peewee import (
    CharField
)


class FileBase(BaseModel):
    url = CharField()
    path = CharField()
