from models.base import BaseModel
from playhouse.postgres_ext import JSONField, IntegerField
from models.classroom import Classroom
from models.unit import Unit
from models.audio import Audio
from peewee import CharField, DateField, ForeignKeyField, fn, JOIN, BooleanField


class HomeWork(BaseModel):
    date = DateField()
    deadline = DateField()
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    question = CharField()
    unit = ForeignKeyField(Unit, column_name='unit_id', null=True)
    audio = ForeignKeyField(Audio, column_name='audio')
    multi_choice = BooleanField()
    option_1 = CharField()
    option_2 = CharField()
    option_3 = CharField()
    option_4 = CharField()
    answer = CharField()
    have_to_do = BooleanField()

    class Meta:
        db_table = 'home_work'

    @classmethod
    def get_list(cls, classroom, date_from=None, date_to=None):
        query = cls.select(
            cls.id, cls.answer,
            cls.date, cls.classroom, cls.question, cls.multi_choice,
            Audio.url.alias('audio')
        ).join(
            Audio, JOIN.LEFT_OUTER, on=Audio.id == cls.audio
        ).where(cls.active, cls.classroom == classroom).dicts().order_by(cls.id)
        if date_to:
            query = query.where(cls.date <= date_to)
        if date_from:
            query = query.where(cls.date >= date_from)

        return list(query)


