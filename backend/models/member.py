from models.base import BaseModel
from peewee import (
    CharField,
    IntegerField,
    DateField,
    SQL
)
from playhouse.postgres_ext import ArrayField


class Member(BaseModel):
    name = CharField()
    date_of_birth = DateField()
    gender = CharField()
    password = CharField()
    mail = CharField()
    phone = CharField()
    classrooms = ArrayField()

    @classmethod
    def query_get_list(cls, classroom=None):
        query = (
            cls.select(
                cls.id,
                cls.name,
                cls.gender,
                cls.date_of_birth,
                cls.mail,
                cls.phone,
                cls.classrooms
            ).where(cls.active).order_by(cls.id).dicts()
        )

        if classroom:
            query = query.where(SQL(f"{classroom} = any(classrooms)"))

        return query

    @classmethod
    def get_list(cls, classroom=None):
        return list(cls.query_get_list(classroom))

    @classmethod
    def get_classrooms(cls, id):
        from models.classroom import Classroom
        classrooms = cls.get_one(id)
        classrooms = classrooms['classrooms']
        # print(classrooms)
        result = []
        for classroom in classrooms:
            try:
                result.append(Classroom.get_one(classroom))
            except:
                pass

        return result


