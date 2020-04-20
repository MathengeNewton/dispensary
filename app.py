from flask import Flask, render_template, url_for, session, redirect, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:mathenge,./1998@localhost/dispensary'
app.config['SECRET_KEY'] = 'some=secret+key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
UPLOAD_FOLDER = os.getcwd() + '/static/uploads/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# db models
# customer db model class

from models.mymodels import *
from functions.functions import *

@app.route('/reception')
def reception():
   

    activity = patient_session.active_session()
    try:
        x = 0 
        mysessions = []
        length = len(activity)
        while x <= length:
            p = activity[x]
            i = p.patient
            # print (i)
            sessions = patients.select_patient_by_id(i)
            # print (sessions)
            s = sessions.name
            # print(s)
            mysessions.append(sessions)
            for item in mysessions:
                for x in item:
                    print (x)
            x +=1
              
        return render_template('reception.html',session = mysessions)
    except:
        return render_template('reception.html')

@app.route('/reception/search-patient')
def r_search():
    return render_template('search_patient.html')


@app.route('/search_patient',methods=['POST','GET'])
def search_patient():
    if request.method == 'POST':
        name = request.form['name']
        patient = patients.select_patient_by_name(name)
        return render_template('search_patient.html',patient = patient)
    else:
        return render_template('search_patient.html')

@app.route('/reception/add-patient')
def add_patient():
    return render_template('addpatient.html')

@app.route('/add-patient',methods=['POST'])
def create_patient_record():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        age = request.form['age']
        gender = request.form['gender']
        condition = request.form['condition']

        newpatient = patients(name = name,contact=contact,
                age = age,gender = gender,condition = condition)
        newpatient.insert_record()

        patient = patients.select_patient_by_name(name)
        return render_template('search_patient.html',
            patient = patient,lastvisit = "no record")
    else:
        message = 'An error occured'
        flash(message,'danger')
        return render_template('search_patient.html')
@app.route('/create_session/<int:id>',methods = ['POST','GET'])
def create_session(id):
    date = datetime.date.today()
    t = datetime.datetime.now()
    time = t.time()
    newsession = patient_session(patient = id,
                date = date,status = 'active',start = time)
    newsession.create_session()
    return redirect(url_for('reception'))
    


@app.route('/doctor/home')
def doc_dash():
    return render_template("doctor'sdash.html")

@app.route('/doctor/active')
def doc_active_dash():
    return render_template('doc.activesession.html')

@app.route('/doctor/search-patient')
def doc_search_patient():
    return render_template('doc.searchpatient.html')

@app.route('/cashier')
def cashier_dash():
    return render_template('cashier.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')
    
@app.route('/lab/que')
def lab_que():
    return render_template('lablist.html')

@app.route('/lab')
def lab_session():
    return render_template('lab_session.html')

@app.route('/login')
def owners_login():
    # if request.method == 'POST':
    #     # try:
    #     email = request.form['email']
    #     password = request.form['password']

    #     # check if email exist
    #     if owners.check_email_exist(email):
    #         if owners.validate_password(email=email, password=password):
    #             session['email'] = email
    #             session['uid'] = owners.get_owners_id(email)
    #             return redirect(url_for('admin'))
    #         else:
    #             flash('Invalid login credentials', 'danger')
    #             return redirect(url_for('owner_login'))
    #     else:
    #         flash('Invalid login credentials', 'danger')
    #         return redirect(url_for('owner_login'))
    # # except Exception as e:
    #     # print(e)
    return render_template('login.html')


@app.route('/logout',methods=['POST','GET'])
def logout():
    session.clear()
    return render_template('login.html')



# debug mode
if __name__ == "__main__":
    app.run(debug=True)
