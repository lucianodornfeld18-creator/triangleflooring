# =============================================================================
#  Triangle Flooring — One-click deploy (PowerShell version)
# =============================================================================
#
#  Use this if you prefer PowerShell over the .bat file. It gives nicer
#  output and better error handling.
#
#  How to run:
#    Right-click → Run with PowerShell
#    OR from PowerShell: .\deploy.ps1
#    OR with custom message: .\deploy.ps1 -Message "Updated pillar pages"
#
# =============================================================================

param(
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"

# Move to script directory
Set-Location -Path $PSScriptRoot

function Write-Banner($text) {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "  $text" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
}

Write-Banner "Triangle Flooring - Deploy to GitHub"

# Verify git repo
if (-not (Test-Path ".git")) {
    Write-Host "[ERROR] No .git folder found. This folder is not a git repository." -ForegroundColor Red
    Write-Host ""
    Write-Host "First-time setup:"
    Write-Host "  git init"
    Write-Host "  git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git"
    Write-Host "  git branch -M main"
    Write-Host "  git push -u origin main"
    Read-Host "Press Enter to exit"
    exit 1
}

# Verify git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win"
    Read-Host "Press Enter to exit"
    exit 1
}

# Show what's changed
Write-Host "Current git status:" -ForegroundColor Yellow
Write-Host ("-" * 60)
git status --short
Write-Host ("-" * 60)
Write-Host ""

# Check if there are actually changes
$changes = git status --porcelain
if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "No changes to deploy. Working tree is clean." -ForegroundColor Green
    Read-Host "Press Enter to exit"
    exit 0
}

# Build commit message
if ([string]::IsNullOrWhiteSpace($Message)) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $defaultMsg = "Site update $timestamp"
    Write-Host "Auto commit message: '$defaultMsg'" -ForegroundColor Gray
    $userMsg = Read-Host "Press ENTER to use this, or type a custom message"
    if ([string]::IsNullOrWhiteSpace($userMsg)) {
        $Message = $defaultMsg
    } else {
        $Message = $userMsg
    }
}

Write-Host ""
Write-Host "Staging changes..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] git add failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Committing..." -ForegroundColor Yellow
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] git commit failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] git push failed." -ForegroundColor Red
    Write-Host "Common causes:"
    Write-Host "  - No remote configured: run 'git remote -v'"
    Write-Host "  - Credentials expired: re-authenticate with GitHub"
    Write-Host "  - Branch mismatch: try 'git push -u origin main'"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Banner "Deploy submitted!"
Write-Host "  Cloudflare Pages will build and deploy in ~30 seconds." -ForegroundColor Green
Write-Host "  Live site: https://triangle-floor.com/"
Write-Host "  Cloudflare dashboard: https://dash.cloudflare.com"
Write-Host ""
Read-Host "Press Enter to close"
