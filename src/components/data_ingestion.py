import os
import sys
from exception import CustomeException
from logger import logging
import pandas as pd
from sklearn .model_selection import train_test_split
from dataclasses import dataclass

@dataclass
# using dataclass decorator we will be able to define class variable.
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifact', 'train.csv')
    test_data_path: str=os.path.join('artifact', 'test.csv')
    raw_data_path: str=os.path.join('artifact', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered the Data ingestion method or component')
        try:
            df = pd.read_csv('heart.csv')
            logging.info('Read the Dataset as Dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.train_data_path, index=False,header=True)
            
            logging.info('train test split initiated')
            train_set, test_set = train_test_split(df,test_size=0.2,random_state=0)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header = True)

            logging.info('Ingestion of the data is completed')
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                self.ingestion_config.raw_data_path
            )
        except Exception as e:
            raise(CustomeException(e,sys))


if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()