from app import db

class users(db.Model):
    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)    
    password = db.Column(db.String(80), nullable=False)


    def insert_record(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def check_email_exist(cls, email):
        customer = cls.query.filter_by(email=email).first()
        if customer:
            return True
        else:
            return False

    @classmethod
    def validate_password(cls, email, password):
        customer = cls.query.filter_by(email=email).first()
        if customer and bcrypt.check_password_hash(customer.password, password):
            return True
        else:
            return False


class patients(db.Model):
    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String)
    condition = db.Column(db.String(200))
   


    def insert_record(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def check_patient(cls, name,contact):
        patient = cls.query.filter_by(name=name).first()
        if owners:
            contact = patient.contact
            if contact:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def select_patient_by_name(cls,name):
        returns = cls.query.filter_by(name = name)
        if returns:
            return returns
        else:
            return False
    
    @classmethod
    def select_patient_by_id(cls,id):
        returns = cls.query.filter_by(id = id)
        if returns:
            return returns
        else:
            return False
            
          

    @classmethod
    def get_patient_name(cls,id):
        patient = cls.query.filter_by(id = id).name
        if patient:
            return patient
        else:
            return False

class medical_records(db.Model):
    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    patient = db.Column(db.Integer, nullable=False)
    symptomps = db.Column(db.String(200))
    diagnosis = db.Column(db.String(200))
    treatment = db.Column(db.String(200))
    date = db.Column(db.Date)


    def insert_record(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def fetch_all(cls):
        return cls.query.all()

 
    @classmethod
    def fetch_by_date(cls,date):
        return cls.query.filter_by(date = date)

    
    @classmethod
    def get_patient_record_by_id(cls, id):
        record =  cls.query.filter_by(patient=id)
        if record:
            return record
        else:
            return False


class billing(db.Model):
    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    patient = db.Column(db.Integer,nullable = False)
    billing_item = db.Column(db.String, nullable=False)
    bill = db.Column(db.Integer,nullable = False)
    date = db.Column(db.Date, nullable =False)


    def insert_record(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    # view record by patient id
    @classmethod
    def get_record_by_p_id(cls, id):
        return cls.query.filter_by(patient=id).first()

     # view record by date
    @classmethod
    def get_record_by_date(cls, date):
        return cls.query.filter_by(date=date).first()




class drug_bank(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    category = db.Column(db.String(200),nullable = False)
    drug = db.Column(db.String,nullable= False)
    quantity = db.Column(db.Integer, nullable=False,default=0)


    def create_wallet(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def view_current_quantity(cls, drug):
        return cls.query.filter_by(drug=drug).first()


    @classmethod
    def update_drug_bank(cls, name, quantity):
        drug = cls.query.filter_by(drug = name).first()
        if drug:
            drug.quantity = quantity
            db.session.commit()
            return True
        return False



class prescriptions(db.Model):
    id = db.Column(db.Integer,nullable = False,
                unique = True,primary_key = True,autoincrement = True)
    patient = db.Column(db.Integer, nullable = False)
    drug_issued = db.Column(db.String(200),nullable = False)
    date = db.Column(db.Date)
    issued_by = db.Column(db.Integer)

   
    def new_prescription(self):
        db.session.add(self)
        db.session.commit()


    
    @classmethod
    def view_all(cls):
        records = cls.query.all()
        return records
    
   
    @classmethod
    def view_by_date(cls,date):
        records = cls.query.filter_by(date = date)
        return records

    #view by drug
    @classmethod
    def view_by_drug_name(cls,name):
        records = cls.query.filter_by(drug_issued = name)
        return records
        

    @classmethod
    def view_by_issuing_staff(cls,id):
        records = cls.query.filter_by(issued_by = id)
        return records


class restocks(db.Model):
    id = db.Column(db.Integer,nullable = False,
                primary_key = True, autoincrement = True)
    drug = db.Column(db.String,nullable = False)
    supplier = db.Column(db.String,nullable = False)
    date = db.Column(db.String,nullable = False)
    received_by = db.Column(db.Integer, nullable = False)


    
    def restock(self):
        db.session.all(self)
        db.session.commit()

 
    @classmethod
    def view_by_date(cls,date):
        record = cls.query.filter_by(date = date)
        return record
    
    
    @classmethod
    def view_by_drug(cls,drug):
        record = cls.query.filter_by(drug = drug)
        return record
    
   
    @classmethod
    def view_by_receiver(cls,receiver):
        record = cls.query.filter_by(received_by = receiver).first()
        return record

    @classmethod
    def view_by_supplier(cls,supplier):
        record = cls.query.filter_by(supplier = supplier)
        return record

class patient_session(db.Model):
    session_id =db.Column(db.Integer,autoincrement = True,nullable = False,primary_key = True)
    patient = db.Column(db.Integer,nullable = False)
    date = db.Column(db.Date,nullable = False)
    status = db.Column(db.String(30))
    start = db.Column(db.Time)
    end = db.Column(db.Time)


    def create_session(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def active_session(cls):
        actives = cls.query.filter_by(status = "active")
        return actives

    
    @classmethod
    def update_session_by_id(cls,id):
        session = cls.query.filter_by(patient = id).first()
        status = session.status
        while status == 'active':
            session.status = 'closed'
            db.session.commit()
            return True

class tests(db.Model):
    id = db.Column(db.Integer,autoincrement = True,primary_key=True)
    patient = db.Column(db.Integer)
    technician = db.Column(db.Integer)
    date = db.Column(db.Date)
    tests = db.Column(db.String(200))
    results = db.Column(db.String(200))
    deductions = db.Column(db.String(200))
    status = db.Column(db.String,default = "pending")


    def create_test(self):
        self.session.add(self)
        self.session.commit()

    @classmethod
    def view_tests_by_status(cls,status):
        return cls.query.filter_by(status = status)

    @classmethod
    def view_tests_by_patient(cls,patient):
        return cls.query.filter_by(patient = patient)

    @classmethod
    def view_tests_by_tests(cls,tests):
        return cls.query.filter_by(tests = tests)

    @classmethod
    def view_tests_by_date(cls,date):
        return cld.query.filter_by(date = date)

    @classmethod
    def view_tests_by_deductions(cls,deductions):
        return cld.query.filter_by(deductions = deductions)

    @classmethod
    def update_tests_by_id(cls,id):
        test = cls.query.filter_by(id = id).first()
        if test:
            newstatus = "closed"
            test.status = newstatus
            db.session.commit()
            return True
        else:
            return False
        