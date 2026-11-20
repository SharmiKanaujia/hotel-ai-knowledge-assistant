
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
  region = var.aws_region
}

output "project_name" {
  value = var.project_name
}

output "aws_region" {
  value = var.aws_region
}
