variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
  default     = "ca-central-1"
}

variable "project_name" {
  description = "Project prefix for naming AWS resources"
  type        = string
  default     = "finance-tracker"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance type for backend"
  type        = string
  default     = "t2.micro"
}

variable "frontend_bucket_name" {
  description = "Unique bucket name for frontend hosting"
  type        = string
  default     = "finance-tracker-frontend-bucket"
}
