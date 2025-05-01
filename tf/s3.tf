resource "aws_s3_bucket" "artifacts_bucket" {
  bucket = "wl-prediction-artifacts"
  force_destroy = true
}

# Adding S3 bucket as trigger to predictor lambda
resource "aws_s3_bucket_notification" "predictor_lambda_trigger" {
  bucket = aws_s3_bucket.artifacts_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.uploader_function.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_permission" "uploader_lambda_permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.uploader_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.artifacts_bucket.id}"
}
