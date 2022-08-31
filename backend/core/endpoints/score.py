from typing import List
from fastapi import APIRouter
from utils.db import transaction
import json

import schemas.score as schemas
import models.score as models

router = APIRouter()


@router.get('/')
def get_scores(classroom: int):
    return models.Score.get_class_room(classroom)


@router.post('/')
@transaction
def create_scores(params: List[schemas.ScoreCreate]):
    result = []
    for param in params:
        result.append(models.Score.create(**param.dict()))
    return result
