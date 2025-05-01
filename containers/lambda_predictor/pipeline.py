"""Prediction pipeline"""

import os
import sys
import pandas as pd
import numpy as np
from exception import CustomException
from utils import load_object
from logger import get_logger

logger = get_logger(__name__)

class PredictPipeline:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "artifacts", "model.pkl")
        self.preprocessor_path = os.path.join(os.path.dirname(__file__), "artifacts", "preprocessor.pkl")

    def validate_features(self, features: pd.DataFrame) -> bool:
        """Validate that input features match expected format"""
        expected_features = [f"feature_{i}" for i in range(20)]
        return all(col in features.columns for col in expected_features)

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        try:
            logger.info("Starting prediction pipeline")
            
            if not self.validate_features(features):
                logger.error("Input features validation failed")
                raise ValueError("Input features do not match expected format")

            logger.info("Loading model and preprocessor")
            model = load_object(file_path=self.model_path)
            preprocessor = load_object(file_path=self.preprocessor_path)
            
            logger.info("Transforming features")
            data_scaled = preprocessor.transform(features)
            
            logger.info("Making predictions")
            preds = model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e, sys)
