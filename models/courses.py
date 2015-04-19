from _base import *

class Student(db.Model, SessionMixin):
    __tablename__ = "students"
    stuid = db.Column(db.String(100), primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    major = db.Column(db.String(50))
    grade = db.Column(db.Integer)
    courses = relationship(
        'Course',
        secondary='xks'
    )

class Course(db.Model, SessionMixin):
    __tablename__ = "courses"
    code = db.Column(db.String(100), primary_key=True, nullable=False)
    teaid = db.Column(db.String(100), ForeignKey('teachers.teaid'), nullable=False)
    num = db.Column(db.Integer,nullable=False)
    desp = db.Column(db.String(200))
    major = db.Column(db.String(50))
    place = db.Column(db.String(200))
    time = db.Column(db.String(500))
    students = relationship(
        'Student',
        secondary='xks'
    )
    teacher=relationship('Teacher')

class Xk(db.Model, SessionMixin):
    __tablename__ = "xks"
    code = db.Column(db.String(100), ForeignKey('courses.code'), nullable=False, primary_key=True)
    stuid = db.Column(db.String(100), ForeignKey('students.stuid'), nullable=False, primary_key=True)

class Teacher(db.Model, SessionMixin):
    __tablename__ = "teachers"
    teaid = db.Column(db.String(100), primary_key=True, nullable=False)
    name = db.Column(db.String(50))
