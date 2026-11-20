
# Storage for future Hotel AI Copilot assets
resource "aws_s3_bucket" "project_assets" {
  bucket_prefix = "hotel-ai-copilot-assets-"

  tags = {
    Project     = var.project_name
    Environment = "dev"
  }
}

# Prevent public access to our bucket
resource "aws_s3_bucket_public_access_block" "project_assets" {
  bucket = aws_s3_bucket.project_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
