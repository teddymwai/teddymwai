---
name: unslop-ui
description: Audit, redesign, and refactor front-end UI (dashboards, operator panels, reports, blog pages, generated HTML) against the internal TedCraft / Edulis UI Mantra. Runs the 9-pass redline (Spacing, Color, Icons, Copy, Typography, Layout, Details, Visuals, Motion) to strip generic AI-generated aesthetics and enforce quiet chrome, one bright focal element, strict 4px rhythm, zero emojis, and Apple HIG control ergonomics. Use when the user asks to unslop, clean up, polish, review, or restyle an interface.
---

# Unslop UI: TedCraft / Edulis 9-Pass Redline

Internal methodology for converging any interface onto the TedCraft / Edulis UI Mantra. Canonical spec: `.agents/rules/03-ui-unslop-and-apple-hig.md`; default tokens: `references/design-tokens.md`. Control-level geometry is delegated to the `apple-hig-components` skill (where present).

## When to Use

- A screen "looks AI-generated": gradient hero text, neon glows, emoji labels, card-in-card nesting, uniform rainbow accents.
- Building a new dashboard, `<tool>_dashboard.html`, report surface, or page and you need a deterministic design checklist.
- Reviewing a UI diff before staging promotion.

## Inputs to Resolve First (never assume)

1. **Palette & type tokens** — ingest them from `.agents/rules/03-ui-unslop-and-apple-hig.md` (or the project's always-on UI rule). Template defaults live in `references/design-tokens.md`: Dual-mode **Deep Obsidian (`#0c0c0e`) + Champagne Gold (`#d4a853`)** dark default and **Warm Ivory (`#f8f6f1`) + Deep Bronze-Gold (`#8c6218`)** light reading mode, paired with `Newsreader` serif display/editorial headings, `Instrument Sans` UI/body, and `JetBrains Mono` telemetry.
2. **Focal element** — name the single thing on the view that deserves visual weight. If you cannot name it, the layout pass is not done.
3. **Surface type** — operator tool, report, marketing/editorial page. Density targets differ; rhythm rules do not.

## The 9 Passes (strict order)

Each pass is completed and re-rendered before the next starts. Later passes must not undo earlier ones.

| # | Pass | Converge on | Reject |
|---|------|-------------|--------|
| 1 | **Spacing** | Every padding, margin, gap, line-height, and size is a multiple of 4 (`4 8 12 16 20 24 32 48 64`). Related items sit closer than unrelated groups. | `7px`, `13px`, `15px`, `27px`; equal gaps everywhere. |
| 2 | **Color** | Neutral canvas, quiet surfaces, exactly three text roles (primary / secondary / muted). Accent reserved for the focal element and the primary action. Semantic colors only for state. | Purple/violet/cyan glows, multi-hue accents, colored card backgrounds per section. |
| 3 | **Icons** | Google Fonts Material Symbols (or the project's wire-extracted glyph font) at 16/18/20px, tinted with the secondary text role. Domain badges per the iconography rule. | Any emoji; mixed icon families; icons on colored circular blobs. |
| 4 | **Copy** | Verb-led, sentence-case labels. State what a control does. Headlines without trailing periods. | Hype ("supercharge", "seamless", "unleash"), tracked all-caps shouting, filler subtitles. |
| 5 | **Typography** | Max 2 families + 1 mono. Weights 400–500 for body, ≤600 for headings. `tabular-nums` for metrics, IDs, timestamps. WCAG AAA for primary copy. | 700–900 display weights, gradient text, italic blockquotes as decoration. |
| 6 | **Layout** | One container level per region; alignment to a shared column grid; the focal element given the dominant area. | Card inside card inside card; centered everything; symmetric grids with no hierarchy. |
| 7 | **Details** | 1px hairlines at low opacity, consistent radii (Capsule `9999px` for standalone actions, `8–12px` for stacked cards), quiet hover as a surface step. | Heavy drop shadows, outer glows, mixed radii, borders plus shadows plus fills on one element. |
| 8 | **Visuals** | Data-bearing visuals: telemetry meters, sparklines, structured tables, status indicators. Background canvas stays a quiet neutral unless the project defines a canvas spec. | Decorative blur blobs, abstract mesh gradients, stock 3D illustrations. |
| 9 | **Motion** | 120–150ms `cubic-bezier(0.2, 0, 0, 1)` transitions on state change; `:active` `scale(0.97)`; everything guarded by `prefers-reduced-motion`. | Pulsing/bouncing badges, looping shimmer, entrance animations on every card. |

## Control Ergonomics (non-negotiable)

- Interactive hit area ≥ **44×44px** (expand compact 28–36px pills with `::after`).
- Sibling buttons share one height; rank by prominence (Prominent → Tinted → Gray/Glass → Plain), never by size.
- `<select>`: `appearance: none` (+ `-webkit-`/`-moz-`), `44px` height, `42px` right chevron reservation, `text-overflow: ellipsis; white-space: nowrap; overflow: hidden;`, Material Symbol SVG chevron at `calc(100% - 14px) center`.
- Focus: `border-color` + `1px` ring in the brand active tone; never remove focus without replacement.

## Execution Workflow

1. **Inventory** — screenshot (or render) the current view; list every violation using `references/audit-checklist.md`, tagged by pass number.
2. **Redline** — apply passes 1→9 in order. Commit-size each pass so diffs remain reviewable.
3. **Verify** — re-render at desktop and narrow widths in both themes (if the project is dual-mode). Re-run the checklist; zero open items in passes 1–5 is the exit gate.
4. **Report** — summarize changes per pass, note the chosen focal element, and list any deliberate exceptions with rationale.

## Output Rules

- Ship the result as plain production code in the project's own stack (CSS variables / Tailwind tokens / Astro components). No presentation-only classes or demo scaffolding.
- Inline comments may tag the pass that motivated a non-obvious decision (e.g. `/* Pass 5: tabular figures */`).
- Never add third-party external author handles, third-party repository links, or `legacy/` vendored paths. Cite internal paths only, and include the canonical TedCraft / Edulis Secure Systems Hub Limited attribution footer (`Copyright © 2026 Ted Mwai · TedCraft, a publication of Edulis Secure Systems Hub Limited`) with Apple HIG capsule links to GitHub, LinkedIn, and GitLab on rendered web surfaces.
