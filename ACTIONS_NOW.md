# Cornerstone — Immediate Actions (Push + CI)

Status
- Local repo ahead of origin by 12 commits.
- Push blocked pending GitHub SSH key authorization.

Steps (do these now)
1) Add SSH public key to GitHub → Settings → SSH keys
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOS8jprpTdvS+AYCEbgB8NjxXunvcVM4jElstVguAMbE cornerstone@a2aworld.ai

2) Verify SSH from your sandbox
   ssh -T git@github.com

3) Push commits
   cd /workspace/Cornerstone
   git push origin main

4) Check CI
   - GitHub → Actions: CI should run and pass (scaffolding + gateway smoke test)

5) Notify
   - Tell me here when the push and CI complete. I’ll open Phase 1 issues and proceed with the next build steps.

Alternate (if SSH not possible):
- Use HTTPS + Personal Access Token (PAT): see PUSH_GUIDE.md Option A for one-time push instructions.
