from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery

db = SQLAlchemy()

class SessionMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self