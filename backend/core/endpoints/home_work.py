from fastapi import APIRouter
import schemas.home_work as schemas
import models.home_work as models
from typing import List
from utils.db import transaction

router = APIRouter()


@router.get('/', response_model=List[schemas.HomeWork])
def get_home_work(classroom: int, date_from: str = None, date_to: str = None):
    return models.HomeWork.get_list(classroom, date_from, date_to)


@router.post('/')
@transaction
def create_home_work(home_work: schemas.HomeWorkCreate):
    return models.HomeWork.create(**home_work.dict())


@router.put('/')
@transaction
def update_home_work(home_work: schemas.HomeWorkUpdate):
    return models.HomeWork.update_one(home_work.id, home_work.dict())
