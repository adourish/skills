# Git Version Control - Master Guide

**Last Updated:** January 26, 2026  
**Purpose:** Comprehensive guide for Git version control, workflows, and best practices  
**Success Rate:** Proven patterns from production development

---

## Table of Contents

1. [Overview](#overview)
2. [Git Fundamentals](#git-fundamentals)
3. [Repository Setup](#repository-setup)
4. [Branch Strategies](#branch-strategies)
5. [Commit Best Practices](#commit-best-practices)
6. [Working with Remotes](#working-with-remotes)
7. [Merge and Rebase](#merge-and-rebase)
8. [Conflict Resolution](#conflict-resolution)
9. [Stashing and Cherry-Picking](#stashing-and-cherry-picking)
10. [Gitignore Patterns](#gitignore-patterns)
11. [Credential Management](#credential-management)
12. [Troubleshooting](#troubleshooting)

---

## Overview

Git is a distributed version control system that tracks changes in source code during software development. This guide covers essential Git workflows for Salesforce and general development.

### Prerequisites

- Git installed (2.30+)
- Basic command line knowledge
- Understanding of version control concepts

### Check Git Version

```bash
git --version
```

### Configure Git

```bash
# Set user name and email (required)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default editor
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "notepad"      # Notepad

# Set default branch name
git config --global init.defaultBranch main

# View all config
git config --list
```

---

## Git Fundamentals

### Repository States

```
Working Directory → Staging Area → Local Repository → Remote Repository
     (edit)           (git add)      (git commit)      (git push)
```

### Basic Commands

```bash
# Initialize new repository
git init

# Clone existing repository
git clone https://github.com/user/repo.git

# Check status
git status

# View changes
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff HEAD              # All changes

# Add files to staging
git add file.txt           # Specific file
git add .                  # All files in current directory
git add -A                 # All files in repository

# Commit changes
git commit -m "Commit message"
git commit -am "Message"   # Add and commit tracked files

# View commit history
git log
git log --oneline          # Compact view
git log --graph --oneline  # Visual graph
git log -n 5               # Last 5 commits
```

### File States

```bash
# Untracked: New file not in Git
# Modified: Changed file not staged
# Staged: File ready to commit
# Committed: File saved in repository

# Check file status
git status

# Unstage file
git reset HEAD file.txt

# Discard changes in working directory
git checkout -- file.txt

# Remove file from Git (keep in filesystem)
git rm --cached file.txt

# Remove file from Git and filesystem
git rm file.txt
```

---

## Repository Setup

### Initialize New Repository

```bash
# Create project directory
mkdir my-project
cd my-project

# Initialize Git
git init

# Create initial files
echo "# My Project" > README.md
echo "node_modules/" > .gitignore

# Initial commit
git add .
git commit -m "Initial commit"
```

### Connect to Remote Repository

```bash
# Add remote
git remote add origin https://github.com/user/repo.git

# Verify remote
git remote -v

# Push to remote
git push -u origin main

# Change remote URL
git remote set-url origin https://new-url.git
```

### Clone Existing Repository

```bash
# Clone repository
git clone https://github.com/user/repo.git

# Clone to specific directory
git clone https://github.com/user/repo.git my-folder

# Clone specific branch
git clone -b develop https://github.com/user/repo.git

# Shallow clone (faster, less history)
git clone --depth 1 https://github.com/user/repo.git
```

---

## Branch Strategies

### Branch Basics

```bash
# List branches
git branch              # Local branches
git branch -r           # Remote branches
git branch -a           # All branches

# Create new branch
git branch feature-name

# Switch to branch
git checkout feature-name

# Create and switch in one command
git checkout -b feature-name

# Or using newer syntax
git switch feature-name
git switch -c feature-name  # Create and switch

# Delete branch
git branch -d feature-name      # Safe delete (merged only)
git branch -D feature-name      # Force delete

# Delete remote branch
git push origin --delete feature-name
```

### Feature Branch Workflow

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/workflow-enhancements

# 2. Make changes and commit
git add .
git commit -m "Add workflow node type validation"

# 3. Push feature branch
git push -u origin feature/workflow-enhancements

# 4. Create pull request (on GitHub/Azure DevOps)

# 5. After approval, merge to main
git checkout main
git pull origin main
git merge feature/workflow-enhancements

# 6. Delete feature branch
git branch -d feature/workflow-enhancements
git push origin --delete feature/workflow-enhancements
```

### Gitflow Workflow

```
main (production)
  ├── develop (integration)
  │   ├── feature/feature-1
  │   ├── feature/feature-2
  │   └── release/v1.0
  └── hotfix/critical-bug
```

```bash
# Start feature
git checkout develop
git checkout -b feature/new-feature

# Finish feature
git checkout develop
git merge feature/new-feature
git branch -d feature/new-feature

# Start release
git checkout develop
git checkout -b release/v1.0

# Finish release
git checkout main
git merge release/v1.0
git tag v1.0
git checkout develop
git merge release/v1.0
git branch -d release/v1.0

# Hotfix
git checkout main
git checkout -b hotfix/critical-fix
# ... fix and test ...
git checkout main
git merge hotfix/critical-fix
git checkout develop
git merge hotfix/critical-fix
git branch -d hotfix/critical-fix
```

---

## Commit Best Practices

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

**Examples:**

```bash
# Simple commit
git commit -m "feat: add workflow node type validation"

# Detailed commit
git commit -m "feat(workflow): add node type validation

Add helper methods to cmn_WorkflowNode class:
- isCaptureNode() for task nodes
- isApprovalNode() for review nodes
- requiresFormCompletion() for form validation

Closes #123"

# Bug fix
git commit -m "fix(lwc): resolve caching issue in workflow diagram

Deploy parent components to break cache when child changes"

# Documentation
git commit -m "docs: update Salesforce development guide

Add SOQL query patterns and cache-busting strategies"
```

### Atomic Commits

```bash
# ✅ GOOD - One logical change per commit
git add cmn_WorkflowNode.cls
git commit -m "feat: add node type helper methods"

git add cmn_WorkflowTransitionMethods.cls
git commit -m "feat: add pre/post transition hooks"

# ❌ BAD - Multiple unrelated changes
git add .
git commit -m "Various updates"
```

### Amending Commits

```bash
# Amend last commit message
git commit --amend -m "New commit message"

# Add forgotten files to last commit
git add forgotten-file.txt
git commit --amend --no-edit

# ⚠️ WARNING: Don't amend commits that are already pushed
```

---

## Working with Remotes

### Fetch, Pull, and Push

```bash
# Fetch updates from remote (doesn't merge)
git fetch origin

# Pull updates from remote (fetch + merge)
git pull origin main

# Pull with rebase (cleaner history)
git pull --rebase origin main

# Push to remote
git push origin main

# Push new branch
git push -u origin feature-branch

# Force push (DANGEROUS - use with caution)
git push --force origin main
git push --force-with-lease origin main  # Safer alternative
```

### Tracking Branches

```bash
# Set upstream branch
git push -u origin feature-branch

# After setting upstream, just use
git push
git pull

# View tracking branches
git branch -vv

# Change upstream branch
git branch --set-upstream-to=origin/main
```

### Multiple Remotes

```bash
# Add multiple remotes
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git

# Fetch from specific remote
git fetch upstream

# Pull from upstream
git pull upstream main

# Push to origin
git push origin main
```

---

## Merge and Rebase

### Merge

```bash
# Merge feature branch into main
git checkout main
git merge feature-branch

# Merge with commit message
git merge feature-branch -m "Merge feature-branch into main"

# Abort merge
git merge --abort

# Fast-forward merge (no merge commit)
git merge --ff-only feature-branch

# No fast-forward (always create merge commit)
git merge --no-ff feature-branch
```

### Rebase

```bash
# Rebase current branch onto main
git checkout feature-branch
git rebase main

# Interactive rebase (edit commits)
git rebase -i HEAD~3  # Last 3 commits

# Continue after resolving conflicts
git rebase --continue

# Skip commit
git rebase --skip

# Abort rebase
git rebase --abort
```

### Merge vs Rebase

```bash
# Merge: Preserves history, creates merge commit
git checkout main
git merge feature-branch

# Result:
#   A---B---C main
#    \     /
#     D---E feature-branch

# Rebase: Linear history, no merge commit
git checkout feature-branch
git rebase main

# Result:
#   A---B---C---D'---E' main/feature-branch
```

**When to use:**
- **Merge:** For integrating completed features, preserving history
- **Rebase:** For updating feature branches, cleaning up history before merge

---

## Conflict Resolution

### Resolving Merge Conflicts

```bash
# Start merge
git merge feature-branch

# Conflict detected
# CONFLICT (content): Merge conflict in file.txt

# View conflicted files
git status

# Open file and resolve conflicts
# Look for conflict markers:
<<<<<<< HEAD
Current branch content
=======
Feature branch content
>>>>>>> feature-branch

# After resolving, mark as resolved
git add file.txt

# Complete merge
git commit

# Or abort merge
git merge --abort
```

### Conflict Resolution Tools

```bash
# Use merge tool
git mergetool

# Configure merge tool (VS Code)
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# View diff during conflict
git diff --ours file.txt      # Current branch
git diff --theirs file.txt    # Other branch
git diff --base file.txt      # Common ancestor
```

### Resolving Rebase Conflicts

```bash
# Start rebase
git rebase main

# Conflict detected
# Resolve conflicts in files

# After resolving
git add file.txt
git rebase --continue

# Or skip this commit
git rebase --skip

# Or abort rebase
git rebase --abort
```

---

## Stashing and Cherry-Picking

### Stashing Changes

```bash
# Stash current changes
git stash

# Stash with message
git stash save "Work in progress on feature X"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply specific stash
git stash apply stash@{1}

# Apply and remove from stash list
git stash pop

# View stash contents
git stash show
git stash show -p  # Show diff

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

### Stash Use Cases

```bash
# Scenario 1: Switch branches with uncommitted changes
git stash
git checkout other-branch
# ... work on other branch ...
git checkout original-branch
git stash pop

# Scenario 2: Pull with local changes
git stash
git pull
git stash pop

# Scenario 3: Save experimental changes
git stash save "Experimental approach - may not use"
```

### Cherry-Picking

```bash
# Apply specific commit to current branch
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Cherry-pick without committing
git cherry-pick -n abc123

# Abort cherry-pick
git cherry-pick --abort

# Continue after resolving conflicts
git cherry-pick --continue
```

---

## Gitignore Patterns

### Common Patterns

```gitignore
# Node modules
node_modules/
npm-debug.log

# Build outputs
dist/
build/
*.min.js
*.min.css

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Environment files
.env
.env.local
.env.*.local

# Logs
logs/
*.log
npm-debug.log*

# Temporary files
tmp/
temp/
*.tmp
```

### Salesforce-Specific

```gitignore
# Salesforce DX
.sfdx/
.sf/

# Local config
.localdevserver/
.vscode/settings.json

# Scratch org files
config/project-scratch-def.json

# Metadata
**/*.dup

# LWC
**/__tests__/**
**/.eslintcache

# Apex
**/*.cls-meta.xml~
**/*.trigger-meta.xml~

# Logs
*.log
```

### Gitignore Commands

```bash
# Create .gitignore
touch .gitignore

# Add pattern
echo "node_modules/" >> .gitignore

# Remove already tracked file
git rm --cached file.txt
git commit -m "Remove file.txt from tracking"

# Check if file is ignored
git check-ignore -v file.txt

# Force add ignored file
git add -f file.txt
```

---

## Credential Management

### HTTPS Authentication

```bash
# Cache credentials (15 minutes default)
git config --global credential.helper cache

# Cache for specific time (1 hour)
git config --global credential.helper 'cache --timeout=3600'

# Store credentials permanently (LESS SECURE)
git config --global credential.helper store

# Windows Credential Manager
git config --global credential.helper manager-core
```

### SSH Authentication

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Copy public key (add to GitHub/Azure DevOps)
cat ~/.ssh/id_ed25519.pub

# Test SSH connection
ssh -T git@github.com
```

### Personal Access Tokens

```bash
# Use token as password when prompted
# Username: your-username
# Password: ghp_yourPersonalAccessToken

# Or include in URL (NOT RECOMMENDED for security)
git clone https://username:token@github.com/user/repo.git

# Better: Use credential helper
git config --global credential.helper store
# Then enter token once, it will be saved
```

---

## Troubleshooting

### Issue 1: Detached HEAD State

**Problem:** `You are in 'detached HEAD' state`

**Solution:**

```bash
# Create branch from current state
git checkout -b new-branch-name

# Or discard changes and return to branch
git checkout main
```

### Issue 2: Undo Last Commit

**Problem:** Need to undo last commit

**Solution:**

```bash
# Keep changes in working directory
git reset --soft HEAD~1

# Unstage changes
git reset HEAD~1

# Discard changes completely (DANGEROUS)
git reset --hard HEAD~1

# Undo multiple commits
git reset --soft HEAD~3  # Last 3 commits
```

### Issue 3: Recover Deleted Branch

**Problem:** Accidentally deleted branch

**Solution:**

```bash
# Find commit SHA
git reflog

# Recreate branch
git checkout -b branch-name commit-sha
```

### Issue 4: Revert Pushed Commit

**Problem:** Need to undo commit that's already pushed

**Solution:**

```bash
# Create new commit that undoes changes
git revert commit-sha

# Revert multiple commits
git revert commit1 commit2 commit3

# Revert merge commit
git revert -m 1 merge-commit-sha
```

### Issue 5: Large File in History

**Problem:** Repository is too large due to committed large file

**Solution:**

```bash
# Remove file from all history (DANGEROUS)
git filter-branch --tree-filter 'rm -f large-file.zip' HEAD

# Or use BFG Repo-Cleaner (recommended)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files large-file.zip
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Issue 6: Merge Conflicts

**Problem:** Conflicts during merge

**Solution:**

```bash
# View conflicted files
git status

# Accept ours (current branch)
git checkout --ours file.txt
git add file.txt

# Accept theirs (other branch)
git checkout --theirs file.txt
git add file.txt

# Manual resolution
# Edit file, remove conflict markers
git add file.txt
git commit
```

### Issue 7: Wrong Branch

**Problem:** Made commits on wrong branch

**Solution:**

```bash
# Move commits to new branch
git branch new-branch
git reset --hard HEAD~3  # Remove last 3 commits from current
git checkout new-branch  # Commits are now on new branch

# Or cherry-pick to correct branch
git checkout correct-branch
git cherry-pick commit-sha
git checkout wrong-branch
git reset --hard HEAD~1
```

---

## Quick Reference

### Most Common Commands

```bash
# Status and diff
git status
git diff
git log --oneline

# Branch operations
git checkout -b feature-branch
git checkout main
git branch -d feature-branch

# Stage and commit
git add .
git commit -m "feat: add new feature"

# Sync with remote
git pull
git push

# Merge
git merge feature-branch

# Stash
git stash
git stash pop

# Undo
git reset --soft HEAD~1
git checkout -- file.txt
```

### Salesforce Development Workflow

```bash
# 1. Create feature branch
git checkout main
git pull origin main
git checkout -b feature/workflow-updates

# 2. Make changes and commit
git add force-app/main/default/classes/cmn_WorkflowNode.cls
git commit -m "feat(workflow): add node type validation"

# 3. Push feature branch
git push -u origin feature/workflow-updates

# 4. Keep branch updated
git checkout main
git pull origin main
git checkout feature/workflow-updates
git rebase main

# 5. After review, merge to main
git checkout main
git merge feature/workflow-updates
git push origin main

# 6. Clean up
git branch -d feature/workflow-updates
git push origin --delete feature/workflow-updates
```

---

## Related Documentation

- **Salesforce Development:** `Salesforce_Development_Master_Guide.md`
- **PowerShell Automation:** `MASTER_GUIDE_POWERSHELL_AUTOMATION.md`
- **Git Documentation:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-26 | Initial creation with comprehensive Git workflows |
