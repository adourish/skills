# Skill: Push to All Remotes

Push the current branch to both configured remotes: Azure DevOps (`origin`) and GitHub (`github`).

## When to Use

- After committing changes you want synced to both repos
- User says "push to both repos", "push everywhere", "sync all remotes"

## Remotes

| Remote | URL |
| --- | --- |
| `origin` | Azure DevOps — `https://dev.azure.com/reihsbu/TEG/_git/POCs` |
| `github` | GitHub — `https://github.com/adourish/FY25-System-Optimization-and-Automation-Enhancements` |

## Steps

1. Get the current branch name
2. Push to `origin`
3. Push to `github`
4. Report results for both

## Commands

```bash
# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push to Azure DevOps
git push origin "$BRANCH"

# Push to GitHub
git push github "$BRANCH"
```

## Notes

- If the branch doesn't exist on GitHub yet, add `-u` to set upstream: `git push -u github "$BRANCH"`
- Never force-push to `main` on either remote without explicit user confirmation
- If credentials fail for GitHub, the token is stored in the `github` remote URL — check `git remote -v` and update with `git remote set-url github https://<token>@github.com/adourish/FY25-System-Optimization-and-Automation-Enhancements.git`
- Azure DevOps may prompt for credentials via the Windows Credential Manager
