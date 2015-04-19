from _base import db,SessionMixin

class Student(db.Model, SessionMixin):
    __tablename__ = "students"
    stuid = db.Column(db.String(100), primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    major = db.Column(db.String(50))
    grade = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)