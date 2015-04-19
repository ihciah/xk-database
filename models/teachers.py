from _base import db,SessionMixin

class Teacher(db.Model, SessionMixin):
    __tablename__ = "teachers"
    teaid = db.Column(db.String(100), primary_key=True, nullable=False)
    name = db.Column(db.String(50))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)