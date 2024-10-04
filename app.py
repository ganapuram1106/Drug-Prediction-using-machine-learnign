from flask import Flask,request,render_template
import sys
import os

import numpy as np
import pandas as pd

from src.pipeline.predict_pipeline import CustomData,predictPipeline
from sklearn.preprocessing import StandardScaler


web_application=Flask(__name__)
app=web_application

@app.route('/')

def index():
    return render_template('index,html')


@app.route('/predict', methods=['GET','POST'])

def predict():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            Age=request.form.get('Age'),
            Sex=request.form.get('Sex'),
            BP=request.form.get('BP'),
            Cholesterol=request.form.get('Cholesterol'),
            Na_to_K=request.form.get('Na_to_K')
        )


        pred_df=data.get_data_as_dataframe()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=predictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0")       