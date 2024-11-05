from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app = application
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Gvrganga892014.@localhost:5432/drug_prediction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'drug'

db=SQLAlchemy(app)

class employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    hospital_code = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


    def __init__(self,emp_id,name,designation,hospital_code,password_hash):
        self.emp_id=emp_id
        self.name=name
        self.designation=designation
        self.hospital_code=hospital_code
        self.password_hash=password_hash
        
class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(50), db.ForeignKey('employee.emp_id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    bp = db.Column(db.String(20), nullable=False)
    cholesterol = db.Column(db.String(20), nullable=False)
    na_to_k = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, emp_id, age, sex, bp, cholesterol, na_to_k, result):
        self.emp_id = emp_id
        self.age = age
        self.sex = sex
        self.bp = bp
        self.cholesterol = cholesterol
        self.na_to_k = na_to_k
        self.result = result
   
with app.app_context():
    db.create_all()


# Route for the index page
@app.route('/')
def index():
    return render_template('index.html') 

# Route for predicting data
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('home2.html')
    else:
        # Retrieve form data and assign to variables
        age = int(request.form.get('age'))
        sex = request.form.get('sex')
        bp = request.form.get('bp')
        cholesterol = request.form.get('cholesterol')
        na_to_k = float(request.form.get('na_to_k'))

        # Prepare data for prediction
        data = CustomData(
            Age=age,
            Sex=sex,
            BP=bp,
            Cholesterol=cholesterol,
            Na_to_K=na_to_k
        )
        
        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        # Save the prediction result and details to the database
        new_history = PredictionHistory(
            emp_id=session['user_id'],  # Assuming 'emp_id' matches 'user_id' in the session
            age=age,
            sex=sex,
            bp=bp,
            cholesterol=cholesterol,
            na_to_k=na_to_k,
            result=results[0]  # Assuming results[0] contains the prediction
        )
        db.session.add(new_history)
        db.session.commit()
        return redirect(url_for('history'))
# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        designation = request.form['designation']
        hospital_code = request.form['hospital_code']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if employee ID is already registered
        existing_user = employee.query.filter_by(emp_id=emp_id).first()
        if existing_user:
            flash('Employee ID already registered', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            # Hash the password and create a new Employee entry
            hashed_password = generate_password_hash(password)
            new_employee = employee(emp_id=emp_id, name=name, designation=designation,
                                    hospital_code=hospital_code, password_hash=hashed_password)
            db.session.add(new_employee)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        password = request.form['password']
        
        # Check if the employee exists
        user = employee.query.filter_by(emp_id=emp_id).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.emp_id
            flash('Login successful.', 'success')
            return redirect(url_for('history'))
        else:
            flash('Invalid employee ID or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/history')
def history():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    history_records = PredictionHistory.query.filter_by(emp_id=user_id).order_by(PredictionHistory.timestamp.desc()).all()
    
    return render_template('history.html', history_records=history_records)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
