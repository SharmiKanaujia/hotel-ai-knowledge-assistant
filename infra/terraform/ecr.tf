
# Private Docker image repository for Hotel AI Copilot
resource "aws_ecr_repository" "app" {
  name                 = var.project_name
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}

# Display the repository URL after deployment
output "ecr_repository_url" {
  description = "ECR repository URL for the application Docker image"
  value       = aws_ecr_repository.app.repository_url
}
