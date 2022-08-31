from models.base import BaseModel
from peewee import ForeignKeyField, fn, DateField, FloatField
from models.teacher import Teacher
from models.student import Student
from models.classroom import Classroom


class Score(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    date = DateField()
    student = ForeignKeyField(Student, column_name='student_id')
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    specking = FloatField()
    reading = FloatField()
    writing = FloatField()
    listening = FloatField()

    class Meta:
        db_table = 'score'

    @classmethod
    def get_class_room(cls, classroom):
        query = list(
            cls.select(
                fn.json_build_object(
                    'id', Classroom.id,
                    'name', Classroom.name
                ).alias('classroom'),
                cls.date,
                cls.listening,
                cls.reading,
                cls.specking,
                cls.writing,
                fn.json_build_object(
                    'id', Student.id,
                    'name', Student.name
                ).alias('student')
            ).join(
                Classroom, on=Classroom.id == cls.classroom
            ).join(
                Student, on=Student.id == cls.student
            ).where(
                cls.active, cls.classroom == classroom
            ).dicts()
        )
        dates = list(set(list(map(lambda x: str(x['date']), query))))
        datas = []
        for date in dates:
            data = list(filter(lambda x: str(x['date']) == date, query))
            datas.append({
                'date': date,
                'data': data
            })
        return datas

    @classmethod
    def get_score_by_date(cls, date, student_id, class_room_id=None):
        scores = (
            cls.select().where(
                cls.active, cls.date == date, cls.student == student_id
            )
        )
        if class_room_id:
            scores = scores.where(cls.classroom == class_room_id)
        # scores = scores.dicts().get()
        if list(scores):
            scores = scores.dicts().get()
            return scores
        return None