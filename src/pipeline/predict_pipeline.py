import sys
import os
import pandas as pd

from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass


    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join("artifacts","preprocessor.pkl")
            print("Before load")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("after loading")
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)

            return preds
        
        except Exception as e:
            raise CustomException(e,sys)
            


class CustomData:
    def __init__(self,Name:str,Age:int,Sex:str,BP:str,Cholesterol:str,Na_to_K:float):

        self.Name=Name
        self.Age=Age
        self.Sex=Sex
        self.BP=BP
        self.Cholesterol=Cholesterol
        self.Na_to_K= Na_to_K


    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict={
                "Name":[self.Name],
                "Age":[self.Age],
                "Sex":[self.Sex],
                "BP":[self.BP],
                "Cholesterol":[self.Cholesterol],
                "Na_to_K":[self.Na_to_K]
            }
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e,sys)






