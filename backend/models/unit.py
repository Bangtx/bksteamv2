from models.base import BaseModel
from peewee import ForeignKeyField, CharField, fn
from models.classroom import Classroom


class Unit(BaseModel):
    classroom = ForeignKeyField(Classroom, column_name='classroom_id')
    title = CharField()

    class Meta:
        db_table = 'unit'

    @classmethod
    def get_units(cls, classroom_id: int):
        query = (
            cls.select(
                cls.id,
                cls.title,
                fn.json_build_object(
                    'id', Classroom.id,
                    'name', Classroom.name
                ).alias('classroom')
            ).join(
                Classroom, on=cls.classroom == Classroom.id
            ).where(
                cls.active, Classroom.active, cls.classroom == classroom_id
            ).order_by(cls.id.asc()).dicts()
        )

        return list(query)
