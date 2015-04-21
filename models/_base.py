from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class SessionMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)