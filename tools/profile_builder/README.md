# Profile Builder (`tools/profile_builder`)

## 1. Architectural Overview
`build.py` is a zero-dependency Python 3.9+ standard-library generator that compiles `data/profile.json` and the Edulis Unified Signet (`assets/brand/edulis-signet-gold.svg`) into:
- Dual-polarity (`dark` / `light`) SVG hero and lane header cards under `assets/cards/`.
- Marker-delimited Markdown sections (`<!-- BEGIN:<key> -->` ... `<!-- END:<key> -->`) inside `README.md`.

It enforces the repository's Living Invariants (`AGENTS.md`): zero emojis, canonical `TedCraft, a publication of Edulis Secure Systems Hub Limited` attribution, uppercase `CYBER RANGES` nomenclature, no private repository hyperlinks, and valid XML SVG output.

## 2. Deployment & Environment Resolution
Runs locally on macOS/Linux and inside GitHub Actions (`ubuntu-latest`) using the system `python3` binary (3.9+). No virtual environment or third-party `pip` packages are required.

## 3. Credential & Authentication Guide
No credentials, tokens, or API keys are required.
- `--feed` fetches the public RSS endpoint `https://tedcraft.dev/rss.xml` over HTTPS.
- `--check-links` issues unauthenticated HTTP `HEAD` requests to public links in `data/profile.json`.

## 4. How to Run

```bash
# Regenerate SVG cards and README.md sections from data/profile.json
python3 tools/profile_builder/build.py

# Refresh the Latest from TedCraft RSS block
python3 tools/profile_builder/build.py --feed

# Verify committed README.md and SVGs match data/profile.json (CI drift gate)
python3 tools/profile_builder/build.py --check

# Run policy and XML self-tests (add --check-links for live HTTP verification)
python3 tools/profile_builder/build.py --selftest
python3 tools/profile_builder/build.py --selftest --check-links

# Run unit tests
python3 -m unittest discover -s tools/profile_builder -v
```

## 5. Output Artifacts

```text
assets/cards/
├── hero-dark.svg
├── hero-light.svg
├── lane-shipped-dark.svg
├── lane-shipped-light.svg
├── lane-inflight-dark.svg
├── lane-inflight-light.svg
├── lane-horizon-dark.svg
└── lane-horizon-light.svg
```
`README.md` is updated in-place strictly between `<!-- BEGIN:<key> -->` and `<!-- END:<key> -->` markers.
