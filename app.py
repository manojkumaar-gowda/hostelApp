from enum import unique
from flask import Flask,render_template,request, session
from datetime import datetime,timedelta
from sqlalchemy.sql.operators import exists
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import uuid
import random
import os
from werkzeug.wrappers import response
import requests
import pytz


app = Flask(__name__)
app.secret_key = "HOSTEL"
app.permanent_session_lifetime = timedelta(days = 1000)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['UPLOAD_PATH'] =  os.path.join(os.path.dirname(__file__),'static')
db = SQLAlchemy(app)



#student model
class student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_approved = db.Column(db.Boolean, nullable=False, default=False)
    roll_number = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique = True)
    mobile_number = db.Column(db.String(10), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    parent = db.Column(db.String(30), nullable=False)
    parent_mobile_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    pass_id = db.Column(db.String(50), nullable=False,unique = True)
    room_greviance_id = db.Column(db.String(50), nullable=False,unique = True)
    def __repr__(self):
        return 'Student Roll Number : ' + str(self.roll_number)

#digital-outpass model
class Pass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pass_id = db.Column(db.String(50), nullable=False,unique = True)
    student_roll_number = db.Column(db.Integer, nullable=False)
    fromdate = db.Column(db.String(50), nullable=False)
    todate = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    destination_address = db.Column(db.String(100), nullable=False)
    informed_to = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(50), nullable=False)
    pass_status = db.Column(db.String(50), nullable=False)
    applied_on = db.Column(db.String(50), nullable=False)
    hostel_departure = db.Column(db.String(50), nullable=False)
    college_departure = db.Column(db.String(50), nullable=False)
    arrival = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return 'Pass ID : ' + str(self.pass_id)


#departments model
class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False,unique = True)
    def __repr__(self):
        return 'Department : ' + str(self.department)
    #sample departments
    #db.session.add(Departments(department='B.Tech IT'))
    #db.session.add(Departments(department='B.E CSE'))
    #db.session.add(Departments(department='B.E BME'))

#noofyears model
class Years(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer,unique = True)
    def __repr__(self):
        return 'Year : ' + str(self.year)
    #Years
    #db.session.add(Years(year=1))
    #db.session.add(Years(year=2))
    #db.session.add(Years(year=3))

#admin-credentials model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(50), nullable=False,unique = True)
    pwd = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return 'Admin ID : ' + str(self.admin_id)

    #SAMPLE ADMIN-CREDENTIALS
    #db.session.add(Admin(admin_id='menshostel',pwd='Afbcx2mv',role='Male'))
    #db.session.add(Admin(admin_id='ladieshostel',pwd='Afbcx2mv',role='Female'))
    #db.session.add(Admin(admin_id='menshostelgate',pwd='Afbcx2mv',role='Male'))
    #db.session.add(Admin(admin_id='ladieshostelgate',pwd='Afbcx2mv',role='Female'))
    #db.session.add(Admin(admin_id='maingate',pwd='Afbcx2mv',role='MainGate'))

#Common Greviances model
class CommonGreviances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(2500), nullable=False)
    def __repr__(self):
        return 'Roll Number : ' + str(self.roll_number)

#News and Announcements model
class NewsandAnnouncements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(2500), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return 'Id : ' + str(self.id)

#Room Specific grievances model
class RoomSpecificGreviances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_greviance_id = db.Column(db.String(50), nullable=False,unique = True)
    student_roll_number = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    hostel = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    greviances = db.Column(db.String(2500), nullable=False)
    work_status = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(30), nullable=False)
    def __repr__(self):
        return 'Roll Number : ' + str(self.student_roll_number)

