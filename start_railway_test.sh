#!/bin/bash

# Script to start Streamlit frontend for Railway backend testing
set -e

echo "🚀 Starting Streamlit Frontend for Railway Backend Testing"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Railway URL is set
if [ -z "$RAILWAY_BACKEND_URL" ]; then
    print_warning "RAILWAY_BACKEND_URL environment variable not set!"
    echo ""
    echo "Please set your Railway backend URL:"
    echo "export RAILWAY_BACKEND_URL='https://your-app.railway.app'"
    echo ""
    echo "Or update the app_railway.py file directly with your URL."
    echo ""
    read -p "Do you want to continue with default URL? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Exiting. Please set RAILWAY_BACKEND_URL first."
        exit 1
    fi
else
    print_success "Railway URL: $RAILWAY_BACKEND_URL"
fi

# Test Railway backend connection
print_status "Testing Railway backend connection..."
python test_railway_backend.py

if [ $? -eq 0 ]; then
    print_success "Railway backend is accessible!"
else
    print_warning "Railway backend test failed. You may need to check your URL or backend status."
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start Streamlit frontend
print_status "Starting Streamlit frontend..."
echo ""
print_success "Frontend will be available at: http://localhost:8501"
print_success "Press Ctrl+C to stop the frontend"
echo ""

# Start Streamlit with Railway app
streamlit run app_railway.py --server.port 8501 --server.address 0.0.0.0 