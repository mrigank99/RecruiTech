import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
#from DateTime import DateTime

login_manager = LoginManager()
basedir= os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] ="postgres://xlizrefejlapdm:f343152400800416d035bf3cf753867b0c6a8298ee73bcb222a31fa13480a4c3@ec2-3-251-0-202.eu-west-1.compute.amazonaws.com:5432/d9mcnufo140qlb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
login_manager.init_app(app)
login_manager.login_view = 'login'

###########################

class Candidate(db.Model, UserMixin):
    __tablename__ = 'Candidates'

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    candidate_email = db.Column(db.String, unique=True)
    candidate_password = db.Column(db.String, unique=True)
    apptitude_score = db.Column(db.Integer)

    candidateDetails = db.relationship('candidateDetails', cascade="all,delete", backref='cDetails', lazy='dynamic')
    candidateExperience = db.relationship('candidateExperience',cascade="all,delete", backref='cDetails', lazy='dynamic')
    candidateEducation = db.relationship('candidateEducation',cascade="all,delete", backref='cDetails', lazy='dynamic')
    candidateProject = db.relationship('candidateProject',cascade="all,delete", backref='cDetails', lazy='dynamic')
    candidateCertificate = db.relationship('candidateCertificate',cascade="all,delete", backref='cDetails', lazy='dynamic')
    candidateSkills = db.relationship('candidateSkills',cascade="all,delete", backref='cDetails', lazy='dynamic')
    candidateSocial = db.relationship('candidateSocial',cascade="all,delete", backref='cDetails', lazy='dynamic')
    jobsApplied = db.relationship('jobsApplied',cascade="all,delete", backref='candidateDetails', lazy='dynamic')

    def __init__(self, first_name, last_name, candidate_email, candidate_password):
        self.first_name = first_name
        self.last_name = last_name
        self.candidate_email = candidate_email
        self.candidate_password = candidate_password

    def check_password(self, password):
        if self.candidate_password == password:
            return True
        else:
            return False

    def modifyScore(self, score):
        self.apptitude_score = score
        return True

    def get_id(self):
        return self.candidate_email


class Recruiter(db.Model, UserMixin):
    __tablename__ = 'Recruiter'

    rid = db.Column(db.Integer, primary_key = True)
    recruiter_name = db.Column(db.Text)
    recruiter_email = db.Column(db.String, unique=True)
    com_name = db.Column(db.String)
    com_number = db.Column(db.Integer)
    recruiter_designation = db.Column(db.Text)
    recruiter_password = db.Column(db.String, unique=True)

    jobsApplied = db.relationship('jobsApplied', cascade="all,delete", backref='recruiterDetails', lazy='dynamic')
    Jobs = db.relationship('Jobs', cascade="all,delete", backref='jobs', lazy='dynamic')

    def __init__(self, recruiter_name, recruiter_email, com_name, com_number, recruiter_designation, recruiter_password):
        self.recruiter_name = recruiter_name
        self.recruiter_email = recruiter_email
        self.com_name = com_name
        self.com_number = com_number
        self.recruiter_designation = recruiter_designation
        self.recruiter_password = recruiter_password

    def check_password(self, password):
        if self.recruiter_password == password:
            return True
        else:
            return False

    def get_id(self):
        return self.recruiter_email

class candidateDetails(db.Model):
    __tablename__ = 'candidateDetails'

    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.Text)
    last_name=db.Column(db.Text)
    EMAIL=db.Column(db.String)
    age = db.Column(db.Integer)
    contact = db.Column(db.Integer)
    address = db.Column(db.String)
    about_me = db.Column(db.String)
    preference = db.Column(db.String)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))


    def __init__(self, first_name, last_name, EMAIL, age, number, address, about_me, preference, cid):
        self.first_name = first_name
        self.last_name = last_name
        self.EMAIL = EMAIL
        self.age = age
        self.number = number
        self.address = address
        self.about_me = about_me
        self.preference = preference
        self.cid = cid

class candidateExperience(db.Model):
    __tablename__ = 'candidateExperience'

    experience_id = db.Column(db.Integer,primary_key=True)
    com_name = db.Column(db.Text)
    com_from_date = db.Column(db.Text)
    com_to_date = db.Column(db.Text)
    designation=db.Column(db.Text)
    department = db.Column(db.Text)
    about_role = db.Column(db.String)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))

    def __init__(self,com_name,com_from_date,com_to_date,designation,department, about_role, cid):
        self.com_name = com_name
        self.com_from_date = com_from_date
        self.com_to_date = com_to_date
        self.designation = designation
        self.department = department
        self.about_role = about_role
        self.cid = cid

class candidateEducation(db.Model):
    __tablename__ = 'candidateEducation'

    education_id = db.Column(db.Integer, primary_key=True)
    degree_level = db.Column(db.Text)
    university = db.Column(db.Text)
    uni_subject = db.Column(db.Text)
    cgpa = db.Column(db.Text)
    uni_passing = db.Column(db.Text)
    school = db.Column(db.Text)
    school_subject = db.Column(db.Text)
    twelth_marks = db.Column(db.String)
    school_passing = db.Column(db.Text)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))

    def __init__(self,degree_level,university,uni_subject,cgpa,uni_passing,
                 school, school_subject, twelth_marks, school_passing, cid):
        self.degree_level = degree_level
        self.university = university
        self.uni_subject = uni_subject
        self.cgpa = cgpa
        self.uni_passing = uni_passing
        self.school = school
        self.school_subject = school_subject
        self.twelth_marks = twelth_marks
        self.school_passing = school_passing
        self.cid = cid

class candidateProject(db.Model):
    __tablename__ = 'candidateProject'

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
    field = db.Column(db.Text)
    from_date_project = db.Column(db.Text)
    to_date_project = db.Column(db.Text)
    project_details = db.Column(db.String)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))

    def __init__(self,project_name,field,from_date_project,to_date_project, project_details,cid):
        self.project_name = project_name
        self.field = field
        self.from_date_project = from_date_project
        self.to_date_project = to_date_project
        self.project_details = project_details
        self.cid = cid

class candidateCertificate(db.Model):
    __tablename__ = 'candidateCertificate'

    certificate_id = db.Column(db.Integer, primary_key=True)
    certificate = db.Column(db.Text)
    issue = db.Column(db.Text)
    serial = db.Column(db.Integer)
    certificate_date = db.Column(db.Text)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))

    def __init__(self,certificate,issue,serial,certificate_date,cid):
        self.certificate = certificate
        self.issue = issue
        self.serial = serial
        self.certificate_date = certificate_date
        self.cid = cid

class candidateSkills(db.Model):
    __tablename__ = 'candidateSkills'

    skills_id = db.Column(db.Integer, primary_key=True)
    technical = db.Column(db.Text)
    interpersonal = db.Column(db.Text)
    interest = db.Column(db.Text)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))

    def __init__(self,technical,interpersonal,interest, cid):
        self.technical = technical
        self.interpersonal = interpersonal
        self.interest = interest
        self.cid = cid

class candidateSocial(db.Model):
    __tablename__ = 'candidateSocial'

    social_id = db.Column(db.Integer, primary_key=True)
    linkedin = db.Column(db.String)
    facebook = db.Column(db.String)
    twitter = db.Column(db.String)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))

    def __init__(self, linkedin, facebook, twitter, cid):
        self.linkedin = linkedin
        self.facebook = facebook
        self.twitter = twitter
        self.cid = cid

class Jobs(db.Model):
    __tablename__ = "Jobs"
    id = db.Column(db.Integer, primary_key=True)
    jobName = db.Column(db.Text)
    department = db.Column(db.Text)
    location = db.Column(db.Text)
    jobtype = db.Column(db.Text)
    minsalary = db.Column(db.Integer)
    maxsalary = db.Column(db.Integer)
    openings = db.Column(db.Integer)
    about = db.Column(db.Text)
    skills = db.Column(db.Text)
    qualifications = db.Column(db.Text)
    jobdescription = db.Column(db.Text)
    experience = db.Column(db.Integer)
    perks = db.Column(db.Text)
    requirements = db.Column(db.Text)
    postingdate = db.Column(db.Text)

    rid = db.Column(db.Integer, db.ForeignKey('Recruiter.rid'))

    jobsApplied = db.relationship('jobsApplied', cascade="all,delete", backref='jobDetails', lazy='dynamic')

    def __init__(self,jobName,department,location,jobtype, minsalary, maxsalary,openings,
                 about,skills,qualifications, jobdescription,experience,perks,requirements, postingdate, rid):
        self.jobName = jobName
        self.department = department
        self.location = location
        self.jobtype = jobtype
        self.minsalary = minsalary
        self.maxsalary = maxsalary
        self.openings = openings
        self.about = about
        self.skills = skills
        self.qualifications = qualifications
        self.jobdescription = jobdescription
        self.experience = experience
        self.perks = perks
        self.requirements = requirements
        self.postingdate = postingdate
        self.rid = rid

class jobsApplied(db.Model):
    __tablename__ = "jobsApplied"
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('Candidates.id'))
    rid = db.Column(db.Integer, db.ForeignKey('Recruiter.rid'))
    job_id = db.Column(db.Integer, db.ForeignKey('Jobs.id'))

    def __init__(self,cid,rid,job_id):
        self.cid = cid
        self.rid = rid
        self.job_id = job_id