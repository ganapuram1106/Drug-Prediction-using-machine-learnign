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
        
    
with app.app_context():
    db.create_all()


# Route for the index page
@app.route('/')
def index():
    return render_template('index.html') 

# Route for predicting data
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('home2.html')
    else:
        data = CustomData(
            Age=int(request.form.get('age')),
            Sex=request.form.get('sex'),
            BP=request.form.get('bp'),
            Cholesterol=request.form.get('cholesterol'),
            Na_to_K=float(request.form.get('na_to_k'))
        )
        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        return render_template('home2.html', results=results[0])

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
            return redirect(url_for('predict_datapoint'))
        else:
            flash('Invalid employee ID or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
