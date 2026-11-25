# Design Tokens & UI Reference Standards

## 1. 4px Grid Rhythm

All spacing must be multiples of 4px:
- `4px`: Hairline padding, tight icon spacing
- `8px`: Standard element gap, pill internal margin
- `12px`: Card padding (compact)
- `16px`: Standard card/modal padding
- `24px`: Section spacing
- `32px`: Main view gutter

## 2. Dual-Mode Color Roles (Dark Obsidian Default / Warm Ivory Light)

| Token | Dark Obsidian (Default) | Warm Ivory (Light) | Usage |
|---|---|---|---|
| `--color-bg-deep` | `#09090b` | `#efe9df` | Deepest backdrop |
| `--color-bg-base` | `#0c0c0e` | `#f8f6f1` | Main canvas background |
| `--color-bg-surface` | `rgba(21, 21, 24, 0.86)` (`#151518`) | `rgba(253, 251, 247, 0.88)` (`#fdfbf7`) | Cards, panels, drawers |
| `--color-bg-subtle` | `#1f1f23` | `#f3efe6` | Raised controls, active nav |
| `--color-border-subtle` | `rgba(239, 233, 222, 0.08)` | `rgba(31, 27, 22, 0.09)` | Dividers, card strokes |
| `--color-text-primary` | `#efe9de` | `#1f1b16` | Headers, body text |
| `--color-text-secondary` | `#aaa398` | `#5e554a` | Secondary copy |
| `--color-text-muted` | `#8a847a` | `#7b7266` | Metadata, timestamps, captions |
| `--color-brand` | `#d4a853` | `#8c6218` | Primary buttons, focal accent |
| `--color-brand-hover` | `#e2bc6b` | `#6e4c10` | Hover state |
| `--color-brand-fg` | `#0c0c0e` | `#fdfbf7` | Foreground text on brand fill |
| `--color-danger` | `#e5484d` | `#dc2626` | Critical alerts, destructive actions |

## 3. Typography Pairing
- **Display & Editorial Headings**: `'Newsreader', Georgia, serif` (weights `400`–`500`, tracking `-0.025em`)
- **UI & Body Prose**: `'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif` (weights `400`–`500`)
- **Telemetry, IDs & Code**: `'JetBrains Mono', ui-monospace, SFMono-Regular, monospace` (`font-variant-numeric: tabular-nums`)

## 3. Apple HIG Touch Metrics

- Primary Action Button: Height `44px`, Radius `9999px` (Capsule)
- Form Input / Select: Height `44px`, Radius `8px`
- Press Scale: `scale(0.97)` on `:active` with `100ms` cubic-bezier transition
