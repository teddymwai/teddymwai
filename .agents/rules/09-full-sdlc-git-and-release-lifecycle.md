# Full-SDLC Engineering, Git Hygiene & Release Promotion Lifecycle

Every agent and contributor operating in this repository must follow this five-stage Software Development Lifecycle (SDLC) distilled from production test orchestration and security engineering engagements.

---

## Stage 1: Dev Planning & Architectural Triage

1. **"Critic Before Code" (`ADOPT` / `REJECT` / `HOLD` Triage)**:
   - Before writing code for a multi-component feature or architectural proposal, evaluate trade-offs explicitly.
   - Classify each proposed element as **`ADOPT`** (high net-gain, low tech-load), **`REJECT`** (over-engineered, speculative, or violates invariants), or **`HOLD`** (defer until prerequisite seams stabilize).
   - Never modify production or harness code during a review/critique turn when the operator asks to assess or plan first.
2. **Contracts & Seams First (Anti-Seam-Rot Mandate)**:
   - Author declarative schemas and contracts (`manifest.toml`, `<suite_code_lower>.contract.toml`, `verdict.schema.json`, `events.jsonl`, `control.json`) before building UI control planes.
   - **The CLI must be the first consumer of every seam.** A seam consumed only by tests or only by a GUI will rot.
3. **1:1 Registry $\leftrightarrow$ Manifest $\leftrightarrow$ Physical Spec-on-Disk Parity**:
   - Every suite or capability registered in code must have an entry in the governance manifest (`manifest.toml`) and a physical, non-empty markdown specification on disk under `specs/`.
   - Every mutating specification or contract must define four explicit lifecycle blocks:
     - **`[needs]`**: Preconditions, required actor roles/capabilities, and target state.
     - **`[uses]`**: Target services, REST endpoints, and UI routes.
     - **`[produces]`**: Created entities, state mutations, and output artifacts.
     - **`[decommission]`**: Affirmative teardown commands and follow-up absence verification probes.
4. **Tiered Docs-as-Code & Single Canonical Roadmap**:
   - **In Git**: Formal specifications (`specs/`), architectural constitutions (`AGENTS.md`, `HARNESS.md`), release register (`docs/RELEASE_REGISTER.md`), paginated changelog (`CHANGELOG.md`), and a **single consolidated roadmap** (`docs/UPCOMING_FEATURES.md` organized by domain). Never create fragmented `RELEASE_NOTES_NEXT.md` files.
   - **Historical Archive**: Move superseded release notes to `docs/releases/archive/` and wrap historical `CHANGELOG.md` sections in collapsible `<details>` blocks so the active release stays prominent at the top.
   - **Externalized to Notion**: Volatile daily sprint trackers, manual QA checklists, and morning scratchpads belong in Notion (referenced via `docs/trackers/README.md`) to prevent repository documentation bloat.
5. **Local Workstation Storage Mandate**:
   - Always locate active git workspaces on local disk (e.g., `/Users/ted/Development/<Project>`). Never run active git repositories inside cloud-synced folders (OneDrive, iCloud, Dropbox) where macOS "dataless" stub files corrupt `.git/` objects during unsupervised runs.

---

## Stage 2: In-Development Standards & Runtime Resilience

1. **Decoupled Package Architecture & Strict Import Boundaries**:
   - Maintain clean separation between foundational infrastructure (`lib/framework/` or core engine package) and domain suites/tools (`lib/suites/`, `tools/`).
   - **Strict Boundary Rule**: Internal modules must never import from root-level backwards-compatibility shims. Enforce this via AST import-boundary checks in `--selftest`.
2. **Dynamic Asset Discovery & Reverse-Order Teardown (Zero Hardcoded IDs)**:
   - Never hardcode tenant-specific entity IDs (playlist IDs, scenario UUIDs, user roles) that vary across deployments.
   - Discover target entities dynamically with fallback chains, or self-provision ephemeral fixtures prefixed with `pw-tc-<hex8>`.
   - Tear down created fixtures in **reverse dependency order** (e.g., decommission child lobby before disbanding parent team). Only auto-delete entities carrying the `pw-tc-` test prefix; leave pre-existing tenant entities untouched.