#Fast2sms - Message
def sendmsg(message,to):
    message = str(message)
    to = str(to)
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = "sender_id=TXTIND&message="+str(message)+"&route=v3&numbers="+str(to)
    headers = {
        'authorization': "YOUR FAST2SMS KEY",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return 



#Admin-login
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'ladieshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if request.method=="POST":
        adminid = request.form['adminid']
        pwd = request.form['pwd']
        exists = bool(db.session.query(Admin).filter_by(admin_id = adminid).first())
        if exists:
            admin_obj = Admin.query.filter(Admin.admin_id == adminid).first()
            if(pwd == admin_obj.pwd):
                session.permanent = True
                session['admin_id'] = str(admin_obj.admin_id)
                if admin_obj.admin_id == 'menshostel':
                    return redirect('/admin_dashboard')
                elif admin_obj.admin_id == 'Female':
                    return redirect('/admin_dashboard')
                elif admin_obj.admin_id == 'menshostelgate':
                    return redirect('/gate')
                elif admin_obj.admin_id == 'ladieshostelgate':
                    return redirect('/gate')
                elif admin_obj.admin_id == 'maingate':
                    return redirect('/maingatedeparture')
            else:
                return render_template('admin_login.html',message='Invalid Password',id=adminid,pwd=pwd)        
        else:
            return render_template('admin_login.html',message='Account not found',id=adminid,pwd=pwd)        
    return render_template('admin_login.html')


#Admin logout
@app.route('/admin_logout',methods=['GET','POST'])
def admin_logout():
    if "admin_id" in session:
        session.pop('admin_id',None)
    if "year" in session:
        session.pop('year',None)
    return redirect('/admin_login')


#Maingate
#Departure
@app.route('/maingatedeparture',methods=['GET','POST'])
def maingatedeparture():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'ladieshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
    if request.method == 'POST':
        rollnumber = request.form['rollnumber']
        exists = bool(db.session.query(student).filter_by(roll_number = int(rollnumber)).first())
        if not exists:
            return render_template('maingatedeparture.html',message="Invalid roll number")
        else:
            student_obj = student.query.filter(student.roll_number == rollnumber).first()
            admin_obj = Admin.query.filter(Admin.admin_id == session['admin_id']).first()
            #check for outpass if any
            if student_obj.pass_id == str(student_obj.roll_number):
                return render_template('maingatedeparture.html',message="No outpass found")
            else:
                #check if entry was already made at college
                pass_obj = Pass.query.filter(Pass.pass_id == str(student_obj.pass_id)).first()
                if pass_obj.college_departure != 'Pending':
                    return render_template('maingatedeparture.html',message="Entry already made")
                else:
                    #outpass status
                    if pass_obj.pass_status == 'Approved':
                        #check if entry was made at the hostel
                        if pass_obj.hostel_departure != 'Pending':
                            time = str(datetime.now(pytz.timezone('Asia/kolkata')))
                            time = time[0:19]
                            Pass.query.get_or_404(pass_obj.id).college_departure = time
                            db.session.commit()
                            #send SMS to parent
                            message = "Your child "+ student_obj.name + " has successfully left campus on "+ time + ".Please stay connected with your child.\nRegards COLLEGENAME"
                            sendmsg(message,str(student_obj.parent_mobile_number))
                            return render_template('maingatedeparture.html',message="Success")
                        else:
                            return render_template('maingatedeparture.html',message="Entry not made at the hostel")
                    else:
                        return render_template('maingatedeparture.html',message="Pass not approved")
    return render_template('maingatedeparture.html')

#Maingate
#Arrival
@app.route('/maingatearrival',methods=['GET','POST'])
def maingatearrival():
    if "admin_id" not in session:
        return redirect('/admin_login')
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'ladieshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
    if request.method == 'POST':
        rollnumber = request.form['rollnumber']
        exists = bool(db.session.query(student).filter_by(roll_number = int(rollnumber)).first())
        if not exists:
            return render_template('maingatearrival.html',message="Invalid roll number")
        else:
            student_obj = student.query.filter(student.roll_number == rollnumber).first()
            admin_obj = Admin.query.filter(Admin.admin_id == session['admin_id']).first()
            # check for outpass
            if student_obj.pass_id == str(student_obj.roll_number):
                return render_template('maingatearrival.html',message="No outpass found")
            else:
                pass_obj = Pass.query.filter(Pass.pass_id == str(student_obj.pass_id)).first()
                #check if entry was already made
                if pass_obj.arrival != 'Pending':
                    return render_template('maingatearrival.html',message="Entry already made")
                else:
                    #check if entry was not made before departure of both college and hostel
                    if pass_obj.hostel_departure == 'Pending' or pass_obj.college_departure == 'Pending':
                        return render_template('maingatearrival.html',message="Entry not made before Departure")
                    else:
                        #check pass status
                        if pass_obj.pass_status == 'Pending':
                            return render_template('maingatearrival.html',message="Pass not approved")
                        else:

                            student.query.get_or_404(student_obj.id).pass_id = rollnumber
                            time = str(datetime.now(pytz.timezone('Asia/kolkata')))
                            time = time[0:19]
                            Pass.query.get_or_404(pass_obj.id).arrival = time
                            db.session.commit()
                            #send SMS to parent
                            message = "Your child "+ student_obj.name + " has successfully arrived at campus on "+ time + "\nRegards COLLEGENAME"
                            sendmsg(message,str(student_obj.parent_mobile_number))
                            return render_template('maingatearrival.html',message="Success")            
    return render_template('maingatearrival.html')


#HOSTEL-GATE-Departure only
@app.route('/gate',methods=['GET','POST'])
def gate():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'ladieshostel':
            return redirect('/admin_dashboard')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if request.method == 'POST':
        rollnumber = request.form['rollnumber']
        exists = bool(db.session.query(student).filter_by(roll_number = int(rollnumber)).first())
        if not exists:
            return render_template('gate.html',message="Invalid roll number")
        else:
            student_obj = student.query.filter(student.roll_number == rollnumber).first()
            admin_obj = Admin.query.filter(Admin.admin_id == session['admin_id']).first()
            #check for gender and hostel role
            if admin_obj.role != student_obj.gender:
                return render_template('gate.html',message="Access denied")
            else:
                #outpass availability for that student
                if student_obj.pass_id == str(student_obj.roll_number):
                    return render_template('gate.html',message="No outpass found")
                else:
                    pass_obj = Pass.query.filter(Pass.pass_id == str(student_obj.pass_id)).first()
                    #entry already made or not
                    if pass_obj.hostel_departure != 'Pending':
                            return render_template('gate.html',message="Entry already made")
                    else:
                        #outpass status
                        if pass_obj.pass_status == 'Approved':
                            time = str(datetime.now(pytz.timezone('Asia/kolkata')))
                            time = time[0:19]
                            Pass.query.get_or_404(pass_obj.id).hostel_departure = time
                            db.session.commit()
                            return render_template('gate.html',message="Success")
                        else:
                            return render_template('gate.html',message="Pass not approved")
    return render_template('gate.html')




#admin-dashboard
@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    #set year
    year_obj = Years.query.all()
    if request.method == 'POST':
        year = request.form['year']
        session['year'] = year
        message = "YEAR "+ str(year) +" SELECTED"
        return render_template('admin_dashboard.html',message = message,year_obj = year_obj)
    return render_template('admin_dashboard.html',year_obj = year_obj)


#new Pass approvals
@app.route('/new_approvals',methods=['GET','POST'])
def new_approvals():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)
    Pass_obj = Pass.query.filter(Pass.pass_status == 'Pending').all()
    pass_obj = {}
    i = 1
    admin_obj = Admin.query.filter(Admin.admin_id == str(session['admin_id'])).first()
    #filtering gender specific passes along with year filtering
    for x in Pass_obj:
        roll = x.student_roll_number
        student_obj = student.query.filter(student.roll_number == int(roll)).first()
        if student_obj.gender == admin_obj.role and int(student_obj.year) == int(session['year']):
            x = {'id':x.id,'pass_id':x.pass_id,'name':student_obj.name,'student_roll_number':x.student_roll_number,'reason':x.reason,'informed_to':x.informed_to,'mobile_number':x.mobile_number,'applied_on':x.applied_on,'college_departure':x.college_departure,'arrival':x.arrival}
            pass_obj[i] = x
            i+=1
    return render_template('new_approvals.html',Pass_obj = pass_obj)

