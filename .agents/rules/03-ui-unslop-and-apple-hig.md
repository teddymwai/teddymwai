---
name: ui-unslop-and-apple-hig
description: UI design standards, quiet chrome architecture, Apple HIG component foundation, zero emoji mandate, and select element sanitization.
trigger: always_on
---

# UI Unslop Architecture & Apple HIG Component Guidelines

Whenever building, modifying, or styling user interfaces, dashboards, or web reports:

## 1. Zero "AI-Slop" & Emojis
- **Strictly No Emojis**: Never use emojis (no 🚀, ✨, 🔥, 🤖, ✅, ❌) as UI buttons, indicators, table badges, or headings.
- Use clean, professional vector iconography (e.g. Google Fonts Material Symbols or SVG icons).
- Tint icons with muted or secondary text colors to avoid visual distraction.

## 2. Quiet Chrome Architecture
- Understated, quiet navigation panels and structural chrome.
- Establish a strict 4px grid rhythm for all padding, margins, spacing, and sizing.
- Single bright focal point: Only the primary metric, action, or status gauge should claim high visual prominence.
- Ban neon glows, rainbow borders, and vibrating gradients.

## 3. Apple HIG Component Foundation
- **Shapes**:
  - Capsule geometry (`border-radius: 9999px`) for standalone pill buttons, filter chips, and toolbar actions.
  - Rounded Rectangles (`border-radius: 8px`–`12px`) for content cards, modals, and container surfaces.
- **Hit Targets**: Minimum **44x44px** hit target area on all interactive controls.
- **Tactile Response**: Add instant tactile feedback on click/press (`transform: scale(0.97)` on `:active`).
- **Prominence Hierarchy**: Scale visual importance by styling (Prominent, Tinted, Gray, Plain) rather than inconsistent physical sizes.
- **Skill Reference**: Full component schemas and button tokens live in `.agents/skills/apple-hig-components/`; the 9-pass redline lives in `.agents/skills/unslop-ui/`.

## 4. Form Controls & Select Sanitization
- Cross-browser select reset: `appearance: none; -webkit-appearance: none;`.
- Dedicated chevron right padding: `padding-right: 38px` to `42px`.
- Text truncation: `text-overflow: ellipsis; white-space: nowrap; overflow: hidden;`.
- Absolute or right-calculated positioning for dropdown SVG chevrons to eliminate collision with long text.

## 5. Self-Owned Design System, Edulis Signet & Attribution Standard
- The UI Mantra (unslop methodology, Apple HIG adaptation, Champagne Gold / Warm Ivory palette, and typography) is an internal **TedCraft / Edulis Secure Systems Hub Limited** standard.
- Never add third-party external author handles, third-party repository links, or `legacy/` vendored paths to docs, rules, READMEs, or templates. Cite internal paths only.
- **Institutional Relationship Guardrail**: Always attribute as `TedCraft, a publication of Edulis Secure Systems Hub Limited`—never *"an affiliate of Edulis SSH"*.
- **Edulis Unified Signet (`V3.2B-1`) Three-Resolution Optical Mandate**:
  - **`16px – 20px` (Favicon)**: Use the separate two-part drawing (hooked Mahiinga blade + separated hex seed node) as an inline SVG `<link rel="icon" type="image/svg+xml" ...>` so browser tabs read crisply without koru eye collapse. Never auto-scale the `32px+` koru signet below `24px`.
  - **`24px – 128px+` (Header / Signet)**: Use the full `V3.2B-1` compound `evenodd` path (`aria-hidden="true"`, `pointer-events: none`) rendered as single-color `currentColor`—never apply gradients, drop shadows, or multi-color fills inside the mark.
- **Canonical Footer Attribution & Author Links**: Rendered dashboards, walkthroughs, and web surfaces must include the standard attribution notice and Apple HIG capsule links (`min-height: 44px`, `border-radius: 9999px`, `:active { transform: scale(0.97); }`, inline SVG brand icons):
  - Notice: `Copyright © 2026 Ted Mwai · TedCraft, a publication of Edulis Secure Systems Hub Limited`
  - Author URLs: GitHub (`https://github.com/teddymwai`), LinkedIn (`https://www.linkedin.com/in/teddymwai/`), GitLab (`https://gitlab.com/teddymwai`).
