import os
from flask import Flask, render_template, request, redirect, url_for, flash
from basic import *
from flask_login import login_user, login_required, logout_user
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from flask_login import current_user
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from random import *
from flask import session
from recommendJobs import *

abc = Bcrypt()

app = Flask(__name__)
basedir= os.path.abspath(os.path.dirname(__file__))

app.secret_key = "testing101"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] ="postgres://xlizrefejlapdm:f343152400800416d035bf3cf753867b0c6a8298ee73bcb222a31fa13480a4c3@ec2-3-251-0-202.eu-west-1.compute.amazonaws.com:5432/d9mcnufo140qlb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'techproject2022@gmail.com'
app.config['MAIL_PASSWORD'] = 'mrisakhu@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db.init_app(app)
mail = Mail(app)
otp = randint(000000,999999)

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)

login_manager.login_view = 'login' # Sets the place where users will be redirected for @login_required pages

@login_manager.user_loader
def load_user(user_id):
    recruiter = Recruiter.query.filter_by(recruiter_email=user_id).first()
    if recruiter is None:
        return Candidate.query.filter_by(candidate_email=user_id).first()
    else:
        return recruiter

#@login_manager.user_loader
#def load_recruiter(user_id):
#    return Recruiter.query.get(user_id)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup_recruiter')
def signup_recruiter():
    return render_template("signup_recruiter.html")

@app.route('/signup_candidate')
def signup_candidate():
    return render_template("signup_candidate.html")


@app.route('/recruiter_sign', methods = ['POST'])
def recruiter_sign():
    recruiter_name = request.form.get('recruiter_name')
    recruiter_email = request.form.get('recruiter_email')
    com_name = request.form.get('com_name')
    com_number = request.form.get('com_number')
    recruiter_designation = request.form.get('recruiter_designation')
    recruiter_password = request.form.get('recruiter_password')
    #hashed_rpassword = abc.generate_password_hash(password=recruiter_password)

    recruiterSign = Recruiter(recruiter_name=recruiter_name, recruiter_email=recruiter_email, com_name=com_name,
                              com_number=com_number, recruiter_designation=recruiter_designation,
                              recruiter_password=recruiter_password)
    db.session.add(recruiterSign)
    db.session.commit()
    return redirect(url_for('login_recruiter'))

