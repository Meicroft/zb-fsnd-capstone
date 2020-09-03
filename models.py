import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Table
from flask_migrate import Migrate

# ---------
# Config.
# ---------

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "agency"
    database_path = "postgres://{}:{}@{}/{}".format(
        'postgres', 'root', 'localhost:5000', database_name)

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    print('dropped successfully')
    db.create_all()
    print('created successfully')

# ---------
# Models
# ---------

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'{self.title}, released {self.release_date}.'

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }

    def short(self):
        return{
            "title": self.title,
            "release_date": self.release_date,
            "actors": self.actors
        }


class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'{self.name}, {self.age} years old.'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    def short(self):
        return{
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }
