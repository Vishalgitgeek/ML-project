import os
import sys
import pandas as pd
import numpy as np
import pickle

from src.exception import Custom_Exception
from src.logger import logging

class PredictPipeline:
    def __init__(self):
        try:
            self.model_path = os.path.join('artifacts', 'best_model.pkl')
            self.preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
        except Exception as e:
            raise Custom_Exception(e, sys)

    def predict(self, input_df):
        try:
            logging.info("Loading preprocessor and model...")

            # Load the preprocessor
            with open(self.preprocessor_path, 'rb') as f:
                preprocessor = pickle.load(f)

            # Load the model
            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)

            logging.info("Preprocessing input data...")
            input_transformed = preprocessor.transform(input_df)

            logging.info("Generating prediction...")
            prediction = model.predict(input_transformed)

            return prediction

        except Exception as e:
            raise Custom_Exception(e, sys)
        


# to print column name of preprocessor
# Uncomment the following lines to print the feature names of the preprocessor
# with open('artifacts/preprocessor.pkl', 'rb') as f:
#     preprocessor = pickle.load(f)

# print(preprocessor.feature_names_in_)

