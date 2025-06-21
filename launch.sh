#!/bin/bash

# Find the travel assistant directory
# This script can be run from anywhere and will find the correct directory

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we're already in the travel assistant directory
if [[ -f "$SCRIPT_DIR/app.py" ]] && [[ -f "$SCRIPT_DIR/api.py" ]] && [[ -d "$SCRIPT_DIR/orchestrator_agent" ]]; then
    echo "✅ Already in travel assistant directory: $SCRIPT_DIR"
    cd "$SCRIPT_DIR"
else
    echo "❌ Script not found in travel assistant directory"
    echo "Please place this script in the 14-travel-assistant-agent folder"
    exit 1
fi

# Make the startup script executable
chmod +x start_all.sh

# Run the startup script
echo "🚀 Launching Travel Assistant..."
./start_all.sh 