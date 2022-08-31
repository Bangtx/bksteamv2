from models.base import BaseModel
from models.classroom import Classroom
from models.unit import Unit
from peewee import CharField, BooleanField, ForeignKeyField, DateField, SQL
from playhouse.postgres_ext import ArrayField


class HomeWorkFile(BaseModel):
    date = DateField()
    deadline = DateField()
    classroom = ForeignKeyField(Classroom)
    unit = ForeignKeyField(Unit, null=True)
    description = CharField()
    file_url = CharField()
    is_global = BooleanField()
    student_ids = ArrayField()
    have_to_do = BooleanField()

    class Meta:
        db_table = 'home_work_file'

    @classmethod
    def get_list(cls, classroom=None, student=None, date_from=None, date_to=None):
        query = cls.select().where(
            cls.active, cls.classroom == classroom
        ).dicts().order_by(cls.id)
        if date_to:
            query = query.where(cls.date <= date_to)
        if date_from:
            query = query.where(cls.date >= date_from)
        if classroom:
            query = query.where(cls.classroom == classroom)
        if student:
            query = query.where(SQL(f"{student} = any(student_ids)"))

        return list(query)

