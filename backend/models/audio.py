from models.file_base import FileBase
from peewee import (
    CharField
)


class Audio(FileBase):
    class Meta:
        db_table = 'audio'
