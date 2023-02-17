from fastapi import APIRouter
import schemas.home_work as schemas
import models.home_work as models
from typing import List
from utils.db import transaction
from models.audio import Audio
from base64 import b64decode

router = APIRouter()


@router.get('/', response_model=List[schemas.HomeWork])
def get_home_work(classroom: int, date_from: str = None, date_to: str = None):
    return models.HomeWork.get_list(classroom, date_from, date_to)


@router.post('/')
@transaction
def create_home_work(home_work: schemas.HomeWorkCreate):
    file = Audio.create(b64decode(home_work.audio.split(',').pop()))
    home_work.audio = file.id
    return models.HomeWork.create(**home_work.dict())


@router.put('/')
@transaction
def update_home_work(home_work: schemas.HomeWorkUpdate):
    home_work = home_work.dict()
    if home_work['audio'].find('http') == -1:
        file = Audio.create(b64decode(home_work['audio'].split(',').pop()))
        home_work['audio'] = file.id
    else:
        home_work.pop('audio', None)
    return models.HomeWork.update_one(home_work['id'], home_work)


@router.delete('/{id}')
@transaction
def delete_home_work(id: int):
    return models.HomeWork.soft_delete(id)