from models.base import BaseModel
from peewee import IntegerField, ForeignKeyField, fn, DateField, JOIN
from models.teacher import Teacher
from models.student import Student
from models.classroom import Classroom


class RollCall(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    date = DateField()
    student = ForeignKeyField(Student, column_name='student_id')
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    absent_type = IntegerField()

    class Meta:
        db_table = 'roll_call'

    @classmethod
    def get_list(cls, classroom):
        dates = list(
            cls.select(
                cls.date
            ).where(
                cls.active, cls.classroom == classroom
            ).order_by(
                cls.date.asc()
            ).dicts()
        )
        dates = list(set(list(map(lambda x: x['date'], dates))))
        students = Student.get_list(classroom)

        datas = []
        for date in dates:
            data = {
                'date': date,
                'students': []
                # student['id']: list(map(lambda x: x['absent_type'], roll_call))
            }
            for student in students:
                roll_call = list(cls.select().where(
                    cls.student == student['id'], cls.date == date, cls.classroom == classroom, cls.active
                ).dicts())
                data['students'].append({
                    student['id']: list(map(lambda x: x['absent_type'], roll_call))
                })
            datas.append(data)

        return datas

    @classmethod
    def get_roll_call_by_date(cls, date, class_room, student=None):
        roll_calls = (
            cls.select(
                cls.id,
                fn.json_build_object('id', Student.id, 'name', Student.name).alias('student'),
                fn.json_build_object('id', Teacher.id, 'name', Teacher.name).alias('teacher'),
                cls.absent_type
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                Student, JOIN.LEFT_OUTER, on=Student.id == cls.student
            ).join(
                Teacher, JOIN.LEFT_OUTER, on=Teacher.id == cls.teacher
            ).where(
                cls.active, Classroom.active, cls.date == date, cls.classroom == class_room
            ).dicts()
        )

        if student:
            roll_calls = roll_calls.where(cls.student == student)

        return list(roll_calls)

    @classmethod
    def get_roll_call_by_month(cls, month, class_room, student=None):
        first = f'{month}-01'
        last = f'{month}-28'
        day_31 = [1, 3, 5, 7, 8, 10, 12]
        day_30 = [4, 6, 9, 11]
        day_28 = [2]
        if int(month[-1]) in day_31:
            last = f'{month}-31'
        if int(month[-1]) in day_30:
            last = f'{month}-30'

        roll_calls = (
            cls.select(
                cls.id,
                fn.json_build_object('id', Student.id, 'name', Student.name).alias('student'),
                cls.absent_type,
                cls.date
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                Student, JOIN.LEFT_OUTER, on=Student.id == cls.student
            ).join(
                Teacher, JOIN.LEFT_OUTER, on=Teacher.id == cls.teacher
            ).where(
                cls.active, Classroom.active, cls.classroom == class_room,
                cls.date <= last, cls.date >= first
            ).order_by(
                cls.id.desc()
            ).dicts()
        )

        if student:
            roll_calls = roll_calls.where(cls.student == student)

        return list(roll_calls)