3. **Subprocess Isolation, Concurrency Semaphores & Graceful Signal Drain**:
   - Execute stateful or browser-driving suites in isolated subprocesses (`--emit-result-file`) so Playwright/asyncio loops never leak across suites.
   - Enforce multi-tier concurrency semaphores (e.g., `5 Booting / 7 Running / 3 Terminating`) and dynamic rate-limit backoff for heavy infrastructure operations.
   - **Deterministic Signal & File-Based IPC Protocol**:
     - `1st SIGINT` / `SIGTERM` / `SIGUSR1` / `control.json ("pause")`: Graceful drain to next safe barrier, write atomic checkpoint (`temp -> fsync -> os.replace`), and exit with code `3`.
     - `2nd SIGINT` / `control.json ("abort")`: Emergency escalation—abort active step and drain the `pending_cleanup` teardown queue.
   - **Crash Discovery & Orphan Purging (`_runs/index.jsonl`)**: Track active run PIDs in an append-only index; detect stale locks (dead PID + lock age > 60s) and support `--list-runs --orphaned`, `--resume-latest`, and `--cleanup-orphans`.
4. **Mandatory 5-Section Tool `README.md` & Environment Preflight (`doctor.py`)**:
   - Every directory under `tools/<tool>/` must contain a dedicated `README.md` with:
     1. *Architectural Overview*
     2. *Deployment & Environment Resolution*
     3. *Credential & Authentication Guide*
     4. *How to Run* (exhaustive, copy-pasteable CLI commands for standard, staging, and resume runs)
     5. *Output Artifacts*
   - Provide an offline environment preflight (`tools/doctor.py` + `docs/SETUP_GUIDE.md`) to catch missing dependencies or typing imports before runtime.
5. **Zero-Speculative Bypass & Developer Escalation Ledger (`LEDGER-XX`)**:
   - When blocked by missing credentials, isolated network VLANs/VPNs, or a hard backend defect, **never** invent fake mocks, hardcode bypasses, or weaken assertions. Record the blocker in the **Developer Redesign & Input Ledger**:

   | Item Code | Affected Component | Category | Description & Blocker | Required Developer / Operator Input | Recommended Action / Redesign Path |
   | :--- | :--- | :--- | :--- | :--- | :--- |
   | `LEDGER-01` | `<path>` | `Credentials` / `Infra` / `UI` / `Schema` | `<concise root cause>` | `<exact input needed>` | `<concrete remediation>` |

6. **Dual Reporting Contract (`verdict.json` + `run-report.md` AND UltraRed `mainReport.md`)**:
   - **Suite & Tool Runs**: Emit `verdict.json` (schema v1.0.0 with git SHA, target version, redaction proof, check list, and artifact map), `run-report.md`, and optional `walkthrough.html` under `output/<deployment>/<tool>/<YYYY-MM-DD_HHMMSS>/`.
   - **Security & Repository Audits (UltraRed Reporting Engine)**: Emit `<projectTitle>_<YYYYMMDD_HHMMSS>/` containing `mainReport.md`, `findings.json`, and `summary.json` structured with:
     - **Executive Scorecard** (`Total Inspected Files`, `Verified Safe Invariants`, `Immediate Attention`, `Other Items Needing Attention`, `Overall Measured Impact X/Y denominator`, `Posture Status: ALL_SAFE | ADVISORY | NEEDS_IMMEDIATE_ACTION`)
     - **1. What Was Run** (active engines, target path, mode, profile, commit SHA, duration, host)
     - **2. What Was Safe** (Verified Policy Invariants `[PASS]`, Falsified Candidates `[DISPROVED]`, Clean Surfaces `[CLEAN]` — *eliminations require evidence*)
     - **3. What Needs Immediate Attention** (Critical/High passing all 3 Hard Gates, deduplicated by `(root_cause, component, prerequisite)`, with numbered reproduction steps, proof evidence, and remediation)
     - **4. Other Items That Need Attention (Not Severe)** (Medium/Low and hardening advisories)
     - **5. Pre-Submission Rubric Self-Verification** (ARTEX 7-Check Oracle compliance).

