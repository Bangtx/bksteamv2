import models.classroom as models
import schemas.classroom as schemas
from fastapi import APIRouter
from utils.db import transaction
from models.student import Student
from models.teacher import Teacher

router = APIRouter()


@router.get('/')
def get_classrooms(teacher_id: int = None, student_id: int = None):
    if teacher_id:
        return Teacher.get_classrooms(teacher_id)
    if student_id:
        return Student.get_classrooms(student_id)
    return models.Classroom.get_list()


@router.get('/{id}')
def get_classroom_by_id(id: int):
    return models.Classroom.get_one(id)


@router.post('/')
def create_classroom(classroom: schemas.ClassRoomCreate):
    classroom_data = classroom.dict()
    return models.Classroom.create(**classroom_data)


@router.put('/{id}')
def get_classroom_by_id(id: int, classroom: schemas.ClassRoomUpdate):
    return models.Classroom.update_one(id, classroom.dict())


@router.delete('/{id}')
@transaction
def delete_classroom(id: int):
    return models.Classroom.soft_delete(id)
