from models.base import BaseModel
from peewee import CharField, ForeignKeyField, fn, DateField, JOIN
from models.teacher import Teacher
from models.student import Student
from models.classroom import Classroom


class Notification(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    student = ForeignKeyField(Student, column_name='student_id')
    teacher = ForeignKeyField(Teacher, column_name='teacher_id')
    notification = CharField()
    date = DateField()
    type = CharField()

    class Meta:
        db_table = 'notification'

    @classmethod
    def get_notification(cls, class_room, student_id):
        query = cls.select(
            cls.id,
            cls.date,
            cls.notification,
            cls.type,
            fn.json_build_object(
                'id', Classroom.id,
                'name', Classroom.name
            ).alias('classroom'),
            fn.json_build_object('id', Student.id, 'name', Student.name).alias('student'),
            fn.json_build_object('id', Teacher.id, 'name', Teacher.name).alias('teacher'),
        ).join(
            Classroom, on=Classroom.id == cls.classroom
        ).join(
            Student, JOIN.LEFT_OUTER, on=Student.id == cls.student
        ).join(
            Teacher, JOIN.LEFT_OUTER, on=Teacher.id == cls.teacher
        ).where(cls.active)
        if class_room:
            query = query.where(cls.classroom == class_room)
        if student_id:
            query = query.where(cls.student == student_id)
        query = list(query.dicts())

        return query
