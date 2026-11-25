# Unslop Audit Checklist

Tick each item during the Inventory and Verify steps. Tag findings with the pass number so fixes land in the correct order.

## Pass 1 — Spacing
- [ ] No spacing, sizing, or line-height value outside the 4px scale.
- [ ] Intra-group gaps are smaller than inter-group gaps.
- [ ] Table rows and list items share a single row height.

## Pass 2 — Color
- [ ] Exactly one accent hue; it appears on the focal element and the primary action only.
- [ ] Exactly three text roles in use (primary / secondary / muted).
- [ ] Semantic colors (success / warning / error / info) used only for state, never decoration.
- [ ] No purple, violet, or cyan glow; no neon border.

## Pass 3 — Icons
- [ ] Zero emojis anywhere (labels, badges, headers, toasts, CLI output, markdown).
- [ ] Single icon family at 16/18/20px, tinted with the secondary role or a state color.
- [ ] Domain entities carry their mandated badge (Playlists, Scenarios, Teams, Cloud, VPN, Goals, Reports).

## Pass 4 — Copy
- [ ] Buttons are verb-led and sentence-case.
- [ ] No hype vocabulary or filler subtitles.
- [ ] No all-caps tracked labels; no trailing periods on short headlines or buttons.
- [ ] Institutional attribution written as `TedCraft, a publication of Edulis Secure Systems Hub Limited` (never *"an affiliate of Edulis SSH"*).
- [ ] Display/editorial headings use `Newsreader` serif (`400`–`500`), UI/body uses `Instrument Sans`, and `V3.2B-1` Edulis signet / `16px` optical favicon are present.

## Pass 5 — Typography
- [ ] ≤ 2 families + 1 mono.
- [ ] Body 400–500, headings ≤ 600; no gradient or outlined text.
- [ ] Metrics, IDs, and timestamps use `tabular-nums`.
- [ ] Primary copy meets WCAG AAA against its surface.

## Pass 6 — Layout
- [ ] Focal element is identifiable and holds the dominant area.
- [ ] Max one card level per region.
- [ ] Content aligns to a shared column grid.

## Pass 7 — Details
- [ ] Hairline borders (1px, low opacity); no stacked border + shadow + fill.
- [ ] Radii consistent: Capsule for standalone actions, 8–12px for stacked cards.
- [ ] Hover is a quiet surface step, not a glow.

## Pass 8 — Visuals
- [ ] Every visual carries data or state; no decorative blobs or mesh gradients.
- [ ] Canvas is a quiet neutral (or follows the project's canvas spec, if defined).

## Pass 9 — Motion
- [ ] Transitions 120–150ms with `cubic-bezier(0.2, 0, 0, 1)`.
- [ ] `:active` press `scale(0.97)` on interactive controls.
- [ ] No pulse, bounce, shimmer, or staggered entrance on static content.
- [ ] All motion guarded by `prefers-reduced-motion`.

## Ergonomics
- [ ] All interactive targets ≥ 44×44px.
- [ ] Sibling buttons share one height; hierarchy via prominence.
- [ ] `<select>` reset, 42px chevron reservation, ellipsis truncation.
- [ ] Visible focus state on every control.
