#!/usr/bin/env python3
"""Deterministic profile README and SVG card generator for teddymwai/teddymwai.

Zero external dependencies (Python 3.9+ standard library only).
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "profile.json"
README_PATH = ROOT / "README.md"
SIGNET_PATH = ROOT / "assets" / "brand" / "edulis-signet-gold.svg"
CARDS_DIR = ROOT / "assets" / "cards"

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\U0001F000-\U0001F2FF\u200D\uFE0F]"
)
CYBER_RANGES_BAD_RE = re.compile(r"\b(?:CyberRanges|Cyberranges|cyberranges|Cyber Ranges|cyber ranges)\b")
AFFILIATE_BAD_RE = re.compile(r"affiliate\s+of\s+Edulis", re.IGNORECASE)

PALETTE: Dict[str, Dict[str, str]] = {
    "dark": {
        "bg": "#0c0c0e",
        "card": "#151518",
        "border": "#26262c",
        "accent": "#d4a853",
        "accent_dim": "#221d13",
        "fg": "#efe9de",
        "fg2": "#aaa398",
        "fg3": "#8a847a",
    },
    "light": {
        "bg": "#f8f6f1",
        "card": "#fdfbf7",
        "border": "#e5dfd3",
        "accent": "#8c6218",
        "accent_dim": "#f3ece0",
        "fg": "#1f1b16",
        "fg2": "#5e554a",
        "fg3": "#7b7266",
    },
}

FONT_SERIF = "'Newsreader', Georgia, 'Times New Roman', serif"
FONT_SANS = "'Instrument Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
FONT_MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"


def load_data() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def extract_signet_path() -> str:
    raw = SIGNET_PATH.read_text(encoding="utf-8")
    m = re.search(r'\bd="([^"]+)"', raw)
    if not m:
        raise ValueError(f"Could not extract <path d='...'> from {SIGNET_PATH}")
    return m.group(1)


def render_hero_svg(data: dict, theme: str, signet_d: str) -> str:
    p = PALETTE[theme]
    ident = data["identity"]
    edulis = data["edulis"]
    name = html.escape(ident["name"])
    role = html.escape(ident["role"])
    pos = html.escape(ident["positioning"])
    loc = html.escape(ident["location"])
    pub = html.escape(edulis["publication"]["line"])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 216" width="880" height="216" role="img" aria-label="{name} — {role}">
  <rect width="880" height="216" rx="12" fill="{p['bg']}" />
  <rect x="0.5" y="0.5" width="879" height="215" rx="11.5" fill="none" stroke="{p['border']}" />
  <rect x="24" y="24" width="832" height="168" rx="10" fill="{p['card']}" stroke="{p['border']}" />

  <g transform="translate(48, 52) scale(0.875)">
    <path fill="{p['accent']}" fill-rule="evenodd" clip-rule="evenodd" d="{signet_d}" />
  </g>

  <text x="192" y="72" font-family="{FONT_MONO}" font-size="11" letter-spacing="1.8" fill="{p['accent']}">EDULIS SECURE SYSTEMS HUB</text>
  <text x="192" y="114" font-family="{FONT_SERIF}" font-size="36" font-weight="400" letter-spacing="-0.6" fill="{p['fg']}">{name}</text>
  <text x="192" y="142" font-family="{FONT_SANS}" font-size="14" font-weight="500" fill="{p['fg2']}">{pos}</text>
  <text x="192" y="168" font-family="{FONT_MONO}" font-size="11.5" fill="{p['fg3']}">{loc}  |  {pub}</text>
</svg>
"""


def render_lane_svg(lane_key: str, lane_meta: dict, count: int, theme: str) -> str:
    p = PALETTE[theme]
    eyebrow = html.escape(f"{lane_meta['index']}  /  {lane_meta['eyebrow']}")
    title = html.escape(lane_meta["title"])
    blurb = html.escape(lane_meta["blurb"])
    badge = html.escape(f"{count} {'ITEM' if count == 1 else 'ITEMS'}")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 80" width="880" height="80" role="img" aria-label="{title} — {blurb}">
  <rect width="880" height="80" rx="10" fill="{p['card']}" />
  <rect x="0.5" y="0.5" width="879" height="79" rx="9.5" fill="none" stroke="{p['border']}" />
  <rect x="16" y="18" width="4" height="44" rx="2" fill="{p['accent']}" />

  <text x="36" y="32" font-family="{FONT_MONO}" font-size="10.5" letter-spacing="1.6" fill="{p['accent']}">{eyebrow}</text>
  <text x="36" y="58" font-family="{FONT_SERIF}" font-size="22" font-weight="400" letter-spacing="-0.3" fill="{p['fg']}">{title}</text>

  <text x="260" y="45" font-family="{FONT_SANS}" font-size="13" fill="{p['fg2']}">{blurb}</text>

  <rect x="772" y="26" width="88" height="28" rx="14" fill="{p['accent_dim']}" stroke="{p['border']}" />
  <text x="816" y="44" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="500" fill="{p['accent']}">{badge}</text>
