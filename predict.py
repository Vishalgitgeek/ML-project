import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline

if __name__ == "__main__":
    # Step 1: Create input data as a DataFrame
    input_data = {
        'gender': ['male'],
        'race/ethnicity': ['group A'],
        'parental level of education': ['bachelor\'s degree'],
        'lunch': ['standard'],
        'test preparation course': ['completed'],
        'reading score': [100],
        'writing score': [100]
    }

    input_df = pd.DataFrame(input_data)

    # Step 2: Pass data to prediction pipeline
    pipeline = PredictPipeline()
    prediction = pipeline.predict(input_df)

    # Step 3: Print the output
    print("Prediction Result:", prediction)

