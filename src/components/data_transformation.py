import os 
import sys
from dataclasses import  dataclass

import pandas as pd 
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.logger import logging
from src.exception import CustomException

from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()


    def get_data_transformer_object(self):

        try:
            numerical_columns=["Age","Na_to_K"]
            categorical_columns=["BP","Sex","Cholesterol"]

            categories = [
                ['male', 'female'],           # Sex categories
                ['low', 'normal', 'high'],    # BP categories
                ['normal', 'high']             # Cholesterol categories
            ]

            num_pipeline=Pipeline(
                steps=[
                    ('scaler',StandardScaler()),
                    ('imputer',SimpleImputer(strategy="median"))
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ("label",OneHotEncoder(handle_unknown="ignore")),
                ]
            )
            logging.info(f"Categorical columns:{categorical_columns}")
            logging.info(f"Numerical columns:{numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="Drug"
            numerical_columns=["Age","Na_to_K"]
           

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(f"applying preprocessing object on training df and testing df.")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)


            
            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df) ]

            test_arr=np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("saved preprocessing object")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
