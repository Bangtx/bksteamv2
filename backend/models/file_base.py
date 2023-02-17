from models.base import BaseModel
from peewee import (
    CharField
)
from datetime import datetime
from config.setting import VUE_APP_API_URL


class FileBase(BaseModel):
    url = CharField()
    path = CharField()
    DIR = ''

    @classmethod
    def create(cls, file):
        time_now = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        if cls.DIR == '': return
        path = f"{cls.DIR}/{time_now}.{'png' if cls.DIR == 'image' else 'mp3'}"
        with open(path, 'wb+') as file_object:
            file_object.write(file)

        url = f'{VUE_APP_API_URL}/{cls.DIR}?path={path}'

        return super().create(url=url, path=path)
