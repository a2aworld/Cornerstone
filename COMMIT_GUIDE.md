# Commit & Push Guide

This repository is the single source of truth. Commit regularly and push to GitHub so CI runs and collaborators can track progress.

## Regular commit workflow
1) Stage changes
```
cd /workspace/Cornerstone
git add .
```

2) Commit with a descriptive message
```
git commit -m "<what you changed and why>"
```

3) Push to GitHub
- SSH (recommended):
  - Ensure the SSH key is added in GitHub → Settings → SSH keys
  - Verify: `ssh -T git@github.com`
  - Push: `git push origin main`

- HTTPS + PAT (alternative):
  - Create a GitHub Personal Access Token
  - Set remote: `git remote set-url origin https://<USERNAME>:<TOKEN>@github.com/a2aworld/Cornerstone.git`
  - Push: `git push origin main`
  - Reset remote to clean URL afterwards.

## Commit cadence
- Commit after each significant step (scaffolding, new modules, tests, docs).
- Aim for small, atomic commits with clear messages.
- Tag milestones (e.g., v0.1.0) as releases.

## Troubleshooting push
- Permission denied (publickey): Add SSH key to GitHub and `ssh-keyscan github.com >> ~/.ssh/known_hosts`.
- Host key verification failed: ensure `~/.ssh/known_hosts` contains GitHub.

## On CI
- GitHub Actions runs on every push to `main`.
- Current CI: installs deps, verifies scaffolding, runs gateway smoke test.

## Branch protection (recommended)
- Protect `main` in repo settings; require passing status checks.

## Contact
support@a2aworld.ai