#Approve new application
@app.route('/newapproveapplication/<id>',methods=['GET','POST'])
def new_approve_application(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)

    #check for pass_id availability
    exists = bool(db.session.query(Pass).filter_by(pass_id = str(id)).first())
    if not exists:
        return redirect('/new_approvals')
    
    #approve application
    pass_obj = Pass.query.filter(Pass.pass_id == str(id)).first()
    Pass.query.get_or_404(pass_obj.id).pass_status = "Approved"
    db.session.commit()
    #inform parent
    
    message = "Outpass granted to your child.\nDestination address:"+str(pass_obj.destination_address) + "\nDate of departure:"+pass_obj.fromdate+"\nRegards COLLEGENAME "
    to = str(pass_obj.mobile_number)
    sendmsg(message,to)
    return redirect('/new_approvals')

#Reject new application
@app.route('/newrejectapplication/<id>',methods=['GET','POST'])
def new_reject_application(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)
    
    #check for pass_id availability
    exists = bool(db.session.query(Pass).filter_by(pass_id = str(id)).first())
    if not exists:
        return redirect('/new_approvals')

    pass_obj = Pass.query.filter(Pass.pass_id == str(id)).first()
    roll = Pass.query.get_or_404(pass_obj.id).student_roll_number
    #delete pass
    deleteobj = Pass.query.get_or_404(pass_obj.id)
    db.session.delete(deleteobj)
    #change pass_id to rollnumber
    student_obj = student.query.filter(student.roll_number == int(roll)).first()
    student.query.get_or_404(student_obj.id).pass_id = str(roll)
    db.session.commit()
    return redirect('/new_approvals')


#put application on hold
@app.route('/holdapplication/<id>',methods=['GET','POST'])
def holdapplication(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)

    #check for pass_id availability
    exists = bool(db.session.query(Pass).filter_by(pass_id = str(id)).first())
    if not exists:
        return redirect('/hold_applications')
    
    #put application on hold
    pass_obj = Pass.query.filter(Pass.pass_id == str(id)).first()
    Pass.query.get_or_404(pass_obj.id).pass_status = "Hold"
    db.session.commit()
    return redirect('/new_approvals')



#view application - common for new and hold applications
@app.route('/viewapplication/<id>',methods=['GET','POST'])
def view_application(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)
    
    #check for pass_id availability
    exists = bool(db.session.query(Pass).filter_by(pass_id = str(id)).first())
    if not exists:
        return redirect('/hold_applications')
    
    #get pass credentials
    Pass_obj = Pass.query.filter(Pass.pass_id == str(id)).first()
    roll = Pass_obj.student_roll_number
    student_obj = student.query.filter(student.roll_number == int(roll)).first()
    Pass_obj = {'address':Pass_obj.destination_address,'fromdate':Pass_obj.fromdate,'todate':Pass_obj.todate,'id':Pass_obj.id,'pass_id':Pass_obj.pass_id,'name':student_obj.name,'email':student_obj.email,'department':student_obj.department,'year':student_obj.year,'student_roll_number':Pass_obj.student_roll_number,'reason':Pass_obj.reason,'informed_to':Pass_obj.informed_to,'mobile_number':Pass_obj.mobile_number,'applied_on':Pass_obj.applied_on,'college_departure':Pass_obj.college_departure,'arrival':Pass_obj.arrival}

    return render_template('view_application.html',Pass_obj= Pass_obj)


#Applications on hold
@app.route('/hold_applications',methods=['GET','POST'])
def hold_applications():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)

    Pass_obj = Pass.query.filter(Pass.pass_status == 'Hold').all()
    Pass_obj = Pass_obj[::-1]
    pass_obj = {}
    i = 1
    admin_obj = Admin.query.filter(Admin.admin_id == str(session['admin_id'])).first()
    #filtering applications based on gender and year selected
    for x in Pass_obj:
        roll = x.student_roll_number
        student_obj = student.query.filter(student.roll_number == int(roll)).first()
        if student_obj.gender == admin_obj.role and int(student_obj.year) == int(session['year']):
            x = {'id':x.id,'pass_id':x.pass_id,'name':student_obj.name,'student_roll_number':x.student_roll_number,'reason':x.reason,'informed_to':x.informed_to,'mobile_number':x.mobile_number,'applied_on':x.applied_on,'college_departure':x.college_departure,'arrival':x.arrival}
            pass_obj[i] = x
            i+=1
    
    return render_template('hold_Applications.html',Pass_obj = pass_obj)

