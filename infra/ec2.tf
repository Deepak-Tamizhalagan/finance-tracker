##############################################
# Lookup latest Ubuntu 22.04 LTS AMI
##############################################

data "aws_ami" "ubuntu_2204" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

##############################################
# Backend EC2 Instance
##############################################

resource "aws_instance" "backend_server" {
  # Use the AMI looked up above (works in any region)
  ami           = data.aws_ami.ubuntu_2204.id
  instance_type = var.instance_type

  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.backend_sg.id]

  # If you KEEP the IAM resources from iam.tf, leave this line.
  # If you remove IAM from Terraform, COMMENT THIS LINE OUT.
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  user_data = file("${path.module}/userdata.sh")

  tags = {
    Name = "${var.project_name}-backend-ec2"
  }
}
