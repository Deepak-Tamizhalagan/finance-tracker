terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Random suffix so bucket name is globally unique
resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "finance_logs" {
  bucket = "finance-tracker-logs-${random_id.suffix.hex}"

  tags = {
    Project = "finance-tracker"
    Owner   = "Zafar"
    Env     = "dev"
  }
}

output "logs_bucket_name" {
  description = "Name of the S3 bucket created for logs"
  value       = aws_s3_bucket.finance_logs.bucket
}
