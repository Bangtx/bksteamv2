from fastapi import APIRouter
import models.home_work_file_result as models
import schemas.home_work_file_result as schemas
from utils.db import transaction
from typing import List


router = APIRouter()


@router.get('/')
def get_home_work_file_result(classroom: int, student: int = None, date_from: str = None, date_to: str = None):
    return models.HomeWorkFileResult.get_list(classroom, student, date_from, date_to)


@router.post('/')
@transaction
def get_home_work_file_result(home_work_file_results: List[schemas.HomeWorkFileResultCreate]):
    home_work_file_results = list(map(lambda x: x.dict(), home_work_file_results))
    return models.HomeWorkFileResult.create_new(home_work_file_results)


@router.put('/score')
@transaction
def update_home_work_file_result(home_work_file_results: schemas.Score):
    return models.HomeWorkFileResult.update_one(home_work_file_results.id, home_work_file_results.dict())

