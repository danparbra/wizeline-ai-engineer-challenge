resource "aws_ecr_repository" "predictor_lambda_repo" {
  name = var.ecr_repo_name
  force_delete = true
}