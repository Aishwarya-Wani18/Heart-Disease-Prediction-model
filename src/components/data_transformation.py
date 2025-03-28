import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from exception import CustomeException
from logger import logging
import os

from utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifact', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This Function is responsible for Data Transformation.
        '''
        try:
            numerical_col = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')), # Handle missing values
                    ("scaler",StandardScaler())  ## Perform Standard Scaling
                ]
            )
            logging.info(f'Numericals Columns : {numerical_col}')

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline,numerical_col)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomeException(e,sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
        
            logging.info('Read Train and Test Data Completed')
            logging.info('Obtaining Preprocessing Object. ')

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = 'target'
            numerical_columns = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal','target']
            
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            print(input_feature_train_df)

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f'Applying Preprocessing object on training dataframe and Testing Dataframe. '
            )
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info(f'Saved Preprocessing object. ')
            
            save_object (
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
              )
        
        except Exception as e:
            raise CustomeException(e,sys)

if __name__ == "__main__":
    from src.components.data_ingestion import DataIngestion
    obj = DataIngestion()
    train_data, test_data= obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)
