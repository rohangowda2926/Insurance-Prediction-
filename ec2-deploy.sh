#!/bin/bash

# AWS EC2 Deployment Script for Insurance Prediction Model

echo "🚀 Setting up Insurance Prediction on EC2..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Clone repository
git clone https://github.com/rohangowda2926/Insurance-Charges-Predictor.git
cd Insurance-Charges-Predictor

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd app/app
pip install -r requirements.txt

# Install additional dependencies for production
pip install gunicorn

# Run FastAPI with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

echo "✅ App running on http://YOUR_EC2_IP:8000"