import os
from flask import Flask, render_template, request, redirect, url_for, flash
from databasefile import *
from flask_login import login_user, login_required, logout_user
from flask_login import LoginManager, UserMixin
from flask_login import current_user
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename


from flask_login import current_user
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.secret_key = "testing101"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://uraapmpmayzzcf:6e8a3f476df6b6f13bcddc982ec77b15e97366654ee2cc5a4ac6ba9575381999@ec2-54-164-22-242.compute-1.amazonaws.com:5432/d33eola97ups6j"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('Login.html')


@app.route('/Information')
def Information():
    return render_template('Information.html')


@app.route("/Info_details", methods=['POST','GET'])
def Info_details():
    # nickname = request.form.get('nickname')
    DOB = request.form.get('DOB')
    Gender = request.form.get('Gender')

    Infod = Information(dob=DOB, Gender=Gender)
    db.session.add(Infod)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/PersonalityTest1')
def PersonalityTest1():
    return render_template('Personality_test1.html')




@app.route('/PersonalityTest2', methods = ['POST','GET'])
def PersonalityTest2():
    Genre = request.form.get('Genre')
    Language1 = request.form.get('Language1')
    Language2 = request.form.get('Language2')

    Personality1d = Personality1(Genre=Genre, Language1=Language1, Language2=Language2)
    db.session.add(Personality1d)
    db.session.commit()
    return render_template('Personality_test2.html')



@app.route('/Signup')
def Signup():
    return render_template('Signup.html')


@app.route("/Signup_details", methods=['POST'])
def Signup_details():
    FirstName = request.form.get('FirstName')
    LastName = request.form.get('LastName')
    Email = request.form.get('Email')
    password = request.form.get('password')

    Signupd = Candidate(FirstName=FirstName, LastName=LastName, Email=Email, password=password)
    db.session.add(Signupd)
    db.session.commit()
    return render_template('Personality_test1.html')


@app.route('/RealLogin')
def RealLogin():
    return render_template('beforelogin.html')


if __name__ == '__main__':
    app.run(debug=True)
