# Deploy Guide — Triangle Flooring

## TL;DR — How to publish changes

Double-click **`deploy.bat`** in this folder. That's it.

The script will:
1. Stage all changed files
2. Commit with a timestamped message (or you can type a custom one)
3. Push to GitHub
4. Cloudflare Pages picks up the push and auto-deploys (~30 seconds)

After ~30s, the live site at <https://triangle-floor.com/> reflects the changes.

---

## First-time setup checklist

Run through this once, then you'll never have to think about it again.

### 1. Install Git for Windows (if not already)

Download: <https://git-scm.com/download/win>

After install, open Command Prompt or PowerShell and verify:

```
git --version
```

### 2. Configure your git identity

```
git config --global user.name "Luciano Dornfeld"
git config --global user.email "lucianodornfeld18@gmail.com"
```

### 3. Verify this folder is a git repo

Open Command Prompt in this folder and run:

```
git status
```

If it says "not a git repository", you need to initialize it:

```
git init
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git branch -M main
git add .
git commit -m "Initial commit"
git push -u origin main
```

### 4. Cache GitHub credentials (one time)

The easiest way is to install **GitHub CLI** or **Git Credential Manager** (bundled with newer Git for Windows installers). The first time you push, it'll open a browser to authenticate, then remember your credentials.

Alternative: create a **Personal Access Token (PAT)** at <https://github.com/settings/tokens> with `repo` scope, and use it as your password when prompted.

### 5. Verify Cloudflare Pages is connected

1. Log into <https://dash.cloudflare.com>
2. Navigate to **Workers & Pages** → your project (probably "triangle-floor" or "triangleflooring")
3. **Settings → Builds & deployments → Build configuration**
4. Verify:
   - Production branch: `main`
   - Build command: (empty — static site)
   - Build output directory: `/`
   - Root directory: `/`

If it's not connected:
1. In Cloudflare Pages → **Create application → Pages → Connect to Git**
2. Authorize Cloudflare to access your GitHub
3. Pick the `triangleflooring-main` repo
4. Production branch: `main`
5. Build command: leave empty
6. Build output: `/`
7. **Save and Deploy**

After that, every `git push` to `main` triggers an automatic deploy. No further action needed.

---

## Daily workflow

```
1. Edit files (or let Claude edit them in this folder)
2. Double-click deploy.bat
3. Type a commit message (or just press Enter for auto-message)
4. Wait ~30 seconds for Cloudflare to deploy
5. Verify on https://triangle-floor.com/
```

That's the whole loop.

---

## Alternative: deploy.ps1 (PowerShell version)

Same thing as `deploy.bat`, but with nicer colored output and better error messages. Right-click → Run with PowerShell.

For a custom commit message in one shot:

```powershell
.\deploy.ps1 -Message "Added pet-friendly pillar page"
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "git is not recognized" | Install Git for Windows |
| "not a git repository" | Run `git init` + add remote (see step 3) |
| "authentication failed" | Re-authenticate via Git Credential Manager or use a PAT |
| "rejected — non-fast-forward" | Run `git pull --rebase` first, then deploy.bat |
| Cloudflare didn't deploy | Check Cloudflare dashboard for build errors; verify the push reached GitHub |
| Site shows old content | Hard refresh (Ctrl+F5); Cloudflare cache can take 30-60s to update edge nodes |

---

## What `deploy.bat` actually runs

For transparency — these are the commands you can also run manually from any terminal in this folder:

```
git add .
git commit -m "Site update YYYY-MM-DD HH:MM"
git push
```

That's the entire deploy. The .bat file just wraps these with sanity checks (verifying the repo exists, git is installed, there are actually changes to commit, etc.) and pretty output.

---

## Files Claude can edit safely

If you let Claude work on this folder in future sessions, these are the canonical files/directories:

- All `.html` files (130 of them)
- `sitemap.xml`
- `robots.txt`
- `llms.txt`
- `_redirects`
- `_headers`
- `images/` (Claude won't modify existing images but may reference new ones)

After Claude finishes, double-click `deploy.bat` to publish.
