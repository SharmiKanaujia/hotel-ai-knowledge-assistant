
# HTTP API for Hotel AI Copilot
resource "aws_apigatewayv2_api" "app" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}

# Forward requests to our existing Lambda function
resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.app.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.app.invoke_arn
  payload_format_version = "2.0"
}

# Catch all paths and HTTP methods; require IAM authentication
resource "aws_apigatewayv2_route" "default" {
  api_id             = aws_apigatewayv2_api.app.id
  route_key          = "$default"
  target             = "integrations/${aws_apigatewayv2_integration.lambda.id}"
  authorization_type = "AWS_IAM"
}

# Deploy route changes automatically
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.app.id
  name        = "$default"
  auto_deploy = true

  default_route_settings {
    throttling_burst_limit = 5
    throttling_rate_limit  = 2
  }

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}

# Allow only this API Gateway to invoke our Lambda function
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.app.execution_arn}/*/*"
}

output "api_gateway_url" {
  description = "IAM-protected HTTPS endpoint for Hotel AI Copilot"
  value       = aws_apigatewayv2_api.app.api_endpoint
}
