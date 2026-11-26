
# Allow Hotel AI Copilot Lambda to invoke Amazon Nova Lite
# in our Sydney AWS region only.

data "aws_iam_policy_document" "lambda_bedrock" {
  statement {
    sid    = "InvokeNovaLite"
    effect = "Allow"

    actions = [
      "bedrock:InvokeModel"
    ]

    resources = [
      "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.nova-lite-v1:0"
    ]
  }
}

resource "aws_iam_role_policy" "lambda_bedrock" {
  name   = "${var.project_name}-bedrock-invoke"
  role   = aws_iam_role.lambda_execution.id
  policy = data.aws_iam_policy_document.lambda_bedrock.json
}
