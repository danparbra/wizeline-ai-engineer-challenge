import os
import sys
from dataclasses import dataclass
import pandas as pd
from exception import CustomException
from sklearn.model_selection import train_test_split
from logger import logging


@dataclass
class DataIngestionConfig:
    val_data_path: str = os.path.join("artifacts", "validation.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    raw_data_path: str = os.path.join("artifacts", "training_data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()


    def initiate_data_ingestion(self):
        logging.info("Started the data ingestion process")
        try:
            # Use proper path
            df = pd.read_csv(self.ingestion_config.raw_data_path)
            logging.info("Raw dataset read successfully")

            # Create data directories if they do not exist
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True
            )
            os.makedirs(
                os.path.dirname(self.ingestion_config.val_data_path), exist_ok=True
            )

            # Split the dataset into train and validation sets
            logging.info("Splitting dataset into train and validation sets")
            train_set, val_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            val_set.to_csv(
                self.ingestion_config.val_data_path, index=False, header=True
            )
            logging.info("Train-validation split completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.val_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    ingestion = DataIngestion()
    train_data_path, test_data_path = ingestion.initiate_data_ingestion()
    print(f"Train data path: {train_data_path}")
    print(f"Validation data path: {test_data_path}")