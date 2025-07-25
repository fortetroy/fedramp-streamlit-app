#!/bin/bash
# Quick start script for FedRAMP Analysis Hub

echo "🚀 FedRAMP Analysis Hub - Quick Start"
echo "===================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Launch the app
echo "🎉 Launching FedRAMP Analysis Hub..."
echo "===================================="
echo "Access the app at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run Home.py