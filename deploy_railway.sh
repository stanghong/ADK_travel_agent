#!/bin/bash

# Travel Assistant Railway Deployment Script
# This script helps deploy the Travel Assistant to Railway

set -e

echo "🚀 Travel Assistant Railway Deployment"
echo "======================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
fi

# Check if project is linked
if [ ! -f ".railway" ]; then
    echo "🔗 Linking to Railway project..."
    railway link
fi

# Check environment variables
echo "🔧 Checking environment variables..."
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  Warning: GOOGLE_API_KEY not set in environment"
    echo "   Please set it in Railway dashboard after deployment"
fi

if [ -z "$OPENWEATHER_API_KEY" ]; then
    echo "ℹ️  OPENWEATHER_API_KEY not set (optional)"
fi

# Build and deploy
echo "🏗️  Building and deploying to Railway..."
railway up

# Get the deployment URL
echo "🌐 Getting deployment URL..."
DEPLOY_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)

if [ -n "$DEPLOY_URL" ]; then
    echo "✅ Deployment successful!"
    echo "🌍 Your Travel Assistant is available at: $DEPLOY_URL"
    echo "📚 API Documentation: $DEPLOY_URL/docs"
    echo "❤️  Health Check: $DEPLOY_URL/health"
    
    echo ""
    echo "🔧 Next steps:"
    echo "1. Set GOOGLE_API_KEY in Railway dashboard"
    echo "2. Set OPENWEATHER_API_KEY in Railway dashboard (optional)"
    echo "3. Test your deployment with:"
    echo "   curl $DEPLOY_URL/health"
else
    echo "❌ Failed to get deployment URL"
    echo "Check Railway dashboard for deployment status"
fi

echo ""
echo "🎉 Deployment script completed!" 