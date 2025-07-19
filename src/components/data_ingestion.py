import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import os, sys
from src.logger import logging
from src.exception import Custom_Exception


@dataclass
class dataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path : str = os.path.join('artifacts', 'test.csv')
    raw_data_path : str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.DataIngestion_config = dataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("inside data ingestion")

        try:
            df = pd.read_csv('notebook/data/StudentsPerformance.xls')
            logging.info('exported csv dataset as dataframe')

            os.makedirs(os.path.dirname(self.DataIngestion_config.train_data_path), exist_ok= True)
            df.to_csv(self.DataIngestion_config.raw_data_path, index=False, header = True)
            logging.info('train test initiated')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=1)

            train_set.to_csv(self.DataIngestion_config.train_data_path, index=False, header = True)
            test_set.to_csv(self.DataIngestion_config.test_data_path, index=False, header = True)

            logging.info("ingestion of data is completed")

            return(
                self.DataIngestion_config.train_data_path,
                self.DataIngestion_config.test_data_path
            )
        except Exception as e:
            raise Custom_Exception(e, sys)
        
if __name__=="__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
            

    