- Permitted: functional namespace URIs (`http://www.w3.org/2000/svg`, JSON Schema `$schema`) and runtime asset imports (Google Fonts `Newsreader`, `Instrument Sans`, `JetBrains Mono`, and `Material Symbols Outlined` stylesheets).
- Third-party code retained under its own license (e.g. CC BY 4.0) keeps its license notice in place; never propagate that notice into internal docs. Prefer rewriting as an original internal artifact over vendoring.

## 6. Dual-Mode Palette, Typography & Composite Canvas (`img001.jpg`)
- **Enforced Dual-Mode Palette (`color-scheme: dark light`, dark default)**:
  - **Dark Obsidian (Default)**: Canvas `#09090b` / `#0c0c0e`, frosted cards `rgba(21, 21, 24, 0.86)` (`#151518` solid), subtle `#1f1f23`, Champagne Gold accent `#d4a853` (hover `#e2bc6b`, foreground `#0c0c0e`), text roles `#efe9de` / `#aaa398` / `#8a847a`.
  - **Warm Ivory Parchment (Light Reading Mode)**: Canvas `#efe9df` / `#f8f6f1`, frosted cards `rgba(253, 251, 247, 0.88)` (`#fdfbf7` solid), subtle `#f3efe6`, Deep Bronze-Gold accent `#8c6218` (hover `#6e4c10`, foreground `#fdfbf7`), text roles `#1f1b16` / `#5e554a` / `#7b7266`.
  - Wire both polarities via CSS `light-dark()` with `@media (prefers-color-scheme: light)` fallbacks—do not add a noisy theme dropdown to top navigation bars.
- **Editorial & Technical Precision Typography**:
  - **Display & Editorial Headings**: `'Newsreader', Georgia, serif` (weights `400`–`500`, tracking `-0.025em`). Never use `700`–`900` weights or gradient text.
  - **UI & Body Prose**: `'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif` (weights `400`–`500`).
  - **Telemetry, IDs & Code**: `'JetBrains Mono', ui-monospace, SFMono-Regular, monospace` with `font-variant-numeric: tabular-nums`.
- **Dual-Layer Composite Canvas (`img001.jpg`)**:
  1. **Fixed Parallax Backplane**: `background-attachment: fixed; background-size: cover; background-position: center top;` using `/backgrounds/img001.jpg`.
  2. **Theme-Matched Wash Overlay**: `linear-gradient(180deg, rgba(12, 12, 14, 0.87) 0%, rgba(12, 12, 14, 0.95) 100%)` in dark mode, and `linear-gradient(180deg, rgba(248, 246, 241, 0.93) 0%, rgba(248, 246, 241, 0.96) 100%)` in light mode.
  3. **Frosted Glass Elevated Containers**: `backdrop-filter: blur(12px); border: 1px solid var(--surface-border);`.
- **Dual-Protocol Asset Resolution**: Local tool servers must stream `GET /backgrounds/<file>` with `file://` relative path fallback so dashboards render identically when opened offline from disk.

## 7. Position-Aware Auto-Hiding Floating Tooltips (`TooltipManager`) & Header Ergonomics
- **Auto-Hiding Floating Guidance (`TooltipManager`)**: Interactive buttons, filter pills, capsule links, and safety toggles must provide position-aware tooltips (`data-tooltip="..."`, optional `data-shortcut="..."`) complying with WCAG 2.1 AA / 1.4.13:
  - Hidden by default (`visibility: hidden; pointer-events: none; opacity: 0; top: -9999px; left: -9999px;`), never intercepting clicks when inactive.
  - Auto-hides on `mouseout`/`focusout` (with a 120ms hover-bridge grace period), `pointerdown`, `scroll`, window `blur`, `<kbd>Escape</kbd>`, and an automatic inactivity timeout (`4000ms`), while remaining hoverable when active.
  - Clamped to viewport edges with automatic top/bottom flip and `prefers-reduced-motion` support.
- **Header Layout Invariant**:
  - **Far Left**: Brand vector icon aligned horizontally inline with the tool title (never stacked awkwardly above it).
  - **Far Right**: Active deployment badge, loopback bind pill (`127.0.0.1:<port>`), and live session status indicator.
