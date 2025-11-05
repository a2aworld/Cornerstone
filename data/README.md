Data directory

Purpose
- Store public sample datasets for CI/dev.
- Register locations for proprietary premium seed dataset (9 CSV/KML) with ODRL metadata and EULA.

Structure
- data/public/: small open datasets for tests.
- data/premium/: placeholders only (no raw data checked into repo). In production, premium data lives in isolated storage (premium Postgres/S3) accessed via Premium Data Service.

Usage
- Do NOT commit proprietary CSVs to the public repo.
- For local dev, place copies under data/premium/local/ and set access flags in a local config (not committed).
- In SaaS, ingestion goes through Premium Data Service with consent/licensing checks.

Next
- After you upload your 9 CSVs to GitHub (private repo or secure storage), we will create ingestion scripts and ODRL provenance.
