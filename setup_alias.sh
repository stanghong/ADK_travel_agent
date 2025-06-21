#!/bin/bash

# Setup script for Travel Assistant aliases
# Run this once to add convenient aliases to your shell

# Get the current directory (should be 14-travel-assistant-agent)
CURRENT_DIR="$(pwd)"
LAUNCH_SCRIPT="$CURRENT_DIR/launch.sh"

# Check if we're in the right directory
if [[ ! -f "app.py" ]] || [[ ! -f "api.py" ]]; then
    echo "❌ Error: Please run this script from the 14-travel-assistant-agent directory"
    exit 1
fi

# Determine which shell profile to use
SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
else
    SHELL_PROFILE="$HOME/.bash_profile"
fi

echo "🔧 Setting up Travel Assistant aliases..."
echo "📁 Travel Assistant directory: $CURRENT_DIR"
echo "📝 Shell profile: $SHELL_PROFILE"
echo ""

# Create aliases
ALIASES=(
    "# Travel Assistant Aliases"
    "alias travel='$LAUNCH_SCRIPT'"
    "alias travel-start='$LAUNCH_SCRIPT'"
    "alias travel-stop='pkill -f \"adk_web_server.py\" && pkill -f \"uvicorn api:app\" && pkill -f \"streamlit run app.py\"'"
    "alias travel-test='cd $CURRENT_DIR && python simple_test.py'"
    "alias travel-logs='cd $CURRENT_DIR && tail -f adk_web.log fastapi.log streamlit.log'"
    ""
)

# Check if aliases already exist
if grep -q "alias travel=" "$SHELL_PROFILE" 2>/dev/null; then
    echo "⚠️  Travel Assistant aliases already exist in $SHELL_PROFILE"
    echo "   You can use: travel, travel-start, travel-stop, travel-test, travel-logs"
else
    # Add aliases to shell profile
    echo "📝 Adding aliases to $SHELL_PROFILE..."
    echo "" >> "$SHELL_PROFILE"
    for alias_line in "${ALIASES[@]}"; do
        echo "$alias_line" >> "$SHELL_PROFILE"
    done
    
    echo "✅ Aliases added successfully!"
    echo ""
    echo "🔄 To use the aliases immediately, run:"
    echo "   source $SHELL_PROFILE"
    echo ""
fi

echo "🚀 Available commands:"
echo "   travel          - Start all Travel Assistant services"
echo "   travel-start    - Start all Travel Assistant services"
echo "   travel-stop     - Stop all Travel Assistant services"
echo "   travel-test     - Run backend tests"
echo "   travel-logs     - View all service logs"
echo ""
echo "💡 You can now run 'travel' from anywhere to start the Travel Assistant!" 