@app.route('/candidate_sign', methods = ['POST'])
def candidate_sign():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    candidate_email = request.form.get('candidate_email')
    candidate_password = request.form.get('candidate_password')
    #hashed_cpassword = abc.generate_password_hash(password=candidate_password)
    session['first_name']=first_name
    session['last_name']=last_name
    session['candidate_email']=candidate_email
    session['password']=candidate_password

    msg = Message('OTP', sender='techproject2022@gmail.com', recipients=[candidate_email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('validate.html')

@app.route('/validate', methods=["POST"])
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        candidateSign = Candidate(first_name=session['first_name'], last_name=session['last_name'], candidate_email=session['candidate_email'],
                                  candidate_password=session['password'])
        db.session.add(candidateSign)
        db.session.commit()
        return render_template('login_candidate.html')

    return "<h3>Could not verify!</h3>"

@app.route('/userlogin')
def userlogin():
    return render_template("login.html")

@app.route('/login_candidate')
def login_candidate():
    return render_template("login_candidate.html")

@app.route('/login_recruiter')
def login_recruiter():
    return render_template("login_recruiter.html")

@app.route('/login', methods = ['POST','GET']) ############## --------------------------->
def login():
    username = request.form.get('candidate_email')
    password = request.form.get('candidate_password')

    current_candidate = Candidate.query.filter_by(candidate_email=username).first()

    if  current_candidate is None or current_candidate.check_password(password) is False:
        flash('Username/Password does not match')
        return redirect(url_for('login_candidate'))

    else:
        login_user(current_candidate)

        next = request.args.get('next')
        if next == None  or not next[0] == '/':
            next = url_for('candidate_dashboard')

        return redirect(next)


@app.route('/login_recruiter', methods = ['POST','GET'])
def recruiter_login(): #Function that processes recruiter login
    username = request.form.get('recruiter_email')
    password = request.form.get('recruiter_password')

    current_recruiter = Recruiter.query.filter_by(recruiter_email= username).first()

    if current_recruiter.check_password(password) is False or current_recruiter is None:
        flash('Username/Password does not match')
        return redirect(url_for('login_recruiter'))
    else:
        login_user(current_recruiter)

        next = request.args.get('next')
        if next == None or not next[0] == '/':
            next = url_for('recruiter_dashboard')

        return redirect(next)

@app.route('/logout') # --------------------------->
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/candidate_dashboard')
@login_required
def candidate_dashboard():
    filename = str(current_user.id)
    filename = 'uploads/'+filename
    total_applications = jobsApplied.query.filter_by(cid=current_user.id).count()
    return render_template("candidate_dashboard.html", filename=filename, total_applications=total_applications)

@app.route('/candidate_applications')
@login_required
def candidate_applications():
    details = db.session.query(jobsApplied.id, Jobs.jobName, Jobs.department, Jobs.jobtype,
                               Recruiter.com_name,jobsApplied.job_id).filter(jobsApplied.cid == current_user.id) \
        .outerjoin(Jobs, Jobs.id == jobsApplied.job_id) \
        .outerjoin(Recruiter, Recruiter.rid == jobsApplied.rid).all()
    print(details)
    return render_template("candidate_applications.html", details=details)

@app.route('/candidate_job_search')
@login_required
def candidate_job_search():
    listed_jobs = Jobs.query.all() #Contains list of Objects of job Table
    userid = current_user.id
    get_job_recommendations(current_user.id)
    temp = jobsApplied.query.with_entities(jobsApplied.job_id).filter_by(cid=userid).all()
    print(temp[0])
    currentuser_applied_jobs = [item[0] for item in temp]
    print(currentuser_applied_jobs)
    companies = []
    for item in range(len(listed_jobs)):
        current_company = Recruiter.query.with_entities(Recruiter.com_name).filter_by(rid=listed_jobs[item].rid).all()
        companies.append(current_company)

    return render_template("candidate_job_search.html", jobDetails=listed_jobs, companies=companies,appliedJobs=currentuser_applied_jobs, jobCategory=None)


@app.route('/filtering', methods=['POST'])
def filtering():
    jobCategory = request.form.get('jobCategory')
    jobLocation = request.form.get('jobLocation')
    jobType = request.form.get('jobType')
    #jobSalary = request.form.get('jobSalary')

    criteria = {}
    if jobCategory != "None":
        criteria['jobName'] = jobCategory
    if jobLocation != "None":
        criteria['location'] = jobLocation
    if jobType != "None":
        criteria['jobtype'] = jobType
    #if jobSalary != "None":
    #    criteria['minsalary'] = jobSalary

    print(jobCategory)
    print(jobLocation)
    #print(jobSalary)
    print(jobType)

    listed_jobs = Jobs.query.filter_by(**criteria).all()

    userid = current_user.id
    temp = jobsApplied.query.with_entities(jobsApplied.job_id).filter_by(cid=userid).all()
    currentuser_applied_jobs = [item[0] for item in temp]
    print("Applied Jobs = ",currentuser_applied_jobs)
    companies = []
    for item in range(len(listed_jobs)):
        current_company = Recruiter.query.with_entities(Recruiter.com_name).filter_by(rid=listed_jobs[item].rid).all()
        companies.append(current_company)


    return render_template("candidate_job_search.html", jobDetails=None, companies=companies,
                           appliedJobs=currentuser_applied_jobs, jobCategory=listed_jobs)


@app.route('/candidate_profile')
@login_required
def candidate_profile():
    userid = current_user.id
    userDetails = candidateDetails.query.filter_by(cid=userid).first()
    userExperience = candidateExperience.query.filter_by(cid=userid).first()
    userEducation = candidateEducation.query.filter_by(cid=userid).first()
    userProject = candidateProject.query.filter_by(cid=userid).first()
    userCertificate = candidateCertificate.query.filter_by(cid=userid).first()
    userSkills = candidateSkills.query.filter_by(cid=userid).first()
    userSocial = candidateSocial.query.filter_by(cid=userid).first()
    return render_template("candidate_profile.html", userDetails=userDetails, userExperience=userExperience,
                           userEducation=userEducation, userProject=userProject, userCertificate=userCertificate,
                           userSkills=userSkills, userSocial=userSocial)

@app.route('/apptitude')
@login_required
def apptitude():
    return render_template("apptitude.html")

@app.route('/basic_test')
@login_required
def basic_test():
    return render_template("basic_test.html")

@app.route('/update_score', methods=['POST','GET'])
@login_required
def update_score():
    score = request.get_json()

    user = db.session.query(Candidate).filter_by(id=current_user.id).first() # Here we dont use the Tablename.query method as this methods returns
    user.modifyScore(score)                                                  # a copy of the object while we need to modify the original.
    db.session.commit()
    return render_template("apptitude.html")


@app.route('/infographic_cv/<int:id>')
@login_required
def infographic_cv(id):
    userid = id
    userDetails = candidateDetails.query.filter_by(cid=userid).first()
    userExperience = candidateExperience.query.filter_by(cid=userid).first()
    userEducation = candidateEducation.query.filter_by(cid=userid).first()
    userProject = candidateProject.query.filter_by(cid=userid).first()
    userCertificate = candidateCertificate.query.filter_by(cid=userid).first()
    userSkills = candidateSkills.query.filter_by(cid=userid).first()
    userSocial = candidateSocial.query.filter_by(cid=userid).first()

    filename = str(userid)
    filename = 'uploads/' + filename
    return render_template("infographic_cv.html", userDetails = userDetails, userExperience=userExperience,
                           userEducation= userEducation, userProject = userProject, userCertificate = userCertificate,
                           userSkills = userSkills, userSocial = userSocial, filename=filename)

@app.route('/candidate_about_us')
@login_required
def candidate_about_us():
    return render_template("candidate_about_us.html")

@app.route('/candidate_contact')
@login_required
def candidate_contact():
    return render_template("candidate_contact.html")

@app.route('/candidate_support',methods=['GET', 'POST'])
def candidate_support():
    subject = request.form.get('subject')
    message = request.form.get('message')

    print(subject)
    print(message)

    fname = current_user.first_name
    lname = current_user.last_name
    email = current_user.candidate_email

    msg = Message(subject, sender='techproject2022@gmail.com', recipients=['syal.sanskar10@gmail.com'])
    msg.body = "You have received a new query from {} {} <{}>. The query is: {}".format(fname,lname, email, message)
    mail.send(msg)
    return render_template("candidate_dashboard.html")

@app.route('/candidate_job_post/<int:jobid>', methods = ['POST','GET'])
@login_required
def candidate_job_post(jobid):
    uid = jobid
    jdetails = Jobs.query.filter_by(id=uid).first()
    return render_template("candidate_job_post.html",jobid=jobid, jdetails = jdetails)

@app.route('/job_apply/<jobid>', methods = ['POST','GET'])
@login_required
def job_apply(jobid):
    cid = current_user.id
    current_job = Jobs.query.filter_by(id=jobid).first()
    rid = current_job.rid
    application_details = jobsApplied(cid=cid,rid=rid,job_id=jobid)

    db.session.add(application_details)
    db.session.commit()

    return redirect(url_for('candidate_dashboard'))


@app.route('/recruiter_about_us')
def recruiter_about_us():
    return render_template("recruiter_about_us.html")

@app.route('/recruiter_applications')
def recruiter_applications():
    listed_jobs = Jobs.query.filter_by(rid=current_user.rid).all()
    return render_template("recruiter_applications.html", jobPost=listed_jobs)

@app.route('/recruiter_company_profile')
def recruiter_company_profile():
    return render_template("recruiter_company_profile.html")

@app.route('/recruiter_contact')
def recruiter_contact():
    return render_template("recruiter_contact.html")

@app.route('/recruiter_dashboard')
@login_required
def recruiter_dashboard():
    return render_template("recruiter_dashboard.html")

@app.route('/recruiter_post_opening')
def recruiter_post_opening():
    return render_template("recruiter_post_opening.html")

@app.route('/addJobOpening', methods = ['POST'])
def addJobOpening():
    #Getting details from the form
    job_name = request.form.get('job_title')
    department = request.form.get('job_department')
    location = request.form.get('job_location')
    jobtype = request.form.get('job_type')
    minsalary = request.form.get('min_salary')
    maxsalary = request.form.get('max_salary')
    openingscount = request.form.get('position_number')
    about = request.form.get('about_company')
    skills = request.form.get('req_skills')
    qualifications = request.form.get('req_qualification')
    jobdesc = request.form.get('job_description')
    experience = request.form.get('req_exp')
    perks = request.form.get('perks')
    requirements = request.form.get('other_req')
    postingdate = request.form.get('close_date')

    rid = current_user.rid

    jobDetails = Jobs(jobName=job_name, department=department, location=location, jobtype=jobtype,minsalary=minsalary, maxsalary=maxsalary,
                      openings=openingscount, about=about, skills=skills, qualifications=qualifications, jobdescription=jobdesc,
                      experience=experience,perks=perks,postingdate=postingdate,requirements=requirements, rid=rid)
    db.session.add(jobDetails)
    db.session.commit()

    return redirect(url_for('recruiter_dashboard'))

@app.route('/recruiter_single_application/<int:jobid>')
def recruiter_single_application(jobid):
    details = db.session.query(jobsApplied.job_id, candidateDetails.first_name, candidateDetails.last_name, candidateDetails.EMAIL,
                               candidateDetails.contact,candidateEducation.degree_level,candidateEducation.cid).filter(jobsApplied.job_id==jobid)\
        .outerjoin(candidateDetails, candidateDetails.cid ==jobsApplied.cid)\
        .outerjoin(candidateEducation, candidateEducation.cid==jobsApplied.cid).all()
    jobName = db.session.query(Jobs.jobName).filter(Jobs.id==jobid).first()

    return render_template("recruiter_single_application.html", details=details, jobName=jobName[0])

@app.route('/filtering_candidate/<int:c_id>/<int:jobid>', methods=['POST'])
def filtering_candidate(c_id, jobid):
    cLocation = request.form.get('cLocation')
    cEducation = request.form.get('cEducation')
    cSkill = request.form.get('cSkill')

    criteria = {}
    if cLocation != "None":
        criteria['address'] = cLocation
    if cEducation != "None":
        criteria['degree_level'] = cEducation
    if cSkill != "None":
        criteria['technical'] = cSkill

    print(cLocation)
    print(cEducation)
    print(cSkill)

    listed_candidates = db.session.query(candidateDetails.id, candidateDetails.address, candidateEducation.degree_level,
                                   candidateSkills.technical).filter(Candidate.id==c_id)\
        .outerjoin(candidateDetails, candidateDetails.cid==Candidate.id)\
        .outerjoin(candidateEducation, candidateEducation.cid==Candidate.id)\
        .outerjoin(candidateSkills, candidateSkills.cid==Candidate.id).filter_by(**criteria).all()

    details = db.session.query(jobsApplied.job_id, candidateDetails.first_name, candidateDetails.last_name, candidateDetails.EMAIL,
                               candidateDetails.contact, candidateEducation.degree_level,
                               candidateEducation.cid).filter(jobsApplied.job_id == jobid) \
        .outerjoin(candidateDetails, candidateDetails.cid == jobsApplied.cid) \
        .outerjoin(candidateEducation, candidateEducation.cid == jobsApplied.cid).all()
    jobName = db.session.query(Jobs.jobName).filter(Jobs.id == jobid).first()

    return render_template("recruiter_single_application.html", details=details, jobName=jobName[0], listed_candidates=listed_candidates)

@app.route('/recruiter_delete_application/<int:jobid>')
def recruiter_delete_application(jobid):
    db.session.query(Jobs).filter_by(id=jobid).delete()
    db.session.commit()

    return redirect(url_for('recruiter_applications'))

@app.route('/add_candidate_details', methods = ['POST'])
def add_candidate_details():
    #Getting details from the form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    EMAIL = request.form.get('EMAIL')
    age = request.form.get('age')
    contact = request.form.get('contact')
    address = request.form.get('address')
    about_me = request.form.get('about_me')
    preference = request.form.get('preference')
    cid = current_user.id

    candDetails = candidateDetails(first_name=first_name, last_name=last_name, EMAIL=EMAIL, age=age, contact=contact,
                        address=address, about_me = about_me, preference=preference, cid=cid)
    db.session.add(candDetails)
    db.session.commit()
    return redirect(url_for('candidate_profile'))

@app.route('/add_candidate_experience', methods = ['POST'])
def add_candidate_experience():
    com_name = request.form.get('com_name')
    com_from_date = request.form.get('com_from_date')
    com_to_date = request.form.get('com_to_date')
    designation = request.form.get('designation')
    department = request.form.get('department')
    about_role = request.form.get('about_role')
    cid = current_user.id

    candExperience = candidateExperience(com_name=com_name, com_from_date=com_from_date,com_to_date=com_to_date,
                           designation=designation,department=department, about_role=about_role, cid=cid)
    db.session.add(candExperience)
    db.session.commit()
    return redirect(url_for('candidate_profile'))

@app.route('/add_candidate_education', methods=['POST'])
def add_candidate_education():
    degree_level = request.form.get('degree_level')
    university = request.form.get('university')
    uni_subject = request.form.get('uni_subject')
    cgpa = request.form.get('cgpa')
    uni_passing = request.form.get('uni_passing')
    school = request.form.get('school')
    school_subject = request.form.get('school_subject')
    twelth_marks = request.form.get('twelth_marks')
    school_passing = request.form.get('school_passing')
    cid = current_user.id

    candEducation = candidateEducation(degree_level=degree_level, university=university,uni_subject=uni_subject,cgpa=cgpa, uni_passing=uni_passing,
                      school=school, school_subject=school_subject, twelth_marks=twelth_marks, school_passing=school_passing, cid=cid)
    db.session.add(candEducation)
    db.session.commit()
    return redirect(url_for('candidate_profile'))

@app.route('/add_candidate_project', methods=['POST'])
def add_candidate_project():
    project_name = request.form.get('project_name')
    field = request.form.get('field')
    from_date_project = request.form.get('from_date_project')
    to_date_project = request.form.get('to_date_project')
    project_details = request.form.get('project_details')
    cid = current_user.id

    candProject = candidateProject(project_name=project_name,field=field,from_date_project=from_date_project,
                          to_date_project=to_date_project, project_details=project_details, cid=cid)
    db.session.add(candProject)
    db.session.commit()
    return redirect(url_for('candidate_profile'))

@app.route('/add_candidate_certificate', methods=['POST'])
def add_candidate_certificate():
    certificate = request.form.get('certificate')
    issue = request.form.get('issue')
    serial = request.form.get('serial')
    certificate_date = request.form.get('certificate_date')
    cid = current_user.id

    candCertificate = candidateCertificate(certificate=certificate,issue=issue,serial=serial,certificate_date=certificate_date, cid=cid)
    db.session.add(candCertificate)
    db.session.commit()
    return redirect(url_for('candidate_profile'))

@app.route('/add_candidate_skills', methods=['POST'])
def add_candidate_skills():
    technical = request.form.get('technical')
    interpersonal = request.form.get('interpersonal')
    interest = request.form.get('interest')
    cid = current_user.id

    candSkills = candidateSkills(technical=technical, interpersonal=interpersonal,interest=interest, cid=cid)
    db.session.add(candSkills)
    db.session.commit()
    return redirect(url_for('candidate_profile'))

@app.route('/add_social_details', methods=['POST'])
def add_social_details():
    linkedin = request.form.get('linkedin')
    facebook = request.form.get('facebook')
    twitter = request.form.get('twitter')
    cid = current_user.id

    candSocial = candidateSocial(linkedin=linkedin, facebook=facebook, twitter =twitter , cid=cid)
    db.session.add(candSocial)
    db.session.commit()
    return redirect(url_for('candidate_profile'))

@app.route('/update/<int:id>', methods = ['POST','GET'])
def update(id):

    new = db.session.query(candidateDetails).filter_by(cid = id).first()
    if request.method == "POST":
        print("If condition runs")
        new.first_name=request.form['first_name']
        new.last_name = request.form['last_name']
        new.EMAIL = request.form['EMAIL']
        new.age = request.form['age']
        new.contact = request.form['contact']
        new.address = request.form['address']
        new.about_me = request.form['about_me']
        new.preference = request.form['preference']

        try:
            db.session.commit()
            return redirect(url_for('candidate_profile'))
        except:
            return "erororoorroor"

    print(new)
    return render_template('update.html',new=new)

@app.route('/updateExperience/<int:id>', methods = ['POST','GET'])
def updateExperience(id):

    new = db.session.query(candidateExperience).filter_by(cid = id).first()
    if request.method == "POST":
        print("If condition runs")
        new.com_name=request.form['com_name']
        new.com_from_date = request.form['com_from_date']
        new.com_to_date = request.form['com_to_date']
        new.designation = request.form['designation']
        new.department = request.form['department']
        new.about_role = request.form['about_role']
        try:
            db.session.commit()
            return redirect(url_for('candidate_profile'))
        except:
            return "erororoorroor"

    print(new)
    return render_template('updateExperience.html',new=new)

@app.route('/updateEducation/<int:id>', methods = ['POST','GET'])
def updateEducation(id):

    new = db.session.query(candidateEducation).filter_by(cid = id).first()
    if request.method == "POST":
        print("If condition runs")
        new.degree_level = request.form['degree_level']
        new.university = request.form['university']
        new.uni_subject = request.form['uni_subject']
        new.cgpa = request.form['cgpa']
        new.uni_passing = request.form['uni_passing']
        new.school = request.form['school']
        new.school_subject = request.form['school_subject']
        new.twelth_marks = request.form['twelth_marks']
        new.school_passing = request.form['school_passing']
        try:
            db.session.commit()
            return redirect(url_for('candidate_profile'))
        except:
            return "erororoorroor"

    print(new)
    return render_template('updateEducation.html',new=new)

@app.route('/updateProject/<int:id>', methods = ['POST','GET'])
def updateProject(id):

    new = db.session.query(candidateProject).filter_by(cid = id).first()
    if request.method == "POST":
        print("If condition runs")
        new.project_name = request.form['project_name']
        new.field = request.form['field']
        new.from_date_project = request.form['from_date_project']
        new.to_date_project = request.form['to_date_project']
        new.project_details = request.form['project_details']
        try:
            db.session.commit()
            return redirect(url_for('candidate_profile'))
        except:
            return "erororoorroor"

    print(new)
    return render_template('updateProject.html',new=new)

@app.route('/updateCertificate/<int:id>', methods = ['POST','GET'])
def updateCertificate(id):

    new = db.session.query(candidateCertificate).filter_by(cid = id).first()
    if request.method == "POST":
        print("If condition runs")
        new.certificate = request.form['certificate']
        new.issue = request.form['issue']
        new.certificate_date = request.form['certificate_date']

        try:
            db.session.commit()
            return redirect(url_for('candidate_profile'))
        except:
            return "erororoorroor"

    print(new)
    return render_template('updateCertificate.html',new=new)

@app.route('/updateSkills/<int:id>', methods = ['POST','GET'])
def updateSkills(id):

    new = db.session.query(candidateSkills).filter_by(cid = id).first()
    if request.method == "POST":
        print("If condition runs")
        new.technical = request.form['technical']
        new.interpersonal = request.form['interpersonal']
        new.interest = request.form['interest']

        try:
            db.session.commit()
            return redirect(url_for('candidate_profile'))
        except:
            return "erororoorroor"

    print(new)
    return render_template('updateSkills.html',new=new)

@app.route('/updateSocial/<int:id>', methods = ['POST','GET'])
def updateSocial(id):

    new = db.session.query(candidateSocial).filter_by(cid = id).first()
    if request.method == "POST":
        print("If condition runs")
        new.linkedin = request.form['linkedin']
        new.facebook = request.form['facebook']
        new.twitter = request.form['twitter']

        try:
            db.session.commit()
            return redirect(url_for('candidate_profile'))
        except:
            return "erororoorroor"

    print(new)
    return render_template('updateSocial.html',new=new)

IMAGE_UPLOADS = join(dirname(realpath(__file__)), 'static/uploads/new/..')
app.config['IMAGE_UPLOADS'] = IMAGE_UPLOADS

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/photo", methods=["GET", "POST"])
def photo():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                filename = str(current_user.id)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image saved")
                return redirect(url_for('candidate_profile'))

            else:
                print("That file extension is not allowed")
                return redirect(url_for('login_candidate'))

    return render_template("/candidate_profile.html")



if __name__ == '__main__':
   app.run(debug = True)
