---
name: "sdlc-git-release-lifecycle"
description: "Execute the end-to-end Software Development Lifecycle (SDLC): dev planning (ADOPT/REJECT/HOLD triage, anti-seam-rot contracts), in-development standards, the 7-Check Pre-Commit Sanitization Gate, Senior-Engineer commit messaging (Why/Trade-off/Touches), UltraRed & verdict reporting, 3-tier branch promotion (beta/unstable-nightly -> staging -> main), Commit-and-Purge legacy handling, and GH013 release tag governance."
---

# End-to-End SDLC, Git Hygiene & Release Promotion Lifecycle Skill

Distilled from `CYBER RANGES Agents/docs/push2git.md`, `CYBER RANGES Agents/.agents/rules/agent-harness.md`, and `TedRedCraft/AGENTS.md`.

## When to Activate
- When planning or critiquing new features, refactors, or test suites (`/plan`, `/grill-me`).
- Before staging, committing, tagging, or pushing changes to git.
- When curating release notes, updating `CHANGELOG.md`, `docs/UPCOMING_FEATURES.md`, or `docs/RELEASE_REGISTER.md`.
- When promoting changes across `beta/unstable-nightly`, `staging`, and `main`, or remediating git history and GitHub release tags (`GH013`).

---

## 1. Dev Planning & Architecture Gate

1. **Critic Before Code (`ADOPT` / `REJECT` / `HOLD`)**:
   - Evaluate architectural proposals against Net-Gain vs. Tech-Load before writing code.
   - Classify items into `ADOPT`, `REJECT`, or `HOLD`.
2. **Contracts & Seams First (Anti-Seam-Rot)**:
   - Define machine-readable contracts (`manifest.toml`, `<suite_code_lower>.contract.toml`, `verdict.schema.json`, `events.jsonl`, `control.json`) first.
   - Ensure the CLI runner is the first consumer of every contract seam before wiring the web dashboard.
3. **1:1 Registry $\leftrightarrow$ Manifest $\leftrightarrow$ Physical Spec Parity**:
   - Every registered suite/module must have a physical markdown spec under `specs/` and an entry in `manifest.toml`.
   - Mutating contracts must declare `[needs]`, `[uses]`, `[produces]`, and `[decommission]`.
4. **Single Roadmap & Tiered Docs**:
   - Consolidate all forward-looking features in `docs/UPCOMING_FEATURES.md` grouped by domain.
   - Keep active release notes at the top of `CHANGELOG.md` and wrap older releases in `<details>` blocks; move archived release docs to `docs/releases/archive/`.

---

## 2. Pre-Commit: The 7-Check "Forgotten Bits" Sanitization Gate

Run all 7 checks before staging and committing:

```bash
# 1. Inspect worktree & untracked files
git status --short --branch
git diff --stat
git ls-files --others --exclude-standard

# 2. Check 1: Full-tree bytecode compilation
python3 -m compileall -q lib tools tests templates 2>/dev/null || python3 -m compileall -q .

# 3. Check 2 & 3: Offline harness selftests & contract/unit tests
# (Run project --selftest and unittest/pytest suites)

# 4. Check 6: TedRedCraft Tier 1 Pre-Commit SAST (<1.5s)
PYTHONPATH=/Users/ted/Development/TedRedCraft python3 -m redcraft audit --target . --mode pre-commit

# 5. Stage EXPLICIT file paths only (NEVER git add -A or git add .)
# git add <path1> <path2>

# 6. Check 7: Staged path, secret & whitespace interception (must return 0 matches)
git diff --cached --name-only | grep -E '(^|/)(creds([.]|$)|\.session_cache\.json|\.venv|output/.*/(responses|screenshots)|.*\.har$|.*\.zip$|\.DS_Store)'
git diff --cached | grep -Ein 'authorization|bearer |set-cookie|password|access_token|refresh_token|sessionid'
git diff --cached --check
```

---

## 3. Senior-Engineer Commit Message & Blast-Radius Protocol

Format every commit message with an explicit blast-radius declaration:

```text
type(scope): imperative summary <= 72 chars

Why: 1-3 lines explaining what changed, the root cause, and what it replaces.
Trade-off: architectural forks, performance vs. memory trade-offs, or deferrals; omit if none.

Touches: AREA1, AREA2, AREA3
Refs: #PR or issue
```

- **Commit Subject Integrity**: If the operator specifies an exact commit subject line, preserve that subject line **verbatim** on line 1 while structuring the body with `Why:`, `Trade-off:`, and `Touches:`.
- **Blast-Radius Areas (`Touches:`)**: `Specs`, `Framework Core`, `Test Suites`, `Deployments & Config`, `Operational Tools`, `Golden Baselines`, `UI & Dashboards`, `HAR Wire Reference`, `Docs & Trackers`, or `none (internal)`.

---

## 4. Push, 3-Tier Fast-Forward Promotion & History Governance

1. **3-Tier Branch Progression**:
   - `beta/unstable-nightly` (or `beta-<Feature>`) $\rightarrow$ `staging` (run Tier 2 Loopback DAST: `python3 -m redcraft audit --target . --mode pre-push`) $\rightarrow$ `main` (fast-forward `--ff-only` merge only).
   - Never commit directly to `main`; never force-push shared branches; never `--amend` commits already pushed to remote.
2. **GitHub Release Synchronization**:
   - Pair every annotated Ptarmigan (*Lagopus*) tag with verbose GitHub Release notes (`gh release create <LagopusTag> --title "..." --notes-file docs/releases/RELEASE_NOTES_vX.Y.Z.md`).
3. **Commit-and-Purge Legacy Reference Pattern**:
   - Commit 1: `chore(archive): restore sanitized legacy sample scripts for historical reference` (all tokens redacted, exec bits removed).
   - Commit 2: `Cleaned up legacy files - see prev <short-sha> for legacy details.` (removes `tools/legacy/` from active tree while preserving `git checkout <sha> -- tools/legacy/`).
4. **Deleting Protected GitHub Release Tags (`GH013`)**:
   - Use `gh release delete <tag_name> --repo <owner/repo> --yes --cleanup-tag` when a tag is locked by a published GitHub Release.