---

## Stage 3: Pre-Commit & The 7-Check "Forgotten Bits" Sanitization Gate

Before committing or promoting any branch, execute all seven checks:

1. **Check 1 — Full-Tree Bytecode & Syntax Compilation**:
   ```bash
   python3 -m compileall -q lib tools tests templates
   ```
   Must exit `0` across 100% of files (catches syntax errors, malformed f-strings, and missing `typing` imports).
2. **Check 2 — 1:1 Registry, Manifest & Physical Spec-on-Disk Self-Test**:
   - Run offline harness self-tests (`--selftest`) confirming every registered suite exists in `manifest.toml`, every `default_spec` physically exists on disk, and AST import boundaries are unbroken.
3. **Check 3 — Contract Canonicalization & Unit Tests**:
   - Confirm contracts follow `<suite_code_lower>.contract.toml` with zero squashed duplicates (`mp01` vs `mp_01`) and affirmative `[produces]` / `[decommission]` hooks.
4. **Check 4 — Tool Architecture Rule #4 & Legacy Quarantine**:
   - Every `tools/<tool>/` has a 5-section `README.md`; dashboards are named `<tool>_dashboard.html`; zero active scripts contain hardcoded cookie placeholders (`<YOUR_PROD_SESSION_COOKIE>`); legacy scripts are quarantined under `tools/legacy/archive/`.
5. **Check 5 — Tiered Documentation & Release Register Synchronization**:
   - Verify `CHANGELOG.md`, `docs/RELEASE_REGISTER.md`, `docs/UPCOMING_FEATURES.md`, and `docs/releases/RELEASE_NOTES_*.md` reflect matching version tags, Ptarmigan (*Lagopus*) taxonomic codenames, dates, and commit SHAs.
   - **Tests & Docs Ship With the Feature**: Never defer tests or documentation updates to a later commit.
6. **Check 6 — TedRedCraft Tier 1 Pre-Commit SAST (<1.5s)**:
   ```bash
   python3 -m redcraft audit --target . --mode pre-commit
   ```
7. **Check 7 — Explicit Staging & Secret/Path Regex Interception**:
   - Inspect untracked and modified files (`git status --short --branch`, `git ls-files --others --exclude-standard`).
   - **Stage explicit file paths only** (`git add <path1> <path2>`); **never use `git add -A` or `git add .`**.
   - Run mandatory staged path and secret scans (must return zero matches):
     ```bash
     git diff --cached --name-only | grep -E '(^|/)(creds([.]|$)|\.session_cache\.json|\.venv|output/.*/(responses|screenshots)|.*\.har$|.*\.zip$|\.DS_Store)'
     git diff --cached | grep -Ein 'authorization|bearer |set-cookie|password|access_token|refresh_token|sessionid'
     git diff --cached --check
     ```

---

## Stage 4: Senior-Engineer Commit Messaging & Blast-Radius Audit

Commits must be atomic, single-purpose, and formatted with an explicit blast-radius declaration:

```text
type(scope): imperative summary <= 72 chars

Why: 1-3 lines explaining what changed, the root cause, and what it replaces.
Trade-off: architectural forks, performance vs. memory trade-offs, or deferrals; omit if none.

Touches: AREA1, AREA2, AREA3
Refs: #PR or issue number
```

- **Allowed `type` values**: `feat`, `fix`, `test`, `refactor`, `docs`, `perf`, `chore`.
- **Commit Subject Integrity**: When the operator specifies an exact commit subject line, preserve that requested first line **verbatim** while still structuring the commit body with `Why:`, `Trade-off:`, and `Touches:`.
- **Never Amend Pushed Commits**: Once a commit is pushed to any remote branch, never rewrite or `--amend` it; push a forward fix commit instead.
- **Blast-Radius Areas (`Touches:`)**: Audit changes against `Specs`, `Framework Core`, `Test Suites`, `Deployments & Config`, `Operational Tools`, `Golden Baselines`, `UI & Dashboards`, `HAR Wire Reference`, `Docs & Trackers`, or `none (internal)`.

