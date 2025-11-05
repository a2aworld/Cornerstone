# Cornerstone Push Guide: Publish local commits to GitHub

Your repository is cloned and we committed `BLUEPRINT.md` locally (commit: see `git log`). The push failed due to missing GitHub credentials:

```
fatal: could not read Username for 'https://github.com': No such device or address
```

Use one of the methods below to authenticate and push.

---

## Option A — HTTPS with Personal Access Token (PAT)

1) Create a GitHub PAT (Fine‑grained token preferred)
- GitHub → Settings → Developer settings → Personal access tokens
- Scope: repository content (repo read/write). Limit to `a2aworld/Cornerstone` if using fine‑grained token.

2) Update the remote URL to embed credentials for a one‑time push
Replace `<USERNAME>` and `<TOKEN>` accordingly:

```
cd /workspace/Cornerstone
git remote set-url origin https://<USERNAME>:<TOKEN>@github.com/a2aworld/Cornerstone.git
```

3) Push the current branch
```
git push origin main
```

4) (Recommended) Remove embedded credentials from the remote URL after pushing
```
git remote set-url origin https://github.com/a2aworld/Cornerstone.git
```

Security note: Embedding tokens in URLs writes them to shell history. Consider clearing history or use SSH.

---

## Option B — SSH Keys

1) Generate a new SSH keypair in this environment
```
ssh-keygen -t ed25519 -C "a2aworld@a2aworld.ai" -f ~/.ssh/a2aworld_cornerstone -N ""
```

2) Add the public key to GitHub
- Copy `~/.ssh/a2aworld_cornerstone.pub` contents
- GitHub → Settings → SSH and GPG keys → New SSH key → paste the public key

3) Start agent and add the key
```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/a2aworld_cornerstone
```

4) Switch the remote to SSH and push
```
cd /workspace/Cornerstone
git remote set-url origin git@github.com:a2aworld/Cornerstone.git
git push origin main
```

---

## Option C — Push from your local machine
If you prefer, you can download the files and push from your local computer (with your existing credentials). Ensure the commit preserves authorship and timestamps.

---

## Current local state
- `BLUEPRINT.md` created and committed locally
- Run to confirm:
```
cd /workspace/Cornerstone
git log -1 --oneline --decorate
git status -sb
```

After authenticating via Option A or B, `git push origin main` will publish `BLUEPRINT.md` to GitHub.
