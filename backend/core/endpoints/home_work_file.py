from fastapi import APIRouter
import models.home_work_file as models
import schemas.home_work_file as schemas

router = APIRouter()


@router.get('/')
def get_home_work_file(
    classroom: int = None, student: int = None, date_from: str = None, date_to: str = None
):
    return models.HomeWorkFile.get_list(classroom, student, date_from, date_to)


@router.post('/')
def create_home_work_file(home_work_file: schemas.HomeWorkFileCreate):
    return models.HomeWorkFile.create(**home_work_file.dict())


@router.put('/')
def update_home_work_file(home_work_file: schemas.HomeWorkFileUpdate):
    return models.HomeWorkFile.update_one(home_work_file.id, home_work_file.dict())


@router.delete('/{id}')
def delete_home_work_file(id: int):
    return models.HomeWorkFile.soft_delete(id)
