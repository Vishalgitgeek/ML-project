import numpy as np
import pandas as pd

import sys
import os
from src.exception import Custom_Exception
from src.logger import logging

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.utils import save_object


class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'model.pkl')


class DataTransformation:
    def __init__(self):
        self.DataTransformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        # responsible for data transformation
        try:
            numerical_cols = ['reading score', 'writing score']
            categorical_cols = [
                'gender',
                'race/ethnicity',
                'parental level of education',
                'lunch',
                'test preparation course',
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )


            logging.info("categorical cols encoding completed...")
            logging.info("numerical cols standard scaling completed...")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_cols),
                    ("cat_pipeline", cat_pipeline, categorical_cols)
                ]
            )

            return preprocessor

        except Exception as e:
            raise Custom_Exception(e, sys)

    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)   

            logging.info("read train and test data completed....")
            logging.info("fetching preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column = 'math score'
            numerical_column = ['writing score', 'reading score']

            input_feature_train_df = train_df.drop(columns=[target_column], axis= 1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column], axis= 1)
            target_feature_test_df = test_df[target_column]

            logging.info("applying preprocessing object on training and testing dataframe")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info("preprocessing object on train and test applied succesfully")

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info(f"saved preprocessing object....")

            save_object(

                file_path = self.DataTransformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.DataTransformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise Custom_Exception(e, sys)