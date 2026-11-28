
variable "project_name" {
  description = "Name of our Hotel AI Copilot project"
  type        = string
  default     = "hotel-ai-copilot"
}

variable "aws_region" {
  description = "AWS region used by our project"
  type        = string
  default     = "ap-southeast-2"
}

variable "monthly_budget_limit_usd" {
  description = "Monthly AWS cost budget limit in USD"
  type        = number
  default     = 10

  validation {
    condition     = var.monthly_budget_limit_usd > 0
    error_message = "monthly_budget_limit_usd must be greater than 0."
  }
}

variable "budget_alert_email" {
  description = "Email address that receives AWS Budgets cost alerts. Set it in an untracked tfvars file or TF_VAR_budget_alert_email."
  type        = string

  validation {
    condition     = can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", var.budget_alert_email))
    error_message = "budget_alert_email must be a valid email address."
  }
}
