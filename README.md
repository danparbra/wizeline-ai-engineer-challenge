# wizeline-ai-engineer-challenge

Architecture Overview:

API Gateway: Exposes REST endpoint that accepts POST requests with feature data
Lambda Function: Loads model and preprocessor, makes predictions
ECR: Stores Docker image with model artifacts and dependencies
S3 (optional): Could store model artifacts if they're too large for Lambda

Service Flow:
Client sends POST request to API Gateway endpoint
API Gateway triggers Lambda function
Lambda loads model/preprocessor, processes input, returns prediction
API Gateway returns prediction to client