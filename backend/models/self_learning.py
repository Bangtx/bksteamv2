from models.base import BaseModel
from peewee import ForeignKeyField, fn, JOIN, DateField, IntegerField
from models.classroom import Classroom
from models.student import Student
from datetime import datetime
import calendar


class SelfLearning(BaseModel):
    date = DateField()
    classroom = ForeignKeyField(Classroom)
    absent_type = IntegerField()
    student = ForeignKeyField(Student)

    class Meta:
        db_table = 'self_learning'

    @classmethod
    def get_self_learning(cls, classroom: int, student=None):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        first, last = calendar.monthrange(currentYear, currentMonth)
        # get students id
        students = Student.get_list(classroom=classroom)
        student_ids = list(map(lambda x: x['id'], students))

        query = (
            cls.select(
                cls.id,
                cls.date,
                cls.absent_type,
                fn.json_build_object(
                    'id', Student.id,
                    'name', Student.name
                ).alias('student'),
                cls.date
            ).join(
                Student, JOIN.LEFT_OUTER, on=Student.id == cls.student
            ).where(
                cls.active,
                cls.student << student_ids,
                cls.date <= f'{currentYear}-{currentMonth}-{last}',
                cls.date >= f'{currentYear}-{currentMonth}-01'
            ).order_by(
                cls.date
            ).dicts()
        )

        if student:
            query = query.where(cls.student == student)

        return list(query)