</svg>
"""


def picture_tag(base_name: str, alt: str) -> str:
    return (
        "<picture>\n"
        f'  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/{base_name}-dark.svg">\n'
        f'  <source media="(prefers-color-scheme: light)" srcset="assets/cards/{base_name}-light.svg">\n'
        f'  <img alt="{html.escape(alt)}" src="assets/cards/{base_name}-dark.svg" width="100%">\n'
        "</picture>"
    )


def render_edulis_block(data: dict) -> str:
    ed = data["edulis"]
    lines = [
        f"> **{ed['mission']}**",
        "",
        ed["origin"],
        "",
        "| Practice | Focus |",
        "| :--- | :--- |",
    ]
    for pillar, desc in ed["pillars"]:
        lines.append(f"| **{pillar}** | {desc} |")
    lines.extend(["", f"Editorial ledger: [{ed['publication']['line']}]({ed['publication']['url']})."])
    return "\n".join(lines)


def render_lane_block(data: dict, lane_key: str) -> str:
    meta = data["lanes"][lane_key]
    items = [w for w in data["works"] if w["lane"] == lane_key]
    lines = [
        picture_tag(f"lane-{lane_key}", f"{meta['index']} {meta['title']} — {meta['blurb']}"),
        "",
        "| Work | What it does | Status | Links |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for w in items:
        title = f"**{w['title']}**"
        if w.get("version"):
            title += f" `{w['version']}`"
        stack = " · ".join(w.get("stack", []))
        what = w["tagline"]
        if stack:
            what += f" *({stack})*"
        status = f"`{w['status']}`"
        links = " · ".join(f"[{k}]({v})" for k, v in w.get("links", {}).items()) or "—"
        lines.append(f"| {title} | {what} | {status} | {links} |")
    return "\n".join(lines)


def render_method_block(data: dict) -> str:
    lines = ["| Principle | Practice |", "| :--- | :--- |"]
    for k, v in data["method"]:
        lines.append(f"| **{k}** | {v} |")
    return "\n".join(lines)


def render_credentials_block(data: dict) -> str:
    lines = [f"- {c}" for c in data["credentials"]]
    lines.append("")
    lines.append(f"**Beyond the terminal:** {data['beyond']}")
    return "\n".join(lines)


def render_connect_block(data: dict) -> str:
    links = " · ".join(f"[{label}]({url})" for label, url in data["links"])
    pub = data["edulis"]["publication"]["line"]
    return f"{links}\n\n<sub>Copyright &copy; 2026 {data['identity']['name']} &middot; {pub}</sub>"


def fetch_feed_block(url: str, limit: int) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "teddymwai-profile-builder/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
    root = ET.fromstring(raw)
    items = root.findall(".//item")[:limit]
    lines: List[str] = []
    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_raw = (item.findtext("pubDate") or "").strip()
        date_str = ""
        if pub_raw:
            try:
                date_str = parsedate_to_datetime(pub_raw).strftime("%Y-%m-%d")
            except (TypeError, ValueError):
                date_str = pub_raw[:16]
        if title and link:
            prefix = f"`{date_str}` — " if date_str else ""
            lines.append(f"- {prefix}[{title}]({link})")
    if not lines:
        lines.append("- Field notes and dossiers published at [tedcraft.dev](https://tedcraft.dev).")
    return "\n".join(lines)


def replace_block(readme: str, key: str, body: str) -> str:
    pat = re.compile(rf"(<!-- BEGIN:{re.escape(key)} -->)(.*?)(<!-- END:{re.escape(key)} -->)", re.S)
    if not pat.search(readme):
        raise ValueError(f"Missing marker <!-- BEGIN:{key} --> in README.md")
    return pat.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", readme)


def compute_outputs(data: dict, feed_url: Optional[str] = None) -> Tuple[Dict[Path, str], str]:
    signet_d = extract_signet_path()
    svgs: Dict[Path, str] = {}
    for theme in ("dark", "light"):
        svgs[CARDS_DIR / f"hero-{theme}.svg"] = render_hero_svg(data, theme, signet_d)
        for lane_key, lane_meta in data["lanes"].items():
            count = sum(1 for w in data["works"] if w["lane"] == lane_key)
            svgs[CARDS_DIR / f"lane-{lane_key}-{theme}.svg"] = render_lane_svg(
                lane_key, lane_meta, count, theme
            )

    readme = README_PATH.read_text(encoding="utf-8")
    readme = replace_block(readme, "hero", picture_tag("hero", f"{data['identity']['name']} — {data['identity']['role']}"))
    readme = replace_block(readme, "summary", data["identity"]["summary"])
    readme = replace_block(readme, "edulis", render_edulis_block(data))
    for lane_key in ("shipped", "inflight", "horizon"):
        readme = replace_block(readme, lane_key, render_lane_block(data, lane_key))
    readme = replace_block(readme, "method", render_method_block(data))
    readme = replace_block(readme, "credentials", render_credentials_block(data))
    readme = replace_block(readme, "connect", render_connect_block(data))
    if feed_url:
        feed_body = fetch_feed_block(feed_url, int(data["feed"]["limit"]))
        readme = replace_block(readme, "feed", feed_body)
    return svgs, readme


def run_selftest(check_links: bool = False) -> int:
    data = load_data()
    errors: List[str] = []

    for req_key in ("identity", "edulis", "lanes", "works", "method", "credentials", "links"):
        if req_key not in data:
            errors.append(f"profile.json missing top-level key: {req_key}")

    valid_lanes = set(data["lanes"].keys())
    for w in data["works"]:
        if w.get("lane") not in valid_lanes:
            errors.append(f"Work '{w.get('id')}' has invalid lane '{w.get('lane')}'")
        for link_url in w.get("links", {}).values():
            for priv in data.get("private_repos", []):
                if re.search(rf"(github|gitlab)\.com/teddymwai/{re.escape(priv)}\b", link_url, re.IGNORECASE):
                    errors.append(f"Private repo '{priv}' hyperlinked in work '{w['id']}': {link_url}")

    svgs, readme = compute_outputs(data, feed_url=None)
    texts_to_scan = [
        ("data/profile.json", DATA_PATH.read_text(encoding="utf-8")),
        ("README.md", readme),
    ] + [(str(p.relative_to(ROOT)), content) for p, content in svgs.items()]

    for label, text in texts_to_scan:
        if EMOJI_RE.search(text):
            errors.append(f"Emoji detected in {label}")
        if CYBER_RANGES_BAD_RE.search(text):
            errors.append(f"Invalid CYBER RANGES casing in {label}")
        if AFFILIATE_BAD_RE.search(text):
            errors.append(f"Prohibited 'affiliate of Edulis' phrasing in {label}")

    pub_line = data["edulis"]["publication"]["line"]
    if pub_line not in readme:
        errors.append(f"Missing canonical attribution '{pub_line}' in README.md")

    for p, content in svgs.items():
        try:
            ET.fromstring(content)
        except ET.ParseError as exc:
            errors.append(f"Malformed SVG XML in {p.name}: {exc}")

    if check_links:
        urls = set()
        for w in data["works"]:
            urls.update(w.get("links", {}).values())
        for _, url in data["links"]:
            urls.add(url)
        urls.add(data["edulis"]["publication"]["url"])
        for url in sorted(urls):
            try:
                req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "teddymwai-link-check/1.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status >= 400:
                        errors.append(f"Link returned {resp.status}: {url}")
            except urllib.error.HTTPError as exc:
                if exc.code in (403, 405):
                    continue
                errors.append(f"Link HTTP error {exc.code}: {url}")
            except Exception as exc:
                errors.append(f"Link unreachable ({exc}): {url}")

    if errors:
        for err in errors:
            print(f"[FAIL] {err}", file=sys.stderr)
        return 1
    print(f"[PASS] selftest passed ({len(data['works'])} works, {len(svgs)} SVGs, 0 policy violations)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or verify teddymwai/teddymwai profile README and SVG cards.")
    parser.add_argument("--check", action="store_true", help="Verify committed README.md and SVGs match data/profile.json.")
    parser.add_argument("--selftest", action="store_true", help="Validate schema, zero-emoji, attribution, private-link, and XML invariants.")
    parser.add_argument("--check-links", action="store_true", help="Verify HTTP reachability of public links during --selftest.")
    parser.add_argument("--feed", nargs="?", const="DEFAULT", help="Fetch latest RSS items from TedCraft feed URL.")
    args = parser.parse_args()

    if args.selftest:
        return run_selftest(check_links=args.check_links)

    data = load_data()
    feed_url = data["feed"]["url"] if args.feed == "DEFAULT" else args.feed
    svgs, readme = compute_outputs(data, feed_url=feed_url)

    if args.check:
        drifted: List[str] = []
        if README_PATH.read_text(encoding="utf-8") != readme:
            drifted.append("README.md")
        for path, content in svgs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drifted.append(str(path.relative_to(ROOT)))
        if drifted:
            print(f"[FAIL] Generated artifacts out of sync with data/profile.json: {', '.join(drifted)}", file=sys.stderr)
            return 1
        print(f"[PASS] All {len(svgs) + 1} generated artifacts are in sync with data/profile.json")
        return 0

    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in svgs.items():
        path.write_text(content, encoding="utf-8")
    README_PATH.write_text(readme, encoding="utf-8")
    print(f"[OK] Generated {len(svgs)} SVG cards and updated README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
