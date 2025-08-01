import sys
import os  
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer ## for the missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformerConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformerConfig()

   ## Below fuction is created just create all pickle files which is responsible for converting 
   #   categoricla to numerical while performing the One Hot encoder and Standard scaling
      
    def get_data_transformer_object(self) :

        try:
            numerical_Columns = ["writing_score","reading_score"]
            categorical_columns = [
              "gender",
              "race_ethnicity",
               "parental_level_of_education",
               "lunch",
               "test_preparation_course"
            ]
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]

            )
            cat_pipeline = Pipeline(
                steps=[
                     ("imputer",SimpleImputer(strategy="most_frequent")),
                     ("onehotencoder",OneHotEncoder()),
                     ("scaler",StandardScaler(with_mean = False))

                ]
            )
              
            logging.info("Numerical columns standard scaling completed")
            logging.info("Categorical columns encoding completed")


            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_Columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_tranformation(self,train_path,test_path):
        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and the test data cpmpletely")
            logging.info("Obtaining the preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = "math_score"
            numerical_Columns = ["writing_score","reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info( f"Applying preprocessing object on training dataframe and testing dataframe " )

            input_feature_train_arr= preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr= preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object")
        
            save_object(
             file_path = self.data_transformation_config.preprocessor_obj_file_path,
             obj = preprocessing_obj

            )

            return( 
            train_arr,
            test_arr,
            )

        

        except Exception as e :
          
           raise CustomException(e,sys)
       