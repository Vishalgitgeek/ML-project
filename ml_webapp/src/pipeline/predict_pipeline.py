import sys
import pickle
import pandas as pd
from src.exception import Custom_Exception
from src.logger import logging
from src.paths import BEST_MODEL_PATH, PREPROCESSOR_PATH

class PredictPipeline:
    def __init__(self):
        try:
            self.model_path = BEST_MODEL_PATH
            self.preprocessor_path = PREPROCESSOR_PATH
        except Exception as e:
            raise Custom_Exception(e, sys)

    def predict(self, input_data):
        """
        input_data: Can be a Pandas DataFrame or a dictionary.
        """
        try:
            logging.info("Loading preprocessor and model...")

            # Ensure input_data is a DataFrame
            if not isinstance(input_data, pd.DataFrame):
                input_data = pd.DataFrame(input_data)

            # Load the preprocessor
            with open(self.preprocessor_path, 'rb') as f:
                preprocessor = pickle.load(f)

            # Load the model
            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)

            logging.info("Preprocessing input data...")
            input_transformed = preprocessor.transform(input_data)

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

