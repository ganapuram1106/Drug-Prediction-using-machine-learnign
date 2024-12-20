import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

from src.utils import save_object,evaluate_models
from src.exception import CustomException
from src.logger import logging

@dataclass
class modeltrainerconfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class modelTrainer:

    def __init__(self):
        self.model_trainer_config=modeltrainerconfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("split training and test test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                
                "LogisticRegression":LogisticRegression(),
                "RandomForest":RandomForestClassifier(),
                "KNN":KNeighborsClassifier(),
                "SVM":SVC()

            }

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)

            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score<0.7:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)


            accuracy=accuracy_score(y_test,predicted)
            return accuracy 
           
            
              
        except Exception as e:
            raise CustomException(e,sys)
        