#Approve applications on hold
@app.route('/approveholdapplication/<id>',methods=['GET','POST'])
def approve_application(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)
    exists = bool(db.session.query(Pass).filter_by(pass_id = str(id)).first())
    if not exists:
        return redirect('/hold_applications')
    pass_obj = Pass.query.filter(Pass.pass_id == str(id)).first()
    Pass.query.get_or_404(pass_obj.id).pass_status = "Approved"
    db.session.commit()
    #inform parent
    message = "Outpass granted to your child.\nDestination address:"+str(pass_obj.destination_address) + "\nDate of departure:"+str(pass_obj.fromdate)+"\nRegards COLLEGENAME"
    to = str(pass_obj.mobile_number)
    sendmsg(message,to)
    return redirect('/hold_applications')

#Reject applications on Hold
@app.route('/rejectholdapplication/<id>',methods=['GET','POST'])
def reject_application(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)
   
    exists = bool(db.session.query(Pass).filter_by(pass_id = str(id)).first())
    if not exists:
        return redirect('/hold_applications')
    
    pass_obj = Pass.query.filter(Pass.pass_id == str(id)).first()
    roll = Pass.query.get_or_404(pass_obj.id).student_roll_number
    #delete pass
    deleteobj = Pass.query.get_or_404(pass_obj.id)
    db.session.delete(deleteobj)
    #update pass_id in student
    student_obj = student.query.filter(student.roll_number == int(roll)).first()
    student.query.get_or_404(student_obj.id).pass_id = str(roll)
    db.session.commit()
    return redirect('/hold_applications')


#All applications - display all outpass
@app.route('/all_applications')
def all_applications():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if "year" not in session:
        year_obj = Years.query.all()
        return render_template('admin_dashboard.html',message = "Please select an year to continue",year_obj = year_obj)
    Pass_obj = Pass.query.all()
    Pass_obj = Pass_obj[::-1]
    pass_obj = {}
    i = 1
    #filter records based on gender and year
    admin_obj = Admin.query.filter(Admin.admin_id == str(session['admin_id'])).first()
    for x in Pass_obj:
        roll = x.student_roll_number
        student_obj = student.query.filter(student.roll_number == int(roll)).first()
        if student_obj.gender == admin_obj.role and int(student_obj.year) == int(session['year']):
            x = {'id':x.id,'pass_id':x.pass_id,'student_roll_number':x.student_roll_number,'reason':x.reason,'informed_to':x.informed_to,'mobile_number':x.mobile_number,'applied_on':x.applied_on,'college_departure':x.college_departure,'arrival':x.arrival}
            pass_obj[i] = x
            i+=1
    return render_template('all_applications.html',Pass_obj = pass_obj)


#student details
@app.route('/student_details',methods=['GET','POST'])
def student_details():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    
    #search by roll number
    if request.method == "POST":
        rollnumber = request.form['rollnumber']
        rollnumber = int(rollnumber)
        exists = bool(db.session.query(student).filter_by(roll_number = int(rollnumber)).first())
        #check if roll number is valid or not
        if exists:
            student_obj = student.query.filter(student.roll_number == int(rollnumber)).first()
            admin_obj = Admin.query.filter(Admin.admin_id == str(session['admin_id'])).first()
            department_obj = Departments.query.all()
            years_obj = Years.query.all()
            #gender validation
            if student_obj.gender == admin_obj.role:
                return render_template('student_details.html',message="Details Fetched",rollnumber = rollnumber,student_obj = student_obj,show = True,roll = str(student_obj.roll_number),department_obj = department_obj,years_obj = years_obj)        
            else:
                return render_template('student_details.html',message="Access denied",rollnumber = rollnumber)        
        else:
            return render_template('student_details.html',message="Account not found",rollnumber = rollnumber)        
    return render_template('student_details.html')

