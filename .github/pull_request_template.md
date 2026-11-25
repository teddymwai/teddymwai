# Ted Mwai Profile Pull Request & 3-Tier Release Promotion Review Template

Use this template for all Pull Requests and promotion reviews targeting `beta/unstable-nightly` (or `beta-<Feature>`), `staging`, and `main`.

---

## 1. Release Identification & Branch Metadata

| Field | Value |
| :--- | :--- |
| **Product / Suite Scope** | `Ted Mwai Profile` |
| **Taxonomic Release Identifier** | `<Lagopus[Species][Subspecies]_vMAJOR.MINOR.PATCH[-STAGE.N][+BUILD]>` |
| **Human-Readable Release Title** | `Ted Mwai Profile Platform <vMAJOR.MINOR.PATCH> - <Lagopus Species Subspecies>` |
| **Source Branch -> Target Branch** | `<branch>` -> `<beta/unstable-nightly / staging / main>` |
| **Reviewed Commit SHA & Subject** | `<short-sha>` - `<exact commit subject>` |
| **Promotion Requested** | `<Nightly Verification / Staging Candidate / Fast-Forward Promotion to main>` |

---

## 2. Pre-Commit & Pre-Promotion Automated Validation Gates (The 7 Checks)

All automated validation gates must pass locally before staging or pushing:

| Gate | Validation Command | Result (`PASS` / `FAIL`) | Notes |
| :--- | :--- | :---: | :--- |
| **Gate 1: Bytecode Compilation** | `python3 -m compileall -q lib tools tests templates` | `<PASS / FAIL>` | 100% clean syntax & imports |
| **Gate 2: Harness Self-Test & Parity** | `python3 -m lib.runner --selftest` *(or template selftests)* | `<PASS / FAIL>` | 1:1 registry/manifest/spec-on-disk & AST boundaries |
| **Gate 3: Contract & Unit Tests** | `python3 -m unittest discover -s tests` | `<PASS / FAIL>` | Canonical `<suite_code_lower>.contract.toml` & hooks |
| **Gate 4: Tool & Dashboard Audit** | Verify 5-section `README.md` & `<tool>_dashboard.html` | `<PASS / FAIL>` | 7 interactive capabilities & `--dashboard` lifecycle |
| **Gate 5: Docs & Register Sync** | Verify `CHANGELOG.md`, `RELEASE_REGISTER.md`, `UPCOMING_FEATURES.md` | `<PASS / FAIL>` | Matching SHAs, dates, and Lagopus tags |
| **Gate 6: RedCraft Tier 1 SAST** | `python3 -m redcraft audit --target . --mode pre-commit` | `<PASS / FAIL>` | `<1.5s` staged SAST, `SEC-01..04`, secret & `.har` check |
| **Gate 7: RedCraft Tier 2 DAST** | `python3 -m redcraft audit --target . --mode pre-push` | `<PASS / FAIL>` | `<4s` ephemeral loopback DAST & socket lease closeout |

---

## 3. Live Suite Execution & Mutation Audit

Record every suite or tool verified against target environments:

| Suite / Tool ID | Category / Name | Target Deployment (`staging` / `prod`) | Mode (`read-only` / `--allow-mutation`) | Result (`PASS` / `FAIL` / `NOT RUN`) | Affirmative Teardown Verified |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `<SUITE-ID>` | `<e.g., Baseline Smoke>` | `staging` | `read-only` | `<PASS / FAIL>` | `N/A (read-only)` |
| `<SUITE-ID>` | `<e.g., Stateful Lifecycle>` | `staging` | `--allow-mutation` | `<PASS / FAIL>` | `<Yes / No / N/A>` |

> [!NOTE]
> Production is strictly read-only by default. Mutating runs against production require explicit single-run operator authorization (`--allow-mutation` and `PROD-MUTATE`).

---

## 4. Artifact Sanitization & Secret Scan Checklist

Verify all items before committing or merging:

- [ ] Worktree and untracked file list inspected (`git status --short --branch`, `git ls-files --others --exclude-standard`).
- [ ] Explicit file paths staged; `git add -A` and `git add .` were **NOT** used.
- [ ] Tests, 5-section tool `README.md`, `CHANGELOG.md`, and `docs/UPCOMING_FEATURES.md` ship in the same commit as the feature.
- [ ] Zero credentials (`creds*.txt`), `.session_cache.json`, cookies, bearer tokens, or passwords staged.
- [ ] Zero raw runtime `output/` subdirectories (`responses/`, `screenshots/`, `wire.har`) staged.
- [ ] Staged path and secret audit passed with **zero** matches:
  - `git diff --cached --name-only | grep -E '(^|/)(creds([.]|$)|\.session_cache\.json|\.venv|output/.*/(responses|screenshots)|.*\.har$|.*\.zip$|\.DS_Store)'`
  - `git diff --cached | grep -Ein 'authorization|bearer |set-cookie|password|access_token|refresh_token|sessionid'`
  - `git diff --cached --check`
- [ ] **Release Nomenclature**: Git tag and PR title strictly conform to the **Ptarmigan (*Lagopus*) specification** (`docs/releases/LAGOPUS_NOMENCLATURE_SPEC.md`).
- [ ] **UI Base Mantra & Interactive Dashboard Standard**: Grounded in `#0e3f2a` / `#0d1310`, Studio Curve (`img001.jpg`) composite canvas, zero emojis, vector icons only, Apple HIG 44px capsules, `TooltipManager`, and full interactive run creation/monitoring/409-reset controls.

---

## 5. Included Files, Exclusions, and Known Gaps (`LEDGER-XX`)

- **Staged & Published Files (`Touches:`)**:
  - `<path/to/file_1>`
- **Excluded Local / Sensitive Artifacts**:
  - `<list local captures, outputs, or configs intentionally left unstaged>`
- **Known Coverage Gaps or Developer Escalation Ledger Items (`LEDGER-XX`)**:
  - `<list open items or LEDGER-XX rows>`

---

## 6. Fast-Forward Main Promotion & GitHub Release Sign-Off

- [ ] `git merge-base --is-ancestor origin/main origin/staging` verified clean fast-forward ancestry.
- [ ] Fast-forward merge completed (`git switch main && git pull --ff-only origin main && git merge --ff-only origin/staging`).
- [ ] Annotated taxonomic release tag applied (`git tag -a "<LagopusIdentifier>" -m "Ted Mwai Profile Platform <vX.Y.Z> - <Lagopus Lineage>"`).
- [ ] Pushed to `main` with tags (`git push origin main --follow-tags`) and verified `origin/main` SHA matches `origin/staging`.
- [ ] `docs/RELEASE_REGISTER.md` updated and verbose GitHub Release published (`gh release create "<LagopusIdentifier>" --notes-file ...`).

**Reviewer Sign-Off**: ____________________________  
**Role / Title**: Ted Mwai, Release Approver / Lead  
**Date**: `YYYY-MM-DD`
