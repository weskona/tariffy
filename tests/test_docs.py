"""The documentation must not point to things that do not exist."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
WIKI = ROOT / "docs" / "wiki"
PANEL_JS = (ROOT / "custom_components" / "tariffy" / "frontend" / "tariffy-panel.js").read_text(encoding="utf-8")
PAGES = [ROOT / "README.md", *sorted(WIKI.glob("*.md"))]


def _anchors(markdown: str) -> set[str]:
    """GitHub's anchors for the headings of a page."""
    anchors = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", markdown, flags=re.M):
        text = re.sub(r"[^\w\s-]", "", heading.lower().replace("`", ""))
        anchors.add(re.sub(r"\s", "-", text))  # an emoji leaves a leading "-", like on GitHub
    return anchors


@pytest.mark.parametrize("page", PAGES, ids=lambda p: str(p.relative_to(ROOT)))
def test_relative_links_and_images_resolve(page):
    text = page.read_text(encoding="utf-8")
    for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        path, _, anchor = target.partition("#")
        if page.parent == WIKI and not path.endswith((".md", ".png")):
            candidate = WIKI / f"{path}.md"  # wiki links name the page without extension
        else:
            candidate = (page.parent / path).resolve()
        assert candidate.exists(), f"{page.name}: {target} does not exist"
        if anchor:
            assert anchor in _anchors(candidate.read_text(encoding="utf-8")), f"{page.name}: no heading #{anchor}"


def test_in_page_anchors_exist():
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        for anchor in re.findall(r"\]\(#([^)\s]+)\)", text):
            assert anchor in _anchors(text), f"{page.name}: no heading #{anchor}"


def test_every_wiki_page_is_in_the_sidebar_and_on_the_home_page():
    sidebar = (WIKI / "_Sidebar.md").read_text(encoding="utf-8")
    home = (WIKI / "Home.md").read_text(encoding="utf-8")
    for page in WIKI.glob("*.md"):
        if page.stem in {"_Sidebar", "Home"}:
            continue
        assert f"({page.stem})" in sidebar, f"{page.stem} is missing in _Sidebar.md"
        assert f"({page.stem})" in home, f"{page.stem} is missing in Home.md"


# The button names the panel documentation quotes must be the ones the panel shows.
GERMAN = (
    "Neuer Vertrag", "Vertrag bearbeiten", "Folgevertrag planen", "Folgevertrag bearbeiten",
    "Warnung bestätigen", "Kündigung bestätigen", "Vertrag löschen", "Endgültig löschen",
    "Geplanten Vertrag entfernen", "Kündigung als erledigt markieren",
)
ENGLISH = (
    "New contract", "Edit contract", "Plan next contract", "Edit next contract",
    "Acknowledge warning", "Acknowledge cancellation", "Delete contract", "Delete for good",
    "Remove planned contract", "Mark the cancellation as done",
)


@pytest.mark.parametrize("label", GERMAN + ENGLISH)
def test_the_panel_shows_the_button_names_the_documentation_quotes(label):
    assert f'"{label}"' in PANEL_JS, f"the panel has no text '{label}'"


def test_the_documentation_quotes_them():
    german = (WIKI / "Panel.md").read_text(encoding="utf-8")
    english = (WIKI / "English.md").read_text(encoding="utf-8")
    for label in GERMAN:
        assert label in german, f"Panel.md does not mention '{label}'"
    for label in ENGLISH:
        assert label in english, f"English.md does not mention '{label}'"
