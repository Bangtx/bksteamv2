from models.file_base import FileBase
from peewee import (
    CharField
)


class Image(FileBase):
    DIR = 'image'
    class Meta:
        db_table = 'image'