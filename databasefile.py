import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate

login_manager = LoginManager()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://uraapmpmayzzcf:6e8a3f476df6b6f13bcddc982ec77b15e97366654ee2cc5a4ac6ba9575381999@ec2-54-164-22-242.compute-1.amazonaws.com:5432/d33eola97ups6j"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'


###############################

class Candidate(db.Model, UserMixin):
    __tablename__ = 'Candidate'

    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.Text)
    LastName = db.Column(db.Text)
    Email = db.Column(db.String)

    password = db.Column(db.String, unique=True)

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False

    def __init__(self, FirstName, Lastname, Email, password):
        self.FirstName = FirstName
        self.LastName = Lastname
        self.Email = Email
        self.password = password


class RealLogin(db.Model):
    __tablename__ = 'RealLogin'

    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, Username, password):
        self.Username = Username
        self.password = password


class Information(db.Model):
    __tablename__ = 'Information'

    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.Integer)
    Gender = db.Column(db.Text)

    def __init__(self, dob, Gender):
        self.dob = dob
        self.Gender = Gender


class Personality1(db.Model):
    __tablename__ = 'Personality1'

    id = db.Column(db.Integer, primary_key=True)
    Genre = db.Column(db.Text)
    Language1 = db.Column(db.Text)
    Language2 = db.Column(db.Text)

    def __init__(self, Genre, Language1, Language2):
        self.Genre = Genre
        self.Language1 = Language1
        self.Language2 = Language2


class Personality2(db.Model):
    __tablename__ = 'Personality2'

    id = db.Column(db.Integer, primary_key=True)
    Artist = db.Column(db.Text)
    Album = db.Column(db.Text)

    def __init__(self, Artist, Album):
        self.Artist = Artist
        self.Album = Album
