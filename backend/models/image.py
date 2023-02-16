from models.file_base import FileBase
from peewee import (
    CharField
)


class Image(FileBase):
    class Meta:
        db_table = 'image'