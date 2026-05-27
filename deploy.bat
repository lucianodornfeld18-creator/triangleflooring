@echo off
REM ============================================================
REM  Triangle Flooring — One-click deploy to GitHub + Cloudflare
REM ============================================================
REM
REM  How it works:
REM    1. Stages all changed files (git add .)
REM    2. Commits with auto-generated message + timestamp
REM    3. Pushes to GitHub
REM    4. Cloudflare Pages auto-deploys from the push (~30s)
REM
REM  How to use:
REM    Just double-click this file from File Explorer.
REM
REM  Requirements (one-time setup):
REM    - Git for Windows installed (https://git-scm.com/download/win)
REM    - This folder is a git repo (has hidden .git folder)
REM    - GitHub credentials cached (or use HTTPS PAT / SSH key)
REM
REM ============================================================

setlocal enabledelayedexpansion

REM Move to script directory
cd /d "%~dp0"

echo.
echo ============================================================
echo  Triangle Flooring — Deploy to GitHub
echo ============================================================
echo.

REM Verify this is a git repo
if not exist ".git" (
  echo [ERROR] No .git folder found in this directory.
  echo This folder is not a Git repository.
  echo.
  echo If you've never set this up:
  echo    git init
  echo    git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
  echo    git branch -M main
  echo    git push -u origin main
  echo.
  pause
  exit /b 1
)

REM Verify git is installed
where git >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Git is not installed or not in PATH.
  echo Download from: https://git-scm.com/download/win
  pause
  exit /b 1
)

REM Show current status
echo Current Git status:
echo ------------------------------------------------------------
git status --short
echo ------------------------------------------------------------
echo.

REM Check if there's anything to commit
git diff --quiet HEAD --
if not errorlevel 1 (
  REM Also check for untracked files
  git status --porcelain | findstr /R "^?? " >nul
  if errorlevel 1 (
    echo No changes to deploy. Working tree is clean.
    echo.
    pause
    exit /b 0
  )
)

REM Build commit message with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "YYYY=%datetime:~0,4%"
set "MM=%datetime:~4,2%"
set "DD=%datetime:~6,2%"
set "HH=%datetime:~8,2%"
set "MIN=%datetime:~10,2%"
set "COMMIT_MSG=Site update %YYYY%-%MM%-%DD% %HH%:%MIN%"

REM Optional: ask user for a custom commit message
echo Auto commit message: "%COMMIT_MSG%"
echo.
set /p "USER_MSG=Press ENTER to use this, or type a custom message: "
if not "!USER_MSG!"=="" set "COMMIT_MSG=!USER_MSG!"

echo.
echo Staging all changes...
git add .
if errorlevel 1 (
  echo [ERROR] git add failed.
  pause
  exit /b 1
)

echo Committing...
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
  echo [ERROR] git commit failed (maybe nothing was staged).
  pause
  exit /b 1
)

echo Pushing to GitHub...
git push
if errorlevel 1 (
  echo.
  echo [ERROR] git push failed.
  echo Common causes:
  echo   - No remote configured: git remote -v
  echo   - Credentials expired: re-authenticate with GitHub
  echo   - Branch mismatch: git push -u origin main
  echo.
  pause
  exit /b 1
)

echo.
echo ============================================================
echo  Deploy submitted!
echo ============================================================
echo.
echo  Cloudflare Pages will build and deploy in approximately 30s.
echo  Watch progress at: https://dash.cloudflare.com
echo  Live site: https://triangle-floor.com/
echo.
echo  Done.
echo.
pause
