from flask import Flask, render_template, url_for, session, redirect, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
import os


lab_id = 0
transaction_id = 0

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
    # try:       
    #     return render_template('reception.html')
    # except:
    return render_template('reception.html')

@app.route('/reception/search-patient')
def r_search():
    return render_template('search_patient.html')


@app.route('/search_patient',methods=['POST','GET'])
def search_patient():
    if request.method == 'POST':
        try:
            name = request.form['name']
            print(name)        
            session['searchpatient_record'] = name
            return redirect(url_for('searched'))
        except:
            flash("error retreiving the record","danger")
            return render_template('search_patient.html')         
    else:
        return render_template('search_patient.html')

@app.route('/searched')
def searched():
    name = session['searchpatient_record']
    
    try:
        patient = patients.select_patient_by_name(name)
        return render_template('search_patient.html',patient = patient)
    except:
        flash("error retreiving the record","danger")
        return render_template('search_patient.html')        
        
# @app.route('/try')
# def try_search():
#     name = "Newton Mathenge"
#     seache = patients.select_patient_by_name(name)
#     for each in seache:
#         print(each.id)
#         print(each.name)
#         print(each.contact)
#         print(each.age)
#     return f'correct'

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

        #patient = patients.select_patient_by_name(name)
        return render_template('reception.html')
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

    
@app.route('/searchpage')
def searchpage():
    return render_template('searchpage.html')


@app.route('/lab-session')
def request_lab_session():
    return render_template('lab.doc.html')


@app.route('/send-tests')
def request_laboratory_session():
    return render_template('lab.doc.html')

@app.route('/doctor/home')
def doc_dash():
    try:
        session = patient_session.active_session()
        for ses in session:
            id = ses.patient
        name = patients.select_patient_by_id(id)
        for each in name:
            mn = each.name
        return render_template("doctor'sdash.html",sessions = session,name = mn)
    except:
        return render_template("doctor'sdash.html")

@app.route('/doc/patient/load/<int:id>',methods=['POST','GET'])
def doctor_patient_load(id):
    session['patients_id'] = id
    return redirect(url_for('doc_active_dash'))

@app.route('/active/new')
def doc_active_dash_error():
    flash("no prior medical records","danger")
    return render_template('doc.activesession.html')

@app.route('/doctor/active')
def doc_active_dash():
    id = session['patients_id']
    session['treatment_p_id'] = id
    record = medical_records.get_patient_record_by_id(id)
    if record:        
        name = patients.select_patient_by_id(id)
        for each in name:
            mn = each.name      
        return render_template('doc.activesession.html',record = record,name = mn)
    else:
        return redirect(url_for('doc_active_dash_error'))


@app.route('/doctor/treatment',methods=['POST','GET'])
def treatment_doc():    
    symptom = request.form['symptoms']
    session['symptoms'] = symptom
    diagnosis = request.form['diagnosis']
    session['diagnosis'] = diagnosis
    deduction = request.form['deductions']
    id = session['treatment_p_id']
    name = patients.select_patient_by_id(id)
    for each in name:
        mn = each.name    
    return render_template('doc.treatment.html',name = mn,symptoms = symptom,deductions=deduction )   
    

@app.route('/checkout',methods=['POST','GET'])
def checkout():
    prescription = request.form['prescription']
    patient = session['treatment_p_id']
    symptoms = session['symptoms']
    diagnosis = session['diagnosis']
    date = datetime.date.today()
    newrecord = medical_records(patient = patient,symptomps = symptoms,diagnosis = diagnosis,
                                treatment = prescription,date = date)
    newrecord.insert_record()
    patient_session.update_session_by_id(patient)
    return redirect(url_for('doc_dash'))


@app.route('/doctor/search-patient')
def doc_search_patient():
    return render_template('doc.searchpatient.html')

@app.route('/cashier/home')
def cashier_dash():
    return render_template('transactions.html')
    

@app.route('/cashier/transactions/<int:id>')
def transactions(id):
    print(id)
    session['transactionID'] = id
    return redirect(url_for('cashier_transaction'))

@app.route('/cashier/transaction')
def cashier_transaction():
    id = session['transactionID']
    try:
        pname = patients.select_patient_by_id(id)
        patient = billing.get_record_by_p_id(id)
        return render_template('cashier.html',patient = patient
                            ,patientname = pname)
    except:
        flash("an error occured","danger")
        return render_template('transactions.html')   
    
    
    
@app.route('/lab/que')
def lab_que():
    status = "pending"
    mytests = tests.view_tests_by_status(status)
    return render_template('lablist.html',thetests = mytests)

@app.route('/lab/home/<int:id>')
def lab_session(id):     
    session['lab_id'] = id
    return redirect(url_for('lab_redirect'))

@app.route('/lab/redirect')
def lab_redirect():
    id = session['lab_id']
    try:
        test = tests.view_tests_by_patient(id)
        con = patients.select_patient_by_id(id)
        return render_template('lab_session.html',test = test,mycon = con )
    except:
        flash("an error occured try again later","danger")
        return render_template('lablist.html')

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
