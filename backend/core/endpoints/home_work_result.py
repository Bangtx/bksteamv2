from fastapi import APIRouter
import models.home_work_result as models
import schemas.home_work_result as schemas
from typing import List


router = APIRouter()


@router.get('/')
def get_home_work_result(classroom: int, student: int = None, date_from: str = None, date_to: str = None):
    return models.HomeWorkResult.get_list(classroom, student, date_from, date_to)


@router.post('/')
def create_home_work_result(home_work_results: List[schemas.HomeWorkResultCreate]):
    home_work_results = list(map(lambda x: x.dict(), home_work_results))
    return models.HomeWorkResult.create_new(home_work_results)
