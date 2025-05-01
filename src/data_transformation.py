import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from exception import CustomException
from logger import logging
from utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = [f"feature_{i}" for i in range(20)]
            num_pipeline = Pipeline(steps=[("scaler", StandardScaler())])
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", num_pipeline, numerical_columns),
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, val_path: str) -> tuple[np.ndarray, np.ndarray, str]:
        try:
            train_df = pd.read_csv(train_path)
            val_df = pd.read_csv(val_path)
            logging.info("Loaded train and test datasets")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "target"
            input_features_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_features_val_df = val_df.drop(columns=[target_column_name], axis=1)
            target_feature_val_df = val_df[target_column_name]

            logging.info("Applying preprocessing to dataframes")
            input_features_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            input_features_val_arr = preprocessing_obj.transform(input_features_val_df)

            train_arr = np.c_[input_features_train_arr, target_feature_train_df.to_numpy()]
            val_arr = np.c_[input_features_val_arr, target_feature_val_df.to_numpy()]

            logging.info("Saving preprocessing object")
            save_object(
                self.data_transformation_config.preprocessor_obj_file_path,
                preprocessing_obj,
            )

            return (
                train_arr,
                val_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)