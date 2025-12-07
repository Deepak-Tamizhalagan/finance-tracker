##############################################
# Output Values for Documentation & Testing
##############################################

output "ec2_public_ip" {
  description = "Public IP of backend server"
  value       = aws_instance.backend_server.public_ip
}

output "cloudfront_url" {
  description = "Frontend CDN URL"
  value       = aws_cloudfront_distribution.frontend_cdn.domain_name
}

output "s3_bucket_name" {
  description = "Name of S3 bucket for frontend"
  value       = aws_s3_bucket.frontend_bucket.bucket
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "Subnet ID"
  value       = aws_subnet.public_subnet.id
}

output "backend_security_group_id" {
  description = "Backend EC2 Security Group ID"
  value       = aws_security_group.backend_sg.id
}
