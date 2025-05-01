ifneq (,$(wildcard ./.env))
    include .env
    export
endif

BASE_ECR_URL=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
ECR_URL=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPO_NAME)
FOLDER ?= .

# Logging function
info:
@echo "[$(shell date '+%Y-%m-%d %H:%M:%S')] $(1)"

# Build Docker image
build-docker:
$(call info, "Building Docker image...")
cd $(FOLDER) && docker build --platform=linux/amd64 --provenance=false -t $(IMAGE_NAME) .

# Tag and push Docker image to ECR
push-docker:
$(call info, "Authenticating with AWS ECR...")
-aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
$(call info, "Tagging Docker image...")
docker tag $(IMAGE_NAME):latest $(ECR_URL):latest
$(call info, "Pushing Docker image to ECR...")
docker push $(ECR_URL):latest
$(call info, "Docker image pushed successfully.")

# Create ECR repository (if it doesn't exist)
create-ecr-repo:
$(call info, "Creating ECR repository if it doesn't exist...")
aws ecr describe-repositories --repository-names $(ECR_REPO_NAME) --region $(AWS_REGION) || aws ecr create-repository --repository-name $(ECR_REPO_NAME) --region $(AWS_REGION)

# Terraform plan
terraform-plan:
$(call info, "Running Terraform plan...")
cd $(TERRAFORM_DIR) && terraform plan

# Terraform apply
terraform-apply:
$(call info, "Running Terraform apply...")
cd $(TERRAFORM_DIR) && terraform apply

update-lambda:
$(call info, "Updating Lambda function with new Docker image...")
AWS_PAGER="" aws lambda update-function-code --function-name $(LAMBDA) --image-uri $(ECR_URL):latest
$(call info, "Lambda function updated successfully.")

# Main tasks
build-and-push-docker-update-lambda: build-docker push-docker update-lambda

build-and-push-error-notifier-update-lambda: build-error-notifier push-error-notifier update-error-notifier-lambda

# UAT Deploy
terraform-deploy:
$(call info, "Deploying to UAT environment...")
cd terraform && terraform apply

# UAT Deploy
uat-deploy:
$(call info, "Deploying to UAT environment...")
cd terraform && terraform workspace select uat && terraform apply

# PROD Deploy
prod-deploy:
$(call info, "Deploying to PROD environment...")
cd terraform && terraform workspace select prod && terraform apply
