# Step-by-Step: Push to GitHub

Follow these steps to push your code to GitHub:

## Step 1: Configure Git (First Time Only)

Run these commands with your information:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Important:** Use the same email as your GitHub account!

## Step 2: Commit Your Files

```powershell
git commit -m "Initial commit - PIR assignment with SHEEP"
```

## Step 3: Create GitHub Repository

1. Go to https://github.com
2. Sign in (or create account)
3. Click the **"+"** icon → **"New repository"**
4. Name it: `cs528-pir-assignment` (or any name)
5. Choose **Public** or **Private**
6. **DON'T** check "Initialize with README"
7. Click **"Create repository"**

## Step 4: Connect to GitHub

After creating the repository, GitHub will show you commands. Use these:

```powershell
# Replace YOUR_USERNAME with your GitHub username
# Replace REPO_NAME with your repository name
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Verify connection
git remote -v
```

## Step 5: Push to GitHub

```powershell
git branch -M main
git push -u origin main
```

**You'll need to authenticate!**

### Authentication Options:

#### Option A: Personal Access Token (Recommended)

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name it: "CS528 Assignment"
4. Check **"repo"** scope
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

When pushing:
- **Username:** Your GitHub username
- **Password:** The token you just copied

#### Option B: GitHub CLI

```powershell
# Install GitHub CLI
winget install GitHub.cli

# Authenticate
gh auth login

# Then push
git push -u origin main
```

---

## Quick Commands (Copy & Paste)

```powershell
# 1. Configure Git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Commit
git commit -m "Initial commit - PIR assignment with SHEEP"

# 3. Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 4. Push
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "fatal: not a git repository"
- Run: `git init` first

### "Permission denied" or "Authentication failed"
- Use Personal Access Token (not password)
- Make sure token has "repo" scope

### "remote origin already exists"
- Remove it: `git remote remove origin`
- Add it again: `git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git`

---

## After Pushing

Once your code is on GitHub:
1. Go to your repository
2. Click **"Code"** → **"Codespaces"**
3. Click **"Create codespace on main"**
4. Build the SHEEP server in Codespaces
5. Expose port 34568
6. Connect from your local machine

Let me know if you need help with any step! 🚀

