
terraform {
  required_version = ">= 1.17.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

# Dedicated storage for Terraform state
resource "aws_s3_bucket" "terraform_state" {
  bucket_prefix = "hotel-ai-copilot-tfstate-"

  tags = {
    Project     = "hotel-ai-copilot"
    Environment = "dev"
    Purpose     = "terraform-state"
  }

  lifecycle {
    prevent_destroy = true
  }
}
