output "api_url" {
  value = aws_api_gateway_deployment.rest_api_deployment.invoke_url
}

output "predictor_lambda_ecr_repo_url" {
  value = aws_ecr_repository.predictor_lambda_repo.repository_url
}