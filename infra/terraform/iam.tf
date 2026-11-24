# Trust policy: only AWS Lambda can assume this role
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Execution role for our Hotel AI Copilot Lambda function
resource "aws_iam_role" "lambda_execution" {
  name               = "${var.project_name}-lambda-execution"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}

# Allow Lambda to write logs to CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_basic_logging" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}