# Changelog & Architectural Release Lineage (`CHANGELOG.md`)

All notable architectural enhancements, security invariants, and showcase updates for **Ted Mwai Profile** are documented in this file.

- **Release Nomenclature**: Strictly governed by the Ptarmigan (*Lagopus*) taxonomic specification ([`docs/releases/LAGOPUS_NOMENCLATURE_SPEC.md`](docs/releases/LAGOPUS_NOMENCLATURE_SPEC.md)).
- **Release Index**: Canonical tags, branches, and commit SHAs are synchronized in [`docs/RELEASE_REGISTER.md`](docs/RELEASE_REGISTER.md).

---

## [v1.0.0 — 2026-11-25] Lagopus (Ted Mwai × Edulis SSH Profile Rewrite)

| Field | Value |
| :--- | :--- |
| **Taxonomic Identifier** | `Lagopus_v1.0.0` |
| **Stage / Branch** | `GA` (`main`) |
| **Primary Subsystems** | `data/profile.json` single source of truth, `tools/profile_builder/build.py` stdlib generator, dual-polarity SVG cards, Edulis Unified Signet (`V3.2B-1`), CI drift/policy gates, weekly TedCraft RSS sync |
| **Validation Status** | `compileall -q tools`, `build.py --selftest --check-links`, `build.py --check`, `unittest` (5/5), and `xmllint` passed with 0 policy violations. |

### Architectural Updates
- Replaced legacy CV-style `readme.md` and unconfigured `tedtencent.yml` boilerplate with a deterministic profile generator backed by `data/profile.json`.
- Structured works into **Shipped** (past), **In Flight** (present), and **On the Horizon** (future) lanes with strict `PRIVATE` labelling and zero private repository hyperlinks.
- Embedded the **Edulis Secure Systems Hub Limited** institutional charter and **TedCraft** publication attribution (`TedCraft, a publication of Edulis Secure Systems Hub Limited`).
- Added `.github/workflows/profile-ci.yml` (drift, selftest, unit tests, SVG XML, secret scan) and `.github/workflows/tedcraft-feed.yml` (weekly Monday 06:00 UTC RSS refresh).
