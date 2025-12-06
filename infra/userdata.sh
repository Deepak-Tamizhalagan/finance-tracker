#!/bin/bash
yum update -y
yum install -y git python3

cd /home/ec2-user

# Clone your backend from GitHub
git clone https://github.com/finance-tracker-f25/finance-tracker.git

cd finance-tracker/backend

pip3 install -r requirements.txt

# Start FastAPI (port 8000)
nohup python3 main.py > app.log 2>&1 &
