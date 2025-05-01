resource "aws_lambda_function" "uploader_function" {
  function_name = "wl-predictor-lambda"
  role          = aws_iam_role.predictor_lambda_role.arn
  timeout       = 600
  memory_size   = 2048
  image_uri     = "${aws_ecr_repository.predictor_lambda_repo.repository_url}:${var.ecr_image_tag}"
  package_type  = "Image"

  depends_on = [null_resource.push_uploader_lambda_image]
}

resource "null_resource" "push_uploader_lambda_image" {
  count = var.build_and_push_docker_images ? 1 : 0
  provisioner "local-exec" {
    command = "make -C ../containers/lambda_predictor build-docker && make -C ../containers/lambda_predictor push-docker"
  }
  depends_on = [aws_ecr_repository.predictor_lambda_repo]
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn        = aws_sqs_queue.requests_api_queue.arn
  function_name           = aws_lambda_function.uploader_function.arn
  enabled                 = true
  function_response_types = ["ReportBatchItemFailures"]
}

resource "aws_lambda_permission" "allows_sqs_to_trigger_lambda" {
  statement_id  = "AllowExecutionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.uploader_function.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = aws_sqs_queue.requests_api_queue.arn
}

resource "aws_iam_role" "predictor_lambda_role" {
  name               = "predictor-lambda-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "predictor_lambda_policy" {
  name   = "predictor-lambda-policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:sqs:${var.aws_region}:${var.aws_account_id}:*"
    },
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "predictor_lambda_policy_attachment" {
  policy_arn = aws_iam_policy.predictor_lambda_policy.arn
  role       = aws_iam_role.predictor_lambda_role.name
}