import schemas.login as schemas
from fastapi import APIRouter, Depends
from models.teacher import Teacher
from models.student import Student
import hashlib
import json
from utils.auth import Auth

router = APIRouter()


@router.get('/test_auth')
def test(data=Depends(Auth())):
    return {'msg': data}


@router.post('/login')
def login(account: schemas.AccountLogin):
    if account.is_teacher:
        teacher = Teacher.get_one(account.id)
        if teacher:
            return {
                'status': 200,
                'token': {
                    'name': teacher['name'], 'id': teacher['id'], 'type_member': 'teacher'
                }
            }
    else:
        student = Student.get_one(account.id)
        if student:
            return {
                'status': 200,
                'token': {
                    'name': student['name'], 'id': student['id'], 'type_member': 'student'
                }
            }
    return {'status': 404}