---
name: lagopus-release-orchestrator
description: Plan, resolve, validate, and execute software releases using the Ptarmigan (Lagopus) biological taxonomic nomenclature paired with Semantic Versioning. Use when tagging releases, updating docs/RELEASE_REGISTER.md, cutting release branches, or preparing PRs.
---

# Lagopus Taxonomic Release Orchestration Skill

This skill governs the systematic generation, validation, and recording of software releases adhering to the **ptarmigan genus (*Lagopus*)** biological taxonomy.

---

## 1. When to Activate
- When the user asks to prepare, cut, or tag a new release.
- When generating a PR title or description for release promotion from staging to main.
- When updating or auditing `docs/RELEASE_REGISTER.md`.

---

## 2. Dynamic Resolution Procedure

### Step 1: Query History & Existing Taxa
Run git tag discovery to identify the latest release and consumed subspecies:
```bash
git tag -l "Lagopus*" --sort=-v:refname | head -n 10
```
Also inspect `docs/RELEASE_REGISTER.md`.

### Step 2: Resolve the Next Taxon & Tag

Follow the taxonomic decision tree:
1. **Patch Bump (`vX.Y.Z` $\rightarrow$ `vX.Y.(Z+1)`)**:
   - Retain existing species and subspecies prefix.
   - Example: `LagopusMutaHelvetica_v2.1.0` $\rightarrow$ `LagopusMutaHelvetica_v2.1.1`
2. **Pre-Release Stage Promotion (`vX.Y.Z-rc.1` $\rightarrow$ `vX.Y.Z`)**:
   - Retain parent taxon prefix, strip stage suffix.
   - Example: `LagopusLeucura_v3.0.0-rc.1` $\rightarrow$ `LagopusLeucura_v3.0.0`
3. **Major Bump (`v(X+1).0.0`)**:
   - Advance species: `v1.x` = `Lagopus`, `v2.x` = `LagopusMuta`, `v3.x` = `LagopusLeucura`, `v4.x` = `LagopusScotica`.
   - No subspecies on `.0` releases.
   - Example: `LagopusLeucura_v3.0.0`
4. **Minor Feature Bump (`vX.(Y+1).0`)**:
   - Retain current species.
   - Select first unused subspecies from the priority pool:
     `Helvetica`, `Hyperborea`, `Islandorum`, `Japonica`, `Millaisi`, `Nivalis`, `Pyrenaica`, `Rupestris`, `Saxatilis`, `Welchi`.
   - Example: `LagopusMutaHyperborea_v2.2.0`

### Step 3: Automated Tag Resolution Helper
You can execute the built-in helper script to resolve and validate release tags:
```bash
python3 templates/release_tagger.py --bump minor
```

### Step 4: Tag & Register Promotion
1. Update `docs/RELEASE_REGISTER.md` with the new version row.
2. Create annotated git tag:
   ```bash
   git tag -a "<TagIdentifier>" -m "{{PROJECT_NAME}} Platform <Version> - <Human Title>"
   ```
3. Push tag:
   ```bash
   git push origin <branch> --follow-tags
   ```
