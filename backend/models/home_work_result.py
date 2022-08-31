from peewee import BooleanField, ForeignKeyField, CharField, JOIN, fn
from models.base import BaseModel
from models.home_work import HomeWork
from models.student import Student
from utils.db import EXCLUDED, transaction


class HomeWorkResult(BaseModel):
    home_work = ForeignKeyField(HomeWork)
    student = ForeignKeyField(Student)
    answer = CharField()
    is_correct = BooleanField()

    class Meta:
        db_table = 'home_work_result'

    @classmethod
    def get_list(cls, classroom, student=None, date_from=None, date_to=None):
        home_work = HomeWork.select(HomeWork).where(HomeWork.active, HomeWork.classroom == classroom)
        if date_to:
            home_work = home_work.where(HomeWork.date <= date_to)
        if date_from:
            home_work = home_work.where(HomeWork.date >= date_from)

        home_work_ids = list(map(lambda x: x.id, list(home_work)))
        query = cls.select(
            cls
        ).where(
            cls.active, cls.home_work << home_work_ids
        ).dicts().order_by(cls.id)

        if student:
            query = query.where(cls.student == student)

        return list(query)

    @classmethod
    @transaction
    def create_new(cls, home_work_results):
        result = []
        for home_work_result in home_work_results:
            query_exists = cls.get_or_none(
                student=home_work_result['student'],
                home_work=home_work_result['home_work']
            )
            if query_exists:
                result.append(cls.update_one(query_exists.id, home_work_result))
            else:
                result.append(cls.create(**home_work_result))
        return result
