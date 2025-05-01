"""Prediction pipeline"""

import os
import sys
import pandas as pd
import numpy as np
from exception import CustomException
from utils import load_object
from logger import logging


class PredictPipeline:
    def __init__(self):
        self.model_path = os.path.join("artifacts", "model.pkl")
        self.preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")

    def validate_features(self, features: pd.DataFrame) -> bool:
        """Validate that input features match expected format"""
        expected_features = [f"feature_{i}" for i in range(20)]
        return all(col in features.columns for col in expected_features)

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        try:
            logging.info("Starting prediction pipeline")
            
            if not self.validate_features(features):
                raise CustomException("Input features do not match expected format", sys)

            logging.info("Loading model and preprocessor")
            model = load_object(file_path=self.model_path)
            preprocessor = load_object(file_path=self.preprocessor_path)
            
            logging.info("Transforming features")
            data_scaled = preprocessor.transform(features)
            
            logging.info("Making predictions")
            preds = model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        logging.info("Loading blind test data")
        test_df = pd.read_csv(os.path.join("artifacts", "blind_test_data.csv"))
        
        predict_pipeline = PredictPipeline()
        predictions = predict_pipeline.predict(test_df)
        
        logging.info("Saving predictions")
        results_df = pd.DataFrame({'target_pred': predictions})
        results_df.to_csv(os.path.join("artifacts", "predictions.csv"), index=False)
        logging.info("Predictions saved successfully")
        print("Predictions have been saved to artifacts/predictions.csv")
        
    except Exception as e:
        logging.error(f"Error in prediction pipeline: {str(e)}")
        raise CustomException(e, sys)
