from fastapi import APIRouter
import csv
from models.teacher import Teacher
from models.student import Student
from models.classroom import Classroom
from utils.db import transaction


router = APIRouter()


@router.get('/import')
@transaction
def import_data():
    import_student()


def import_student():
    csv_file = open('core/endpoints/BK WEB_HỌC VIÊN - HV.csv')
    csv_reader = list(csv.reader(csv_file))[1:]
    student_exists = Student.get_list()
    student_name_exists = list(map(lambda x: x['name'], student_exists))
    class_exists = Classroom.get_list()
    print(class_exists)
    list_class = []

    clas = list(
        set(
            list(
                map(lambda x: x[2], csv_reader)
            )
        )
    )

    students = list(map(lambda x: x[0], csv_reader))

    # data = []
    # for i in clas:
    #     Classroom.create(name=i)

    for row in csv_reader:
        name = row[0]
        clas = row[2]
        phone = row[5]
        if phone == '' or phone is None:
            continue

        if not name in student_name_exists:
            student_name_exists.append(name)
            student = {
                'name': name,
                'password': 'student',
                'phone': '0' + phone,
                'classrooms': list(map(lambda x: x['id'], list(filter(lambda x: x['name'] == clas, class_exists))))
            }
            Student.create(**student)

    # teachers = [
    #     {'name': 'Phạm Việt Hưng', 'phone': '0967528503', 'gender': 'Name'},
    #     {'name': 'Nguyễn Thị Minh Tâm', 'phone': '0986303740', 'gender': 'Name'},
    #     {'name': 'Nguyễn Trần Bảo Ngọc', 'phone': '0975942067', 'gender': 'Name'},
    #     {'name': 'Đoàn Thị Mỹ Dung', 'phone': '0932202936', 'gender': 'Name'},
    #     {'name': 'Rhonna Mae Clare Inot Maasin', 'phone': '0325578127', 'gender': 'Name'},
    # ]
    # for teacher in teachers:
    #     teacher['password'] = 'password'
    #
    #     Teacher.create(**teacher)