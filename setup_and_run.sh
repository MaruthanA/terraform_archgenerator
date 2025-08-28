#!/bin/bash

# Terraform Architecture Generator - Setup and Run Script
# This script creates a virtual environment, installs dependencies, and runs the Streamlit app

set -e  # Exit on any error

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "🚀 Setting up Terraform Architecture Generator..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
if [ -f "$PROJECT_DIR/requirements_streamlit.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements_streamlit.txt"
else
    echo "❌ Error: requirements_streamlit.txt not found"
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🌐 Starting Streamlit application..."
echo "📍 Navigate to the URL shown below to access the app"
echo ""

# Run the Streamlit app
cd "$PROJECT_DIR"
streamlit run streamlit_app.py

# Deactivate virtual environment when done
deactivate
