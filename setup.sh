#!/bin/bash
# Setup script for Imagen 3 API Integration
# This script installs dependencies and runs the test setup

echo "Setting up Imagen 3 API Integration..."
echo "======================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

# Create virtual environment (optional)
echo -n "Do you want to create a virtual environment? (y/n): "
read create_venv

if [[ "$create_venv" == "y" || "$create_venv" == "Y" ]]; then
    echo "Creating virtual environment..."
    
    # Check if venv module is available
    python3 -m venv --help &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Error: Python venv module is not available."
        echo "Please install the Python venv package and try again."
        exit 1
    fi
    
    # Create and activate virtual environment
    python3 -m venv venv
    
    # Activate virtual environment based on OS
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    echo "Virtual environment created and activated."
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

echo "Dependencies installed successfully."

# Prompt for API key if not set
if grep -q "your_api_key_here" .env; then
    echo ""
    echo "You need to set up your Gemini API key."
    echo "Get your API key from https://makersuite.google.com/"
    echo -n "Enter your Gemini API key: "
    read api_key
    
    if [[ -n "$api_key" ]]; then
        # Update the .env file with the provided API key
        sed -i.bak "s/your_api_key_here/$api_key/g" .env
        rm -f .env.bak 2>/dev/null
        echo "API key saved to .env file."
    else
        echo "No API key provided. You'll need to edit the .env file manually."
    fi
fi

# Run the test setup
echo ""
echo "Running setup test..."
python3 test_setup.py

echo ""
echo "Setup complete!"
echo "To generate images, run: python app.py \"your prompt here\""
echo "To start the web interface, run: python web_interface.py"
