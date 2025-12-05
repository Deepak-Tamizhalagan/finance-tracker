##############################################
# Key Outputs for Demo & Documentation
##############################################

output "ec2_public_ip" {
  description = "Public IP of the EC2 backend server"
  value       = aws_instance.backend_server.public_ip
}

output "cloudfront_url" {
  description = "URL of the CloudFront distribution hosting frontend"
  value       = aws_cloudfront_distribution.frontend_cdn.domain_name
}

output "s3_bucket_name" {
  description = "Name of S3 bucket containing the frontend"
  value       = aws_s3_bucket.frontend_bucket.bucket
}

output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public_subnet.id
}

output "backend_security_group_id" {
  description = "Security group ID for backend EC2 server"
  value       = aws_security_group.backend_sg.id
}
