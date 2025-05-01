variable "aws_region" {
    type = string
    default = "us-east-1"
}

variable "aws_account_id" {
    type = string
}

variable "ecr_repo_name" {
    type = string
    default = "ecr_predictor_lambda_repo"
}

variable "build_and_push_docker_images" {
    type = bool
    default = true
}

variable "ecr_image_tag" {
    type = string
    default = "latest"
}
