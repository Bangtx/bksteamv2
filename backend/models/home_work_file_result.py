from peewee import ForeignKeyField, CharField, JOIN, fn, FloatField
from models.base import BaseModel
from models.home_work_file import HomeWorkFile
from models.student import Student


class HomeWorkFileResult(BaseModel):
    home_work_file = ForeignKeyField(HomeWorkFile)
    student = ForeignKeyField(Student)
    file_result_url = CharField()
    score = FloatField()

    class Meta:
        db_table = 'home_work_file_result'

    @classmethod
    def get_list(cls, classroom, student = None, date_from=None, date_to=None):
        home_work_file = HomeWorkFile.select(
            HomeWorkFile
        ).where(
            HomeWorkFile.active, HomeWorkFile.classroom == classroom
        )
        if date_to:
            home_work_file = home_work_file.where(HomeWorkFile.date <= date_to)
        if date_from:
            home_work_file = home_work_file.where(HomeWorkFile.date >= date_from)

        home_work_file_ids = list(map(lambda x: x.id, list(home_work_file)))
        query = cls.select(
            cls
        ).where(
            cls.active, cls.home_work_file << home_work_file_ids
        ).dicts().order_by(cls.id)

        if student:
            query = query.where(cls.student == student)

        return list(query)

    @classmethod
    def create_new(cls, home_work_file_results):
        result = []
        for home_work_file_result in home_work_file_results:
            query_exists = cls.get_or_none(
                student=home_work_file_result['student'],
                home_work_file=home_work_file_result['home_work_file']
            )
            if query_exists:
                result.append(cls.update_one(query_exists.id, home_work_file_result))
            else:
                result.append(cls.create(**home_work_file_result))
        return result
