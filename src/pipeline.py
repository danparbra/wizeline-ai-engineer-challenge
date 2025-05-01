"""Prediction pipeline"""

import sys
import pandas as pd
from exception import CustomException
from utils import load_object
from logger import logging


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        # Load blind test data
        test_df = pd.read_csv('artifacts/blind_test_data.csv')
        
        # Initialize prediction pipeline
        predict_pipeline = PredictPipeline()
        
        # Make predictions
        predictions = predict_pipeline.predict(test_df)
        
        # Save predictions
        results_df = pd.DataFrame({'predicted_target': predictions})
        results_df.to_csv('artifacts/predictions.csv', index=False)
        logging.info("Predictions saved successfully")
        
    except Exception as e:
        raise CustomException(e, sys)
