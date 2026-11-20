#!/bin/bash

# ReWear Clothing System - Quick Start Script
# This script automates the setup process

echo "========================================"
echo "ReWear Clothing System - Quick Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found $PYTHON_VERSION"
echo ""

#Setup backend
echo "Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your configuration"
fi

echo "✓ Backend setup complete"
echo ""

# Return to root directory
cd ..

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run ReWear:"
echo ""
echo "1. Start Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   python app.py"
echo ""
echo "2. Start Frontend (Terminal 2):"
echo "   cd frontend"
echo "   python -m http.server 8000"
echo ""
echo "3. Open browser:"
echo "   http://localhost:8000"
echo ""
echo "API Documentation: See docs/API_DOCUMENTATION.md"
echo "System Architecture: See SYSTEM_ARCHITECTURE.md"
echo "ReadMe: See README.md"
echo ""
echo "Happy sustainable shopping! ♻️"
