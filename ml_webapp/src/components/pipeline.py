from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging

if __name__=="__main__":

    # 1. data ingestion
    logging.info("Starting the data ingestion process...")
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    logging.info("Data ingestion completed successfully.")

    # 2. data transformation
    logging.info("Starting the data transformation process...")
    data_transformation = DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)
    logging.info("Data transformation completed successfully.")

    # 3. model training
    logging.info("Starting the model training process...")
    ModelTrainer = ModelTrainer()
    best_model_name, model_report = ModelTrainer.initiate_model_trainer(train_arr, test_arr)

    print(f"Best model: {best_model_name}")
    print("Model report:", model_report)

    logging.info("Model training completed successfully.")