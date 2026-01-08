@echo off
REM Deployment Helper Script for Windows
REM This script helps you deploy and verify your fixes

echo ╔════════════════════════════════════════════════════════════════╗
echo ║          🚀 DEPLOYMENT HELPER SCRIPT                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Not a git repository
    exit /b 1
)

echo 📋 Pre-Deployment Checklist:
echo.

REM Check if files exist
set all_files_exist=1

if exist "render.yaml" (
    echo ✅ render.yaml exists
) else (
    echo ❌ render.yaml missing
    set all_files_exist=0
)

if exist "runtime.txt" (
    echo ✅ runtime.txt exists
) else (
    echo ❌ runtime.txt missing
    set all_files_exist=0
)

if exist "requirements.txt" (
    echo ✅ requirements.txt exists
) else (
    echo ❌ requirements.txt missing
    set all_files_exist=0
)

if exist "Procfile" (
    echo ✅ Procfile exists
) else (
    echo ❌ Procfile missing
    set all_files_exist=0
)

if exist ".github\workflows\keep-alive.yml" (
    echo ✅ .github\workflows\keep-alive.yml exists
) else (
    echo ❌ .github\workflows\keep-alive.yml missing
    set all_files_exist=0
)

echo.

if %all_files_exist%==0 (
    echo ❌ Some files are missing. Please ensure all files are present.
    exit /b 1
)

echo 🔍 Checking configuration...
findstr /C:"python-3.11.0" runtime.txt >nul
if errorlevel 1 (
    echo ⚠️  Warning: runtime.txt might not have correct Python version
) else (
    echo ✅ Python version in runtime.txt is correct
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ⚠️  IMPORTANT: Before pushing, you MUST:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 1. Add GitHub Secret:
echo    • Go to: GitHub repo ^> Settings ^> Secrets and variables ^> Actions
echo    • Click: New repository secret
echo    • Name: RENDER_URL
echo    • Value: https://your-app-name.onrender.com
echo.
echo 2. Replace 'your-app-name' with your actual Render app name
echo.

set /p continue="Have you added the RENDER_URL secret? (y/n): "
if /i not "%continue%"=="y" (
    echo ⚠️  Please add the secret before continuing
    echo    Run this script again when ready
    exit /b 1
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🚀 Deploying changes...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Stage all changes
echo 📦 Staging changes...
git add .

REM Check if there are changes to commit
git diff --cached --quiet
if errorlevel 1 (
    REM Commit changes
    echo 💾 Committing changes...
    git commit -m "Fix Python/PyTorch compatibility for Render deployment" -m "- Updated torch to 2.5.1 (compatible with Python 3.11-3.13)" -m "- Updated torchvision to 0.20.1" -m "- Added Python version check in build command" -m "- Fixed deployment errors with package compatibility" -m "- Added GitHub Actions keep-alive workflow" -m "- Optimized for Render free tier"

    echo.
    echo 🔄 Pushing to GitHub...
    git push origin main

    if errorlevel 0 (
        echo.
        echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        echo ✅ SUCCESS! Changes pushed to GitHub
        echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        echo.
        echo 📋 Next steps:
        echo.
        echo 1. ✅ Wait for Render to auto-deploy (5-10 minutes^)
        echo    • Check: https://dashboard.render.com
        echo    • IMPORTANT: Clear build cache if this is a retry!
        echo    • Settings ^> Build ^& Deploy ^> Clear build cache ^& deploy
        echo.
        echo 2. ✅ Verify deployment in Render logs
        echo    • Should see: 'Listening on port 10000'
        echo.
        echo 3. ✅ Check GitHub Actions
        echo    • Go to: GitHub repo ^> Actions tab
        echo    • Should see 'Keep Render.com Alive' workflow running
        echo.
        echo 4. ✅ Test your app
        echo    • Visit: https://your-app-name.onrender.com
        echo.
        echo 🎉 Your app will now stay alive 24/7!
        echo.
    ) else (
        echo.
        echo ❌ Failed to push to GitHub
        echo    Check your git configuration and try again
        exit /b 1
    )
) else (
    echo ℹ️  No changes to commit
)

echo.
echo 📚 For more details, see:
echo    • QUICK_FIX_GUIDE.txt
echo    • FIXES_APPLIED.md
echo.

pause
