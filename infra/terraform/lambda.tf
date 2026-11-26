
# AWS Lambda function running our Hotel AI Copilot Docker image
resource "aws_lambda_function" "app" {
  function_name = var.project_name
  description   = "Hotel AI Copilot FastAPI application"

  package_type = "Image"

  image_uri = "${aws_ecr_repository.app.repository_url}:lambda-fa66273-fixed"

  role = aws_iam_role.lambda_execution.arn

  architectures = ["x86_64"]
  memory_size   = 1024
  timeout       = 30

  environment {
    variables = {
      AWS_LWA_PORT    = "8000"
      ENABLE_LIVE_RAG = "true"
      ENABLE_DEMO_RAG = "false"
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_logging,
    aws_cloudwatch_log_group.lambda
  ]

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}

output "lambda_function_name" {
  description = "Name of the Hotel AI Copilot Lambda function"
  value       = aws_lambda_function.app.function_name
}
