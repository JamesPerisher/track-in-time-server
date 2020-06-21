from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    name_first = db.Column(db.String(25))
    name_last  = db.Column(db.String(25))
    dob        = db.Column(db.DateTime, default=datetime.now)
    house      = db.Column(db.String(25))
    gender     = db.Column(db.String(25))


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)

    name      = db.Column(db.String(50))
    date_from = db.Column(db.DateTime, default=datetime.now)
    date_to   = db.Column(db.DateTime, default=datetime.now)
    gender    = db.Column(db.String(25))
    method    = db.Column(db.String(25))


class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)

    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id  = db.Column(db.Integer, db.ForeignKey('events.id'))
    score_time= db.Column(db.DateTime, default=datetime.now)
    score_int = db.Column(db.Integer)

class House(db.Model):
    __tablename__ = 'houses'
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(25))

class Gender(db.Model):
    __tablename__ = 'genders'
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(25))
