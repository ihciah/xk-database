from _base import db
from werkzeug import security

__all__ = ['Account']
class Account(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True,nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = self.create_password(raw)

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.username = username.lower()

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def is_admin(self):
        return self.role==2
    @property
    def is_stu(self):
        return self.role==1
    @property
    def is_teacher(self):
        return self.role==3

    @staticmethod
    def create_password(raw):
        passwd = '{old}{new}'.format(old=raw, new=db.app.config['PASSWORD_SECRET'])
        return security.generate_password_hash(passwd)

    def change_password(self, raw):
        self.passwd = self.create_password(raw)
        self.token = self.create_token()
        return self