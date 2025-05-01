# Wizeline AI Engineer Challenge

## Overview
This project implements an end-to-end machine learning pipeline for multivariate regression predictions. It includes data preprocessing, model training, and basic deployment capabilities through AWS Lambda for real-time bulk and single point predictions. The solution is containerized and can be deployed as a serverless application.

## Project Structure
```
wizeline-ai-engineer-challenge/
├── artifacts/               # Stored model artifacts and preprocessors
├── containers/             
│   └── lambda_predictor/   # Lambda function for predictions
├── src/
│   ├── data_transformation.py  # Data preprocessing pipeline
│   ├── model_trainer.py        # Model training implementation
│   ├── utils.py               # Helper functions
│   ├── logger.py             # Logging configuration
│   └── exception.py          # Custom exception handling
└── README.md
```

## Architecture
For the deployment, the applications is served as a backend services in AWS.

1. **Training Pipeline**:
   - Data preprocessing using sklearn Pipeline and ColumnTransformer
   - Model training with hyperparameter tuning
   - Artifact storage for model and preprocessor objects

2. **Prediction Service**:
   - AWS S3 to receive bulk prediction requests
   - AWS API Gateway as the entry point single point prediction requests
   - AWS Lambda function for serverless predictions
   - Amazon ECR for container image storage
   - Model artifacts packaged within container

### Workflow
1. Client either sends single point prediction request to REST API in API Gateway, or
2. Client dumps CSV file in S3 bucket for bulk prediction requests.
2. API Gateway triggers Lambda function
3. Lambda loads preprocessor and model
4. Prediction is processed and returned
5. Response is sent back through API Gateway

## Usage

### Prerequisites
- Python 3.11+
- uv

### Local Development
1. Clone the repository:
```bash
git clone https://github.com/danparbra/wizeline-ai-engineer-challenge
cd wizeline-ai-engineer-challenge
```

2. Set up Python virtual environment:
```bash
uv venv --python 3.11
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
uv sync
```

4. Run the training pipeline:
```bash
uv run src/model_trainer.py
```

### Making Predictions

To make predictions using the local training pipeline (this will predict for all the data points in the `blind_test_data.csv` file):
```bash
uv run src/pipeline.py
```
To make single point predictions using the deployed service in AWS:
```bash
curl -X POST https://fpzixt1flh.execute-api.us-east-1.amazonaws.com/default/submit \
  -H "Content-Type: application/json" \
  -d '{"feature_1": value_1, "feature_2": value_2, ...}'
# Or using Postman for a request to a REST API using the above URL and example payload
```
Alternatively a CSV file can be saved into the deployed S3 bucket to make bulk predictions. The predictions will be saved in a different folder.

## Improvements

### Technical Enhancements
1. **Model Monitoring**:
   - Implement drift detection
   - Add performance monitoring
   - Set up automated retraining triggers

2. **MLOps Pipeline**:
   - Enhance CI/CD pipeline for continuous retraining on a timely basis or on a data availability basis
   - Version control for model artifacts

3. **Scalability**:
   - Add batch prediction capability
   - Implement caching for frequent predictions
   - Add auto-scaling policies

### Bulk Prediction Strategy
For regular bulk predictions, I recommend implementing:

1. **Scheduled Processing**:
   - Implement AWS Batch for large-scale predictions
   - Store prediction results in Amazon S3 for further analysis

2. **Data Pipeline**:
    - Implement SageMaker-managed or Databricks-managed workflow for the Data Science training steps.
   - Implement data quality checks

3. **Monitoring and Maintenance**:
   - Set up CloudWatch alerts
   - Implement automated backup strategy
   - Create dashboard for prediction metrics