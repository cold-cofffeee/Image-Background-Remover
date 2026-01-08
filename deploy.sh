#!/bin/bash

# Deployment Helper Script
# This script helps you deploy and verify your fixes

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🚀 DEPLOYMENT HELPER SCRIPT                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

echo "📋 Pre-Deployment Checklist:"
echo ""

# Check if files exist
files_to_check=(
    "render.yaml"
    "runtime.txt"
    "requirements.txt"
    "Procfile"
    ".github/workflows/keep-alive.yml"
)

all_files_exist=true
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        all_files_exist=false
    fi
done

echo ""

if [ "$all_files_exist" = false ]; then
    echo "❌ Some files are missing. Please ensure all files are present."
    exit 1
fi

# Check Python version in files
echo "🔍 Checking Python versions..."
runtime_version=$(cat runtime.txt | grep -o "python-[0-9.]*")
render_version=$(grep "PYTHON_VERSION" render.yaml -A 1 | grep "value:" | grep -o "[0-9.]*")

if [ "$runtime_version" = "python-3.11.0" ] && [ "$render_version" = "3.11.0" ]; then
    echo "✅ Python versions correct (3.11.0)"
else
    echo "⚠️  Python version mismatch"
    echo "   runtime.txt: $runtime_version"
    echo "   render.yaml: $render_version"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  IMPORTANT: Before pushing, you MUST:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Add GitHub Secret:"
echo "   • Go to: GitHub repo > Settings > Secrets and variables > Actions"
echo "   • Click: New repository secret"
echo "   • Name: RENDER_URL"
echo "   • Value: https://your-app-name.onrender.com"
echo ""
echo "2. Replace 'your-app-name' with your actual Render app name"
echo ""

read -p "Have you added the RENDER_URL secret? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  Please add the secret before continuing"
    echo "   Run this script again when ready"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Deploying changes..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Stage all changes
echo "📦 Staging changes..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    # Commit changes
    echo "💾 Committing changes..."
    git commit -m "Fix Render deployment and add keep-alive workflow

- Updated Python version to 3.11.0 for better compatibility
- Optimized Gunicorn settings for free tier (1 worker, 2 threads)
- Increased timeout to 300s for large image processing
- Updated all package versions for compatibility
- Added GitHub Actions workflow to keep Render app alive 24/7
- Pings every 14 minutes to prevent sleep on free tier"

    echo ""
    echo "🔄 Pushing to GitHub..."
    git push origin main

    if [ $? -eq 0 ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ SUCCESS! Changes pushed to GitHub"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "📋 Next steps:"
        echo ""
        echo "1. ✅ Wait for Render to auto-deploy (5-10 minutes)"
        echo "   • Check: https://dashboard.render.com"
        echo ""
        echo "2. ✅ Verify deployment in Render logs"
        echo "   • Should see: 'Listening on port 10000'"
        echo ""
        echo "3. ✅ Check GitHub Actions"
        echo "   • Go to: GitHub repo > Actions tab"
        echo "   • Should see 'Keep Render.com Alive' workflow running"
        echo ""
        echo "4. ✅ Test your app"
        echo "   • Visit: https://your-app-name.onrender.com"
        echo ""
        echo "🎉 Your app will now stay alive 24/7!"
        echo ""
    else
        echo ""
        echo "❌ Failed to push to GitHub"
        echo "   Check your git configuration and try again"
        exit 1
    fi
fi

echo ""
echo "📚 For more details, see:"
echo "   • QUICK_FIX_GUIDE.txt"
echo "   • FIXES_APPLIED.md"
echo ""
