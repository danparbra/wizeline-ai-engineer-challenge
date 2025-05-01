import json
import os
import pandas as pd
import boto3
from typing import Dict, Any
from pipeline import PredictPipeline
from logger import get_logger

logger = get_logger(__name__)
s3_client = boto3.client('s3')

def process_csv_file(bucket: str, key: str) -> str:
    """Process CSV file from S3 for bulk predictions and return output in file location"""
    try:
        # Download CSV from S3
        local_input_path = '/tmp/input.csv'
        local_output_path = '/tmp/predictions.csv'
        os.makedirs(os.path.dirname(local_input_path), exist_ok=True)
        s3_client.download_file(bucket, key, local_input_path)
        
        # Read CSV
        df = pd.read_csv(local_input_path)
        
        # Make predictions
        pipeline = PredictPipeline()
        predictions = pipeline.predict(df)
        
        # Save predictions
        results_df = pd.DataFrame({'target_pred': predictions})
        results_df.to_csv(local_output_path, index=False)
        
        # Upload results back to S3
        output_key = f"predictions/{os.path.basename(key)}"
        s3_client.upload_file(local_output_path, bucket, output_key)
        
        return output_key
        
    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}")
        raise

def handle_single_prediction(body: Dict[str, Any]) -> Dict[str, Any]:
    """Handle single prediction request"""
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([body])
        
        # Make prediction
        pipeline = PredictPipeline()
        prediction = pipeline.predict(input_df)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'target_pred': float(prediction[0])
            })
        }
    except Exception as e:
        logger.error(f"Error in single prediction: {str(e)}")
        raise

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda function handler"""
    try:
        # Check if this is an S3 event
        if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:s3':
            # Handle bulk processing
            record = event['Records'][0]['s3']
            bucket = record['bucket']['name']
            key = record['object']['key']
            
            output_key = process_csv_file(bucket, key)
            logger.info(f"Predictions saved to: s3://{bucket}/{output_key}")

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Bulk prediction processing completed',
                    'output_location': f's3://{bucket}/{output_key}'
                })
            }
            
        # Handle API Gateway request
        elif 'body' in event:
            body = json.loads(event['body'])
            return handle_single_prediction(body)
            
        else:
            logger.exception("Invalid event type")
            raise ValueError("Invalid event type")
            
    except Exception as e:
        logger.exception(f"Error in lambda_handler: {str(e)}")
        raise