# Cornerstone — Immediate Next Steps

Status (local):
- BLUEPRINT.md added; scaffolding in place (LICENSE, README, CI, brand guide, docs, gateway code, Docker).
- Local commits ahead of origin by 10; push pending GitHub auth.

Action 1 — Push local commits to GitHub
- Follow PUSH_GUIDE.md for HTTPS (PAT) or SSH.
- Recommended: SSH
  1) ssh-keygen -t ed25519 -C "a2aworld@a2aworld.ai" -f ~/.ssh/a2aworld_cornerstone -N ""
  2) Add ~/.ssh/a2aworld_cornerstone.pub to GitHub → Settings → SSH keys
  3) git remote set-url origin git@github.com:a2aworld/Cornerstone.git
  4) git push origin main
- Alternative (PAT): Update origin with https://<USERNAME>:<TOKEN>@github.com/a2aworld/Cornerstone.git, push, then reset origin to clean URL.

Action 2 — Seed data onboarding (copyrighted 9 CSV/KML)
- Do not commit proprietary data to public repo.
- Upload to secure storage (private repo, S3, or provide direct files privately).
- We will ingest via Premium Data Service with ODRL metadata and provenance.

Action 3 — Open Phase 1 GitHub Issues (after push)
- A2A Method Registry & Manifests
- A2A Gateway: envelope signing/verification, capability negotiation
- Internal agent stubs (MythText, GeoLinker, TimeAlign, DataFusion, Hypothesis, Viz, Ethics)
- CI conformance harness (A2A interop)

Action 4 — Dev stack expansion
- Extend docker-compose with PostGIS, Neo4j, Redis, MinIO
- Add service configs and health checks

Action 5 — Mentorship prep (Week 1)
- Creative Brief v1
- Mood Boards v1 (palettes, textures)
- Initial Data Art sketches (motif constellations, uncertainty ribbons)

Reference files:
- BLUEPRINT.md — Master plan
- PUSH_GUIDE.md — Push instructions
- docs/geomythology.md — Genesis Challenge overview
- docker-compose.yml — Gateway container (foundation)

Contact: support@a2aworld.ai
