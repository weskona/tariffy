#!/usr/bin/env python3
"""Checks the wiki sources in docs/wiki/: links, anchors, images, Mermaid blocks, DE/EN pairs.

Usage: python3 scripts/check_wiki.py          (exit code 1 on any problem)

Conventions it relies on:
- German pages have plain names, English pages the prefix "EN-" (see PAIRS).
- Wiki links name the page without extension: [text](Page) or [text](Page#anchor).
- Images are referenced by https://raw.githubusercontent.com/wiki/weskona/tariffy/images/<file>
  (that is where the file lands after copying docs/wiki/ into the wiki repository) or by a
  relative path images/<file>; the file must exist in docs/wiki/images/ and be under 500 KB.
- Mermaid blocks must start with a known diagram type and have balanced brackets.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "docs" / "wiki"
IMAGES = WIKI / "images"
RAW = "https://raw.githubusercontent.com/wiki/weskona/tariffy/images/"
MAX_IMAGE = 500 * 1024

# German page -> English page
PAIRS = {
    "Home": "EN-Home",
    "Erste-Schritte": "EN-Getting-Started",
    "Vertraege-Anlegen": "EN-Creating-Contracts",
    "Vertrag-Strom": "EN-Contract-Electricity",
    "Vertrag-Gas": "EN-Contract-Gas",
    "Vertrag-Wasser": "EN-Contract-Water",
    "Vertrag-Internet-und-Mobilfunk": "EN-Contract-Internet-and-Mobile",
    "Vertrag-Streaming": "EN-Contract-Streaming",
    "Vertrag-Versicherung": "EN-Contract-Insurance",
    "Vertrag-Leasing": "EN-Contract-Leasing",
    "Vertrag-Kredit": "EN-Contract-Loan",
    "Vertrag-Sonstiges": "EN-Contract-Other",
    "Verbrauch-Messen": "EN-Measuring-Consumption",
    "PV-Autarkie": "EN-PV-Self-Sufficiency",
    "Abschlaege-und-Kosten": "EN-Payments-and-Costs",
    "Abschlagsverlauf-und-Einmalposten": "EN-Payment-History-and-One-off-Items",
    "Vertragsende-und-Wechsel": "EN-Contract-End-and-Switching",
    "Folgevertrag-oder-Verlaengern": "EN-Next-Contract-or-Renew",
    "Archiv-und-Historie": "EN-Archive-and-History",
    "Panel-Uebersicht": "EN-Panel-Overview",
    "Panel-Kosten": "EN-Panel-Costs",
    "Panel-Vertraege": "EN-Panel-Contracts",
    "Panel-Historie": "EN-Panel-History",
    "Panel-Sicherung": "EN-Panel-Backup",
    "Panel-Rechte-und-Design": "EN-Panel-Permissions-and-Design",
    "Sensoren-Referenz": "EN-Sensor-Reference",
    "Dashboard-Beispiele": "EN-Dashboard-Examples",
    "Automationen": "EN-Automations",
    "Sicherung-und-Umzug": "EN-Backup-and-Migration",
    "FAQ": "EN-FAQ",
    "Fehlerbehebung": "EN-Troubleshooting",
    "Releases-und-Beta": "EN-Releases-and-Beta",
    "Entwickler": "EN-Development",
}
SPECIAL = {"_Sidebar", "_Footer"}
MERMAID_TYPES = (
    "flowchart",
    "graph",
    "sequenceDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "classDiagram",
    "erDiagram",
    "gantt",
    "pie",
    "journey",
    "timeline",
)
FENCE = re.compile(r"^```.*?^```", re.M | re.S)


def anchors(markdown: str) -> set[str]:
    """GitHub's anchors for the headings of a page (code fences are ignored)."""
    text = FENCE.sub("", markdown)
    found = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, flags=re.M):
        slug = re.sub(r"[^\w\s-]", "", heading.lower().replace("`", ""))
        found.add(re.sub(r"\s", "-", slug))
    return found


def headings(markdown: str) -> list[int]:
    return [
        len(m) for m in re.findall(r"^(#{1,6})\s", FENCE.sub("", markdown), flags=re.M)
    ]


