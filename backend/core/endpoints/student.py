import models.student as models
import schemas.student as schemas
from fastapi import APIRouter
from utils.db import transaction

router = APIRouter()


@router.get('/')
def get_students(classroom: int = None):
    return models.Student.get_list(classroom)


@router.get('/{id}')
def get_students(id: int):
    return models.Student.get_students_by_id(id)


@router.post('/', response_model=schemas.Student)
@transaction
def create_student(student: schemas.StudentCreate):
    return models.Student.create(**student.dict())


@router.put('/{id}', response_model=schemas.Student)
@transaction
def update_student(id: int, student: schemas.StudentUpdate):
    return models.Student.update_one(id, student.dict())


@router.delete('/{id}')
@transaction
def delete_student(id: int):
    return models.Student.soft_delete(id)
