from _base import db,SessionMixin

class Course(db.Model, SessionMixin):
    __tablename__ = "courses"
    code = db.Column(db.String(100), primary_key=True, nullable=False)
    teaid = db.Column(db.String(100), nullable=False)
    num = db.Column(db.Integer,nullable=False)
    desp = db.Column(db.String(200))
    major = db.Column(db.String(50))
    place = db.Column(db.String(200))
    time = db.Column(db.String(200))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)