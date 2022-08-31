from models.member import Member

class Teacher(Member):

    class Meta:
        db_table = 'teacher'