#Approve new accounts
@app.route('/approveaccount/<int:id>')
def accountapprove(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    admin_obj = Admin.query.filter(Admin.admin_id == str(session['admin_id'])).first()
    student_obj = student.query.get_or_404(id)
    if student_obj.gender != admin_obj.role:
        return render_template('student_details.html',message="Access denied")        
    student.query.get_or_404(id).account_approved = True
    db.session.commit()
    return redirect('/student_details')

#Update student account
@app.route('/update_student',methods=['POST'])
def update_student():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if request.method == "POST":
        rollnumber = request.form['roll_number']
        name = request.form['name']
        gender = request.form['gender']
        department = request.form['department']
        dob = request.form['dob']
        email = request.form['email']
        mobile = request.form['mobile']
        year = request.form['year']
        parent = request.form['parent']
        pnumber = request.form['pnumber']
        address = request.form['address']
        roomnumber = request.form['roomnumber']
        student_obj = student.query.filter(student.roll_number == int(rollnumber) ).first()
        student.query.get_or_404(student_obj.id).roll_number = rollnumber
        student.query.get_or_404(student_obj.id).name = name
        student.query.get_or_404(student_obj.id).gender = gender
        student.query.get_or_404(student_obj.id).department = department
        student.query.get_or_404(student_obj.id).dob = dob
        student.query.get_or_404(student_obj.id).email = email
        student.query.get_or_404(student_obj.id).mobile_number = mobile
        student.query.get_or_404(student_obj.id).year = year
        student.query.get_or_404(student_obj.id).parent = parent
        student.query.get_or_404(student_obj.id).parent_mobile_number = pnumber
        student.query.get_or_404(student_obj.id).address = address
        student.query.get_or_404(student_obj.id).room_number = roomnumber
        db.session.commit()
        student_obj = student.query.filter(student.roll_number == int(rollnumber)).first()
        return render_template('student_details.html',message = "Changes saved",rollnumber = rollnumber)

#cancel outpass
@app.route('/deleteoutpass/<id>',methods=['POST','GET'])
def deleteoutpass(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    
    exists = bool(db.session.query(Pass).filter_by(pass_id = str(id)).first())
    if not exists:
        return render_template('student_details.html',message = "Outpass ID Invalid")
    
    pass_obj = Pass.query.filter(Pass.pass_id == str(id)).first()
    roll = Pass.query.get_or_404(pass_obj.id).student_roll_number
    #delete pass
    deleteobj = Pass.query.get_or_404(pass_obj.id)
    db.session.delete(deleteobj)
    #update pass_id in student
    student_obj = student.query.filter(student.roll_number == int(roll)).first()
    student.query.get_or_404(student_obj.id).pass_id = str(roll)
    db.session.commit()
    return render_template('student_details.html',message = "Successfully cancelled the outpass",rollnumber = roll)


#Delete user
@app.route('/deletestudentuser/<int:id>',methods=['POST','GET'])
def deletestudentuser(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    admin_obj = Admin.query.filter(Admin.admin_id == str(session['admin_id'])).first()
    student_obj = student.query.get_or_404(id)
    #gender verification
    if student_obj.gender != admin_obj.role:
        return render_template('student_details.html',message="Access denied")        
    student_obj = student.query.get_or_404(id)
    db.session.delete(student_obj)
    db.session.commit()
    return render_template('student_details.html',message="Student Account successfully deleted") 

#Manage departments and years
@app.route('/dept_and_years',methods=['GET','POST'])
def deptandyears():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    departments_obj = Departments.query.all()
    years_obj = Years.query.all()
    return render_template('dept_And_years.html',departments_obj = departments_obj,years_obj = years_obj)

#Add department
@app.route('/add_department',methods=['GET',"POST"])
def add_department():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    
    if request.method == "POST":
        department = request.form['department']
        exists = bool(db.session.query(Departments).filter_by(department = str(department)).first())
        if exists:
            departments_obj = Departments.query.all()
            years_obj = Years.query.all()
            return render_template('dept_and_years.html',message = "Department already exists", departments_obj = departments_obj, years_obj = years_obj)
        db.session.add(Departments(department=department))
        db.session.commit()
        return redirect('/dept_and_years')

#Add department
@app.route('/add_year',methods=['GET',"POST"])
def add_year():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if request.method == "POST":
        year = request.form['year']
        exists = bool(db.session.query(Years).filter_by(year = str(year)).first())
        if exists:
            departments_obj = Departments.query.all()
            years_obj = Years.query.all()
            return render_template('dept_and_years.html',message = "Year already exists", departments_obj = departments_obj, years_obj = years_obj)
        db.session.add(Years(year=year))
        db.session.commit()
        return redirect('/dept_and_years')

#Delete department
@app.route('/deletedepartment/<int:id>',methods=['GET',"POST"])
def delete_department(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    
    
    db.session.delete(Departments.query.get_or_404(id))
    db.session.commit()
    return redirect('/dept_and_years')


#Delete year
@app.route('/deleteyear/<int:id>',methods=['GET',"POST"])
def delete_year(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')

    db.session.delete(Years.query.get_or_404(id))
    db.session.commit()
    return redirect('/dept_and_years')


#accounts
@app.route('/accounts',methods=['GET',"POST"])
def accounts():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    if request.method == "POST":
        adminid = request.form['adminid']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        exists = bool(db.session.query(Admin).filter_by(admin_id = str(adminid)).first())
        if not exists:
            return render_template('accounts.html',message = "Account not found")
        admin_obj = Admin.query.filter(Admin.admin_id == adminid).first()
        Admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.role != Admin_obj.role:
            return render_template('accounts.html',message = "Access denied")
        if password != confirmpassword:
            return render_template('accounts.html',message = "Passwords dont match")
        Admin.query.get_or_404(admin_obj.id).pwd = password
        db.session.commit()
    
    return render_template('accounts.html')



   
#Admin News and Announcements
@app.route('/admin_news_and_announcements',methods=['GET',"POST"])
def admin_news_and_announcements():
    if "admin_id" not in session:
        return redirect('/admin_login')
    
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    Admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()       
    if request.method == "POST":
        gender = Admin_obj.role
        title = request.form['title']
        message = request.form['message']
        filenametemp = str(uuid.uuid4())
        filename = request.files['myfile']
        filename1 = request.form['myfileval']
        if filename1 != '':
            #if has file
            filename1 = filename1.split('.')
            extension = filename1[-1]
            x = os.path.join(os.path.dirname(__file__),'static')
            print(x)
            filepath = os.path.join(x,"announcements")
            print(filepath)
            renamed_file = filenametemp +'.' + str(extension)
            x = os.path.join(filepath,renamed_file)
            print(x)
            try:
                
                filename.save(x)
            except Exception as e: 
                print(e)
            new_obj = NewsandAnnouncements(gender = gender,title = title,message = message,filename = filenametemp,extension = extension)
  
        else:
            new_obj = NewsandAnnouncements(gender = gender,title = title,message = message,filename = '',extension = '')
        db.session.add(new_obj)
        db.session.commit()
        return redirect('/admin_news_and_announcements')
    newsandannouncements_obj = NewsandAnnouncements.query.filter(NewsandAnnouncements.gender == Admin_obj.role).all()
    return render_template('admin_news_and_announcements.html',newsandannouncements_obj = newsandannouncements_obj)

#Admin Common Grievance
@app.route('/admin_common_grievances',methods=['GET',"POST"])
def common_grievances():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    Admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
    if request.method == 'POST':
        message = request.form['message']
        roll_number = 123
        gender = Admin_obj.role
        time = str(datetime.now(pytz.timezone('Asia/kolkata')))
        time = time[0:19]
        newGreviances = CommonGreviances(roll_number = roll_number,gender = gender,message = message,time = time)
        db.session.add(newGreviances)
        db.session.commit()
        return redirect('/admin_common_grievances')
    greviance_obj = CommonGreviances.query.filter(CommonGreviances.gender == Admin_obj.role).all()
    return render_template('admin_common_greviances.html',greviance_obj = greviance_obj)

#Admin delete chat
@app.route('/deletechat/<int:id>')
def deletechat(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    chatdel = CommonGreviances.query.get(id)
    db.session.delete(chatdel)
    db.session.commit()
    return redirect('/admin_common_grievances')

#Admin delete Post
@app.route('/deletenews/<int:id>/<filename>')
def deletenews(id,filename):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    path = os.path.join(os.path.join(os.path.dirname(__file__),'static'), 'announcements')
    my_file = os.path.join(path, filename)
    if filename != 'none' and os.path.exists(my_file):
        os.remove(os.path.join(path, filename))
    newsdel = NewsandAnnouncements.query.get(id)
    db.session.delete(newsdel)
    db.session.commit()
    return redirect('/admin_news_and_announcements')

#Admin New Repairs
@app.route('/new_repairs',methods=['GET','POST'])
def new_repairs():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
    grev_obj = RoomSpecificGreviances.query.filter(RoomSpecificGreviances.gender == admin_obj.role , RoomSpecificGreviances.work_status != 'Completed').all()
    print(grev_obj)
    return render_template('new_repairs.html',grev_obj = grev_obj)

#Admin Work done
@app.route('/workcomplete/<int:id>',methods=['GET','POST'])
def workcomplete(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    work_obj = RoomSpecificGreviances.query.get(id)
    work_obj.work_status = 'Completed'
    db.session.commit()
    return redirect('/new_repairs')

#Admin Work-Hold
@app.route('/holdwork/<int:id>',methods=['GET','POST'])
def holdwork(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    work_obj = RoomSpecificGreviances.query.get(id)
    work_obj.work_status = 'Hold'
    db.session.commit()
    return redirect('/new_repairs')

#Admin Work-inprogress
@app.route('/worktaken/<int:id>',methods=['GET','POST'])
def worktaken(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    work_obj = RoomSpecificGreviances.query.get(id)
    work_obj.work_status = 'In-Progress'
    db.session.commit()
    return redirect('/new_repairs')

#Admin Work-Delete
@app.route('/deletework/<int:id>',methods=['GET','POST'])
def deletework(id):
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    work_obj = RoomSpecificGreviances.query.get(id)
    rollnumber = int(work_obj.student_roll_number)
    db.session.delete(work_obj)
    student_obj = student.query.filter(student.roll_number == rollnumber).first()
    student_obj.query.get(student_obj.id).room_greviance_id = rollnumber
    db.session.commit()
    return redirect('/new_repairs')

#Admin all repairs
@app.route('/all_repairs',methods=['GET','POST'])
def all_repairs():
    if "admin_id" not in session:
        return redirect('/admin_login')
    #check admin type
    if "admin_id" in session:
        admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
        if admin_obj.admin_id == 'menshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'ladieshostelgate':
            return redirect('/gate')
        elif admin_obj.admin_id == 'maingate':
            return redirect('/maingatedeparture')
    admin_obj = Admin.query.filter(Admin.admin_id == session["admin_id"]).first()
    grev_obj = RoomSpecificGreviances.query.filter(RoomSpecificGreviances.gender == admin_obj.role).all()
    grev_obj = grev_obj[::-1]
    return render_template('all_repairs.html',grev_obj = grev_obj)

#Student
#student logout
@app.route('/studentlogout',methods=['GET','POST'])
def studentlogout():
    if "user_id" in session:
        session.pop('user_id',None)
    return redirect('/loginAsStudent')



#student signup
@app.route('/studentsignup',methods=['GET','POST'])
def studentsignup():
    if "user_id" in session:
        return redirect('/')
    department_obj = Departments.query.all()
    years_obj = Years.query.all()
    if request.method == "POST":
        rollnumber = request.form['rollnumber']
        fullname = request.form['fullname']
        gender = request.form['gender']
        year = request.form['year']
        department = request.form['department']
        dob = request.form['dob']
        email = request.form['email']
        roomnumber = request.form['roomnumber']
        mobilenumber = request.form['mobilenumber']
        parent = request.form['parent']
        pmobilenumber = request.form['pmobilenumber']
        address = request.form['address']
        pwd = request.form['pwd']
        pwd1 = request.form['pwd1']
        exists = bool(db.session.query(student).filter_by(roll_number = int(rollnumber)).first())
        emailexists = bool(db.session.query(student).filter_by(email = email).first())
        mobileexists = bool(db.session.query(student).filter_by(mobile_number = str(mobilenumber)).first())
        #unique attributes
        if not exists and not emailexists and not mobileexists:
            #parent and student mobile number
            if str(mobilenumber) == str(pmobilenumber):
                return render_template('student_registration.html',message="Invalid credentials",roomnumber = roomnumber, rollnumber = rollnumber,fullname=fullname,gender=gender,year = year,department = department,dob = dob,email=email,mobilenumber=mobilenumber,parent = parent,pmobilenumber = pmobilenumber,address = address,pwd = pwd,department_obj=department_obj,years_obj = years_obj)
            #unfilled fields
            elif gender == '' or year == '' or department == '' or dob == '':
                return render_template('student_registration.html',message="Please fill all the details",roomnumber = roomnumber, rollnumber = rollnumber,fullname=fullname,gender=gender,year = year,department = department,dob = dob,email=email,mobilenumber=mobilenumber,parent = parent,pmobilenumber = pmobilenumber,address = address,pwd = pwd,department_obj=department_obj,years_obj = years_obj)
            #dissimilar passwords
            elif pwd != pwd1:
                return render_template('student_registration.html',message="Passwords dont match",roomnumber = roomnumber, rollnumber = rollnumber,fullname=fullname,gender=gender,year = year,department = department,dob = str(dob),email=email,mobilenumber=mobilenumber,parent = parent,pmobilenumber = pmobilenumber,address = address,pwd = pwd,department_obj=department_obj,years_obj = years_obj)    
            else:
                try:
                    password = pwd
                    time = str(datetime.now(pytz.timezone('Asia/kolkata')))
                    time = time[0:19]
                    newstudent = student(roll_number = int(rollnumber),name = fullname, gender = gender, year = year, department = department, dob = str(dob),email = email,mobile_number = str(mobilenumber),parent = parent,  parent_mobile_number =  str(pmobilenumber),address = address, date_joined = time,password = str(password),pass_id= str(rollnumber),room_number = roomnumber,room_greviance_id =str(rollnumber))
                    db.session.add(newstudent)
                    db.session.commit()
                    return redirect('/loginAsStudent')
                except:
                    return render_template('student_registration.html',message="Please provide valid credentials",roomnumber = roomnumber,rollnumber = rollnumber,fullname=fullname,gender=gender,year = year,department = department,dob = dob,email=email,mobilenumber=mobilenumber,parent = parent,pmobilenumber = pmobilenumber,address = address,pwd = pwd,department_obj=department_obj,years_obj = years_obj)
        else:
            return render_template('student_registration.html',message="An account already exists with these credentials",roomnumber = roomnumber, rollnumber = rollnumber,fullname=fullname,gender=gender,year = year,department = department,dob = dob,email=email,mobilenumber=mobilenumber,parent = parent,pmobilenumber = pmobilenumber,address = address,pwd = pwd,department_obj=department_obj,years_obj = years_obj)
    return render_template('student_registration.html',department_obj=department_obj,years_obj = years_obj)

#forgot password
@app.route('/forgotpwd',methods=['GET',"POST"])
def forgotpwd():
    if "user_id" in session:
        return redirect('/')
    if request.method == "POST":
        email = request.form['email']
        emailexists = bool(db.session.query(student).filter_by(email = email).first())
        if emailexists:
            newpassword = random.randint(100000,999999)
            student_obj = student.query.filter(student.email == email).first()
            student.query.get_or_404(student_obj.id).password = str(newpassword)
            db.session.commit()
            newpassword = str(newpassword)
            to = str(student_obj.mobile_number)
            message = "Your Temporary password is "+ str(newpassword) + ". Please make sure that you change your password after login. \nRegards COLLEGENAME"
            sendmsg(message,to)
            print(newpassword)
            return redirect('/loginAsStudent')
        else:
            return render_template('forgotpwd.html',message = "Email ID not found")
    return render_template('forgotpwd.html')


#student login
@app.route('/loginAsStudent',methods=['GET','POST'])
def loginAsStudent():
    if "user_id" in session:
        return redirect('/')
    if request.method == "POST":
        rollnumber = request.form['rollnumber']
        password = request.form['password']
        rollexists = bool(db.session.query(student).filter_by(roll_number = int(rollnumber)).first())
        if rollexists:
            student_obj = student.query.filter(student.roll_number == int(rollnumber)).first()
            if password == student_obj.password:
                
                if student_obj.account_approved:
                    session.permanent = True
                    session['user_id'] = rollnumber   
                    return redirect('/')
                else:
                    return render_template('student_login.html',message = "Please wait patiently till your account gets approved by the admin", rollnumber = rollnumber,password = password)
            else:
                return render_template('student_login.html',message = "Invalid Password", rollnumber = rollnumber,password = password)
        else:
            return render_template('student_login.html',message = "Account not found", rollnumber = rollnumber,password = password)
    return render_template('student_login.html')

#student dashboard
@app.route('/',methods=['GET','POST'])
def student_dashboard():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
    pass_obj = Pass.query.filter(Pass.pass_id == str(student_obj.pass_id)).first()
    return render_template('student_dashboard.html',student_obj = student_obj,pass_obj = pass_obj,roll = str(student_obj.roll_number))


#Delete application
@app.route('/deleteapplication',methods=['GET',"POST"])
def delate_application():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    if request.method == "POST":
        student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
        pass_obj = Pass.query.filter(Pass.pass_id == student_obj.pass_id).first()
        deleteid = Pass.query.get_or_404(pass_obj.id)
        db.session.delete(deleteid)
        student.query.get_or_404(student_obj.id).pass_id = str(student_obj.roll_number)
        db.session.commit()
        return redirect('/')

#applyforoutpass
@app.route('/applynew',methods=['GET','POST'])
def applynew():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
    if request.method == "POST":      
        fromdate = request.form['from']
        todate = request.form['to']
        reason = request.form['reason']
        address = request.form['address']
        parent = request.form['parent']
        pmobile = request.form['pmobile']
        unique_id = str(uuid.uuid4())
        time = str(datetime.now(pytz.timezone('Asia/kolkata')))
        time = time[0:19]
        passobj = Pass(pass_id = str(unique_id),student_roll_number = int(student_obj.roll_number),fromdate = fromdate,todate = todate,reason = reason,destination_address = address,informed_to = parent,mobile_number = pmobile,pass_status = 'Pending',applied_on = time,hostel_departure  = 'Pending',college_departure = 'Pending',arrival = 'Pending')
        db.session.add(passobj)
        student.query.get_or_404(student_obj.id).pass_id = str(unique_id)
        db.session.commit()
        return redirect('/')
    if str(student_obj.roll_number) == student_obj.pass_id:
        return render_template('applynew.html',student_obj = student_obj)
    pass_obj = Pass.query.filter(Pass.pass_id == str(student_obj.pass_id)).first()
    return render_template('student_dashboard.html',student_obj = student_obj,message = "You already have an existing Pass",pass_obj = pass_obj,roll= str(student_obj.roll_number))
    
#previous outpass
@app.route('/previoussubmissions')
def previoussubmissions():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
    pass_obj = Pass.query.filter(Pass.student_roll_number == int(student_obj.roll_number)).all()
    return render_template('previous_submisssions.html',pass_obj = pass_obj,student_obj = student_obj)


#settings
@app.route('/settings',methods=['GET','POST'])
def settings():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
    years_obj = Years.query.all()
    if request.method == "POST":
        year = request.form['year']
        number = request.form['number']
       
        address = request.form['address']
        roomnumber = request.form['roomnumber']
        password = request.form['password']
        student.query.get_or_404(student_obj.id).year = year
        student.query.get_or_404(student_obj.id).mobile_number = number
        student.query.get_or_404(student_obj.id).address = address
        student.query.get_or_404(student_obj.id).room_number = roomnumber
        student.query.get_or_404(student_obj.id).password = password
        db.session.commit()
        return render_template('settings.html',student_obj = student_obj,message = "Changes saved",years_obj=years_obj)
    return render_template('settings.html',student_obj = student_obj,years_obj=years_obj)


#Common Greviances
@app.route('/common_greviances',methods=['GET','POST'])
def common_greviances():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
    if request.method == "POST":
        message = request.form['message']
        roll_number = student_obj.roll_number
        gender = student_obj.gender
        time = str(datetime.now(pytz.timezone('Asia/kolkata')))
        time = time[0:19]
        newGreviances = CommonGreviances(roll_number = roll_number,gender = gender,message = message,time = time)
        db.session.add(newGreviances)
        db.session.commit()
        return redirect('/common_greviances')
    greviance_obj = CommonGreviances.query.filter(CommonGreviances.gender == student_obj.gender).all()
    return render_template('student_common_chats.html',student_obj = student_obj,greviance_obj = greviance_obj)

#News and Announcements
@app.route('/news_and_announcements')
def news_and_announcements():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
    newsandannouncements_obj = NewsandAnnouncements.query.filter(NewsandAnnouncements.gender == student_obj.gender).all()
    return render_template('news_and_announcements.html',student_obj = student_obj,newsandannouncements_obj = newsandannouncements_obj)


#Room specific Greviances
@app.route('/room_greviances',methods=['GET','POST'])
def room_greviances():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
    if request.method == "POST":
        hostel = request.form['hostel']
        category = request.form['category']
        greviances = request.form['greviances']
        grev_id = str(uuid.uuid4())
        time = str(datetime.now(pytz.timezone('Asia/kolkata')))
        time = time[0:19]
        newGrev = RoomSpecificGreviances(room_number =student_obj.room_number, room_greviance_id = grev_id, student_roll_number = student_obj.roll_number,gender = student_obj.gender,hostel = hostel,category = category,greviances = greviances,work_status = 'Pending',time = time)
        db.session.add(newGrev)
        student.query.get_or_404(student_obj.id).room_greviance_id = grev_id
        db.session.commit()
        return redirect('/room_greviances')
    grev_obj = RoomSpecificGreviances.query.filter(RoomSpecificGreviances.room_greviance_id == str(student_obj.room_greviance_id)).first()
    return render_template('room_greviances.html',student_obj = student_obj,grev_obj = grev_obj, roll = str(student_obj.roll_number))

#Room specific Greviances
@app.route('/deletegreviances',methods=['POST'])
def deletegreviances():
    if "user_id" not in session:
        return redirect('/loginAsStudent')
    if request.method == "POST":
        student_obj = student.query.filter(student.roll_number == int(session['user_id'])).first()
        student.query.get_or_404(student_obj.id).room_greviance_id = str(student_obj.roll_number)
        db.session.commit()
        return redirect('/room_greviances')

@app.route('/team_members')
def team_members():
    return render_template('team_members.html')

@app.errorhandler(500)
def not_found(e):
    return render_template('err.html')

@app.route('/fixerror')
def fixerror():
    session.pop("user_id",None)
    return redirect('/loginAsStudent')


if __name__ == "__main__":
    app.run(debug=True)
