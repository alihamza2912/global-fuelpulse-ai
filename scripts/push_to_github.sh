#!/bin/bash
# Push Global FuelPulse AI to GitHub repository

set -e

echo "🚀 Checking Git remote..."
git remote -v

echo ""
echo "📤 Pushing code to https://github.com/alihamza2912/global-fuelpulse-ai.git..."
git push -u origin main

echo ""
echo "✅ Code successfully pushed to GitHub!"
echo "👉 Repository: https://github.com/alihamza2912/global-fuelpulse-ai"
echo "👉 Now deploy with 1-click on Streamlit Cloud: https://share.streamlit.io"
