from fastapi import APIRouter
from models.classroom import Classroom
from models.student import Student
from models.roll_call import RollCall
from utils.csv import to_csv_by_class


router = APIRouter()
header = ['', 'Lớp học', 'DS học viên', 'Trình độ', 'Số buổi\nhọc trong tháng', 'Ngày', 'Sĩ số lớp', 'Nội dung bài học']


@router.get('/')
def get_csv(month: str, classroom_id: int=None, student_id: int=None):
    # get_class
    if classroom_id:
        classroom = Classroom.get_one(classroom_id)
        students = Student.get_list(classroom_id)
        roll_call = RollCall.get_roll_call_by_month(month, classroom_id)
        to_csv_by_class([classroom], students, roll_call)