def main() -> int:
    problems: list[str] = []
    pages = {p.stem: p for p in WIKI.glob("*.md")}
    expected = set(PAIRS) | set(PAIRS.values()) | SPECIAL
    for name in sorted(expected - set(pages)):
        problems.append(f"missing page: {name}.md")
    for name in sorted(set(pages) - expected):
        problems.append(
            f"page not in PAIRS (add it to scripts/check_wiki.py or delete it): {name}.md"
        )

    for name, page in sorted(pages.items()):
        text = page.read_text(encoding="utf-8")
        plain = FENCE.sub("", text)  # links inside code blocks are examples
        # --- links and images
        for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", plain):
            if target.startswith("#"):
                if target[1:] not in anchors(text):
                    problems.append(f"{name}: no heading {target} on this page")
                continue
            if target.startswith(RAW):
                if not (IMAGES / target[len(RAW) :]).exists():
                    problems.append(f"{name}: image missing: {target[len(RAW) :]}")
                continue
            if re.match(r"^(https?:|mailto:)", target):
                continue
            path, _, anchor = target.partition("#")
            if path.startswith("images/"):
                if not (WIKI / path).exists():
                    problems.append(f"{name}: image missing: {path}")
                continue
            if path not in pages:
                problems.append(f"{name}: link to unknown page: {target}")
            elif anchor and anchor not in anchors(
                pages[path].read_text(encoding="utf-8")
            ):
                problems.append(f"{name}: page {path} has no heading #{anchor}")
        for src in re.findall(r'(?:src|srcset)="([^"]+)"', plain):
            if src.startswith(RAW) and not (IMAGES / src[len(RAW) :]).exists():
                problems.append(f"{name}: image missing: {src[len(RAW) :]}")
            elif not src.startswith(("http", "images/")):
                problems.append(f"{name}: image path not under {RAW}: {src}")
        for alt in re.findall(r"!\[([^\]]*)\]\(", plain):
            if not alt.strip():
                problems.append(f"{name}: image without alt text")
        for tag in re.findall(r"<img\b[^>]*>", plain):
            if not re.search(r'alt="[^"]+"', tag):
                problems.append(f"{name}: <img> without alt text")
        # --- Mermaid
        for block in re.findall(r"^```mermaid\n(.*?)^```", text, flags=re.M | re.S):
            first = next(
                (
                    ln.strip()
                    for ln in block.splitlines()
                    if ln.strip() and not ln.strip().startswith("%%")
                ),
                "",
            )
            if not first.startswith(MERMAID_TYPES):
                problems.append(f"{name}: mermaid block starts with '{first[:30]}'")
            for open_, close in ("()", "[]", "{}"):
                if block.count(open_) != block.count(close):
                    problems.append(
                        f"{name}: mermaid block has unbalanced {open_}{close}"
                    )
        if text.count("```") % 2:
            problems.append(f"{name}: unclosed code fence")

    # --- DE/EN pairs: same number of headings per level, same number of images/diagrams/code blocks
    for de, en in PAIRS.items():
        if de in pages and en in pages:
            a, b = (
                pages[de].read_text(encoding="utf-8"),
                pages[en].read_text(encoding="utf-8"),
            )
            if headings(a) != headings(b):
                problems.append(
                    f"{de} / {en}: heading structure differs ({len(headings(a))} vs {len(headings(b))} headings)"
                )
            for label, pattern in (
                ("images", r"!\[|<img"),
                ("mermaid blocks", r"^```mermaid"),
                ("code blocks", r"^```"),
            ):
                ca, cb = (
                    len(re.findall(pattern, a, re.M)),
                    len(re.findall(pattern, b, re.M)),
                )
                if ca != cb:
                    problems.append(
                        f"{de} / {en}: number of {label} differs ({ca} vs {cb})"
                    )
            if f"]({en})" not in a:
                problems.append(f"{de}: no language link to {en}")
            if f"]({de})" not in b:
                problems.append(f"{en}: no language link to {de}")

    # --- images
    for img in sorted(IMAGES.glob("*")):
        if img.stat().st_size > MAX_IMAGE:
            problems.append(
                f"image over 500 KB: {img.name} ({img.stat().st_size // 1024} KB)"
            )

    # --- reachability: every page within two clicks of Home or the sidebar
    def links_of(name: str) -> set[str]:
        return {
            t.partition("#")[0]
            for t in re.findall(
                r"\]\(([^)\s]+)\)",
                FENCE.sub("", pages[name].read_text(encoding="utf-8")),
            )
            if t.partition("#")[0] in pages
        }

    if "Home" in pages and "_Sidebar" in pages:
        first = links_of("Home") | links_of("_Sidebar") | {"Home"}
        second = set(first)
        for p in list(first):
            if p in pages:
                second |= links_of(p)
        for name in sorted(set(PAIRS) | set(PAIRS.values())):
            if name in pages and name not in second:
                problems.append(
                    f"{name}: not reachable within two clicks from Home/_Sidebar"
                )

    for p in problems:
        print("PROBLEM:", p)
    print(
        f"{len(pages)} pages, {len(list(IMAGES.glob('*')))} images, {len(problems)} problems"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