---

## Stage 5: Push Strategies, 3-Tier Branch Promotion & History Governance

### A. 3-Tier Branch Isolation & Fast-Forward Promotion Pipeline
```text
beta/unstable-nightly (or beta-<Feature>) ──(Regression Certification)──> staging ──(Fast-Forward GA)──> main
```
1. **Nightly / Beta Incubator (`beta/unstable-nightly` or `beta-<Codename>`)**:
   - Dedicated channel for rapid iteration, orchestrator state machines, experimental contracts, and new reporting engines.
   - Before committing experimental or orchestrator changes, affirmatively verify `git branch --show-current`.
2. **Staging Integration (`staging`)**:
   - Pre-release certification branch validated against the staging environment and TedRedCraft Tier 2 Loopback DAST (`python3 -m redcraft audit --target . --mode pre-push`, `<4s`).
3. **Production Baseline (`main`)**:
   - Strictly stable and certified. Direct commits to `main` and `git push --force` on shared branches (`beta/*`, `staging`, `main`) are strictly prohibited.
   - **Fast-Forward Promotion Sequence**:
     ```bash
     git fetch origin
     git merge-base --is-ancestor origin/main origin/staging
     git switch main
     git pull --ff-only origin main
     git merge --ff-only origin/staging
     git tag -a "<LagopusIdentifier>" -m "{{PROJECT_NAME}} Platform <vX.Y.Z> - <Lagopus Species Subspecies>"
     git push origin main --follow-tags
     ```
   - **GitHub Release Publication**: Whenever a release tag is pushed, publish or update the corresponding GitHub Release (`gh release create <tag> --title "..." --notes-file docs/releases/RELEASE_NOTES_vX.Y.Z.md`) with comprehensive release notes so GitHub Releases never lag behind git tags.

### B. The "Commit-and-Purge" Pattern for Historical Legacy Scripts
When deprecated or legacy proof-of-concept scripts should be preserved in git lineage for historical reference without cluttering the active working tree:
1. **Commit 1 (Archive)**: Sanitize all tokens/cookies to placeholders, strip executable bits, place under `tools/legacy/archive/`, and commit:
   `chore(archive): restore sanitized legacy sample scripts for historical reference`
2. **Commit 2 (Purge from Active Tree)**: Immediately remove `tools/legacy/` in the next commit and reference Commit 1's short SHA in the subject:
   `Cleaned up legacy files - see prev <short-sha> for legacy details.`
   *(Historical files remain permanently retrievable via `git checkout <short-sha> -- tools/legacy/` while keeping the active branch 100% clean.)*

### C. Emergency Secret Remediation & Remote Tag Governance (`GH013`)
1. **Deleting Protected Tags Attached to GitHub Releases (`GH013`)**:
   - If `git push origin --delete <tag>` fails with `remote: error: GH013: Repository rule violations found`, do not attempt force-pushing. The tag is locked by a published GitHub Release.
   - Delete both the release and underlying git ref cleanly via GitHub CLI:
     ```bash
     gh release list --repo <owner/repo>
     gh release delete <tag_name> --repo <owner/repo> --yes --cleanup-tag
     ```
2. **Clean-Slate Orphan History Reset**:
   - If historical commits across branches contain exposed secrets and interactive rebase causes intractable conflicts:
     ```bash
     cp -R .git ../repo_git_backup
     git checkout --orphan clean-slate
     git add <explicit-sanitized-paths>
     git commit -m "feat(release): initial clean-slate release of {{PROJECT_NAME}}"
     git branch -M main
     git push origin main --force
     git push origin main:staging --force
     git push origin main:beta/unstable-nightly --force
     ```
