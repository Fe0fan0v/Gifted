import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from werkzeug.security import generate_password_hash, check_password_hash
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<User> {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_all_values(self):
        return {"id": self.id, 'name': self.name, 'surname': self.surname, 'email': self.email,
                'my_problems': self.my_problems, 'ver_problems': self.ver_problems,
                'my_thanks': self.my_thanks, 'ver_thanks': self.ver_thanks, 'hashed_password': self.hashed_password,
                'modified_date': self.modifed_date}


class Contest(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'participant'
    teacher = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    level = sqlalchemy.Column(sqlalchemy.String)
    nomination = sqlalchemy.Column(sqlalchemy.String)
    distant = sqlalchemy.Column(sqlalchemy.Boolean)
    union = sqlalchemy.Column(sqlalchemy.String)
    collective = sqlalchemy.Column(sqlalchemy.Boolean)
    place = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DATE)
    participants = sqlalchemy.Column(sqlalchemy.JSON)
