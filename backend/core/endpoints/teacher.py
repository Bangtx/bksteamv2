import models.teacher as models
from models.classroom import Classroom
import schemas.teacher as schemas
from fastapi import APIRouter, HTTPException
from utils.db import transaction

router = APIRouter()


@router.get('/')
def get_teachers(classroom: int = None):
    return models.Teacher.get_list(classroom)


@router.get('/{id}')
def get_teachers(id: int):
    return models.Teacher.get_teacher_by_id(id)


@router.post('/', response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate):
    return models.Teacher.create(**teacher.dict())


@router.put('/{id}', response_model=schemas.Teacher)
def update_teacher(id: int, teacher: schemas.TeacherUpdate):
    return models.Teacher.update_one(id, teacher.dict())


@router.delete('/{id}')
@transaction
def delete_teacher(id: int):
    return models.Teacher.soft_delete(id)