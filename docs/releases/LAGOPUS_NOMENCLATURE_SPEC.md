# Software Release Nomenclature Specification (Lagopus Protocol)

## 1. Taxonomic Lineage & Semantic Versioning

All software releases must pair **Semantic Versioning** (`vMAJOR.MINOR.PATCH[-STAGE.N][+BUILD]`) with the biological taxonomy of the **ptarmigan genus (*Lagopus*)** in the grouse subfamily of birds.

Mapping taxonomic ranks to release lineage rather than build maturity ensures that pre-release builds tested on `staging` and final generally available (GA) releases promoted to `main` share an unbroken identifier lineage.

### Canonical Identifier Formats

- **Machine & Git Tag Format**:
  `Lagopus[Species][Subspecies]_vMAJOR.MINOR.PATCH[-STAGE.N][+BUILD]`
- **Human-Readable Release Title**:
  `Ted Mwai Profile Platform vMAJOR.MINOR.PATCH[-STAGE.N] - Lagopus [Species] [Subspecies]`
- **Platform-Specific Binary / Artifact Suffix**:
  `Lagopus[Species][Subspecies]_vMAJOR.MINOR.PATCH-<os>-<arch>`  
  *(e.g., `LagopusMutaHelvetica_v2.4.1-linux-amd64`)*

| Segment | Taxonomic / SemVer Rank | Increment Trigger | Example Transition |
| :--- | :--- | :--- | :--- |
| `Lagopus` | Genus | Constant product family prefix across all project releases | `Lagopus...` |
| `[Species]` | Species epithet | Breaking API, schema, architecture, or major workflow change (`MAJOR`) | `LagopusMuta_v2.x` to `LagopusLeucura_v3.0.0` |
| `[Subspecies]` | Subspecies epithet | Backward-compatible feature release (`MINOR > 0`); omitted on `.0` major releases | `LagopusMuta_v2.0.0` to `LagopusMutaHelvetica_v2.1.0` |
| `PATCH` | Semantic patch (`.Z`) | Backward-compatible bug-fix or security hotfix; retains parent taxon verbatim | `LagopusMutaHelvetica_v2.4.0` to `LagopusMutaHelvetica_v2.4.1` |
| `-STAGE.N` | Pre-release label | Nightly / staging validation milestones (`-alpha.1`, `-beta.2`, `-rc.1`); retains parent taxon | `LagopusLeucura_v3.0.0-beta.2` to `LagopusLeucura_v3.0.0-rc.1` |
| `+build.N` | Build metadata | CI/CD pipeline traceability; does not affect version precedence | `LagopusLeucura_v3.0.0-beta.2+build.1847` |

---

## 2. Dynamic Taxon Assignment Protocol

Rather than maintaining a static manual table for future versions, the agent and release tooling resolve taxonomic names dynamically at release time:

1. **Query Existing Repository Tags**:
   Run `git tag -l "Lagopus*"` and inspect `docs/RELEASE_REGISTER.md` to map existing `(MAJOR, MINOR)` lineages and previously consumed subspecies epithets.
2. **Preserve Existing Lineages on Patches & Promotions**:
   - When bumping `PATCH` (`v2.4.0` to `v2.4.1`) or promoting a pre-release (`v3.0.0-rc.1` to `v3.0.0`), reuse the exact taxonomic prefix already bound to `(MAJOR, MINOR)`.
3. **Select Species for Major Releases (`vX.0.0`)**:
   Follow the recognized biological *Lagopus* (ptarmigan) species progression:
   - `v1.x`: `Lagopus` (*Lagopus lagopus* — Willow ptarmigan)
   - `v2.x`: `LagopusMuta` (*Lagopus muta* — Rock ptarmigan)
   - `v3.x`: `LagopusLeucura` (*Lagopus leucura* — White-tailed ptarmigan)
   - `v4.x`: `LagopusScotica` (*Lagopus scotica* — Red grouse / Scottish ptarmigan)
4. **Select Next Unused Subspecies for Minor Releases (`vX.Y.0`, `Y > 0`)**:
   Pull the first unused epithet in alphabetical order from the priority subspecies pool:

### Curated Subspecies Priority Pool (Ptarmigan Family)

| Queue Order | Subspecies Token | Binomial Source | Geographic / Habitat Origin | Example Tag |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `Helvetica` | *L. muta helvetica* | Swiss and Central European Alps | `LagopusMutaHelvetica_v2.1.0` |
| 2 | `Hyperborea` | *L. muta hyperborea* | Svalbard and Franz Josef Land | `LagopusMutaHyperborea_v2.2.0` |
| 3 | `Islandorum` | *L. muta islandorum* | Iceland volcanic highlands | `LagopusMutaIslandorum_v2.3.0` |
| 4 | `Japonica` | *L. muta japonica* | Japanese Honshu alpine zone | `LagopusMutaJaponica_v2.4.0` |
| 5 | `Millaisi` | *L. muta millaisi* | Scottish Highlands | `LagopusMutaMillaisi_v2.5.0` |
| 6 | `Nivalis` | *L. muta* snow-line epithet | High-altitude snow zone | `LagopusMutaNivalis_v2.6.0` |
| 7 | `Pyrenaica` | *L. muta pyrenaica* | Pyrenees mountains | `LagopusMutaPyrenaica_v2.7.0` |
| 8 | `Rupestris` | *L. muta rupestris* | Northern North America & Greenland | `LagopusMutaRupestris_v2.8.0` |
| 9 | `Saxatilis` | *L. leucura saxatilis* | Vancouver Island rocky peaks | `LagopusMutaSaxatilis_v2.9.0` |
| 10 | `Welchi` | *L. muta welchi* | Newfoundland rocky barrens | `LagopusMutaWelchi_v2.10.0` |

*(Extended pool: `Alascensis`, `Alleni`, `Altai`, `Atkhensis`, `Birulai`, `Cabrerai`, `Captus`, `Chamberlaini`, `Dixoni`, `Evermanni`, `Gabrielsoni`, `Kelloggae`, `Kurilensis`, `Leucoptera`, `Macruros`, `Muriei`, `Nadezdae`, `Nelsoni`, `Peninsularis`, `Rainierensis`, `Sanfordi`, `Saturata`, `Townsendi`, `Ungavus`, `Xenoura`.)*

---

## 3. Reference Lifecycle Stages

| Release Scenario | Target Branch | Target Deployment | Full Tag Identifier | Human-Readable Release Title |
| :--- | :--- | :--- | :--- | :--- |
| Major `.0` beta with CI metadata | `staging` | Staging / Foundry | `LagopusLeucura_v3.0.0-beta.2+build.1847` | `Ted Mwai Profile Platform v3.0.0-beta.2+build.1847 - Lagopus Leucura` |
| Major `.0` release candidate | `staging` | Staging / Foundry | `LagopusLeucura_v3.0.0-rc.1` | `Ted Mwai Profile Platform v3.0.0-rc.1 - Lagopus Leucura` |
| Major `.0` GA promotion | `main` | Production | `LagopusLeucura_v3.0.0` | `Ted Mwai Profile Platform v3.0.0 - Lagopus Leucura` |
| Minor `.4` stable feature release | `main` | Production | `LagopusMutaHelvetica_v2.4.0` | `Ted Mwai Profile Platform v2.4.0 - Lagopus Muta Helvetica` |
| Minor `.4` security/bug-fix patch | `main` | Production | `LagopusMutaHelvetica_v2.4.1` | `Ted Mwai Profile Platform v2.4.1 - Lagopus Muta Helvetica` |

---

## 4. Release Register Schema (`docs/RELEASE_REGISTER.md`)

Every tagged release must be recorded in `docs/RELEASE_REGISTER.md`:

```markdown
| Version | Taxonomic Codename | Full Tag Identifier | Stage | Branch | Commit SHA | Release Date | Owner | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `<vX.Y.Z>` | `<Lagopus ...>` | `<Lagopus..._vX.Y.Z>` | `<Alpha/Beta/RC/GA/Patch>` | `<staging/main>` | `<short-sha>` | `<YYYY-MM-DD>` | `<@handle>` | `<Summary>` |
```
