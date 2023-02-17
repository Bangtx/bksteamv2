from models.file_base import FileBase
from peewee import (
    CharField
)


class Audio(FileBase):
    DIR = 'audio'

    class Meta:
        db_table = 'audio'
