from models.member import Member
from peewee import IntegerField


class Student(Member):
    status = IntegerField()

    LEARN = 1
    QUIT = 2
    TEMP_STOP = 3
    COMPLETE = 4
    CHANGE = 5

    class Meta:
        db_table = 'student'

    @classmethod
    def get_list(cls, classroom=None):
        query = cls.query_get_list(classroom)
        query = query.select(cls)
        return list(query)
