ifneq (,$(wildcard ./.env))
	include .env
	export
endif

# Default values for required variables
AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --query Account --output text)
AWS_REGION ?= us-east-1
ECR_REPO_NAME ?= ecr_predictor_lambda_repo
IMAGE_NAME ?= $(ECR_REPO_NAME)

BASE_ECR_URL = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
ECR_URL = $(BASE_ECR_URL)/$(ECR_REPO_NAME)

.PHONY: build-docker push-docker create-ecr-repo update-lambda

# Build Docker image
build-docker:
	docker build --platform=linux/amd64 --provenance=false -t $(IMAGE_NAME) .

# Tag and push Docker image to ECR
push-docker:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(BASE_ECR_URL)
	docker tag $(IMAGE_NAME):latest $(ECR_URL):latest
	docker push $(ECR_URL):latest

# Create ECR repository (if it doesn't exist)
create-ecr-repo:
	aws ecr describe-repositories --repository-names $(ECR_REPO_NAME) --region $(AWS_REGION) || aws ecr create-repository --repository-name $(ECR_REPO_NAME) --region $(AWS_REGION)

# Update Lambda function
update-lambda:
	AWS_PAGER="" aws lambda update-function-code --function-name $(LAMBDA) --image-uri $(ECR_URL):latest

# Combined tasks
build-and-push: build-docker push-docker