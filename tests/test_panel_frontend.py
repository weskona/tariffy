"""Static guards for the panel JavaScript (no browser needed)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from custom_components.tariffy.panel import PANEL_ELEMENT, PANEL_FILE

FRONTEND = Path(__file__).parent.parent / "custom_components" / "tariffy" / "frontend"
# the panel is split into the code (SOURCE) and the files with its texts, icons and styles
SOURCE = (FRONTEND / PANEL_FILE).read_text(encoding="utf-8")
TEXTS = (FRONTEND / "tariffy-i18n.js").read_text(encoding="utf-8")
STYLE = (FRONTEND / "tariffy-style.js").read_text(encoding="utf-8")
FILES = sorted(FRONTEND.glob("*.js"))

# Contract names, providers and tariffs are typed in by the user. They must only
# ever reach the page as text, never as HTML.
FORBIDDEN = (
    "innerHTML", "outerHTML", "insertAdjacentHTML", "document.write",
    "eval(", "new Function", "setAttribute(\"on", "javascript:",
)


@pytest.mark.parametrize("sink", FORBIDDEN)
@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_no_html_sinks(sink, path):
    assert sink not in path.read_text(encoding="utf-8")


def test_registers_the_element_the_backend_announces():
    assert f'customElements.define("{PANEL_ELEMENT}"' in SOURCE


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_every_file_is_small_enough_to_ship(path):
    assert len(path.read_bytes()) < 190_000


def test_the_element_is_defined_without_waiting_for_its_parts():
    """Home Assistant may create the element and set `hass` before it is defined; a module that waits (top-level
    await) for its parts defines it late, the values then hide the setters and the panel stays black."""
    assert not re.search(r"^(const|let|var)\s[^=\n]*=\s*await\b|^await\b", SOURCE, flags=re.M)
    assert "customElements.define(" in SOURCE
    # values given before the definition are taken back through the setters
    assert 'for (const prop of ["hass", "narrow", "panel"])' in SOURCE
    # nothing draws before the parts are there
    assert "if (!STYLE) return;" in SOURCE


def test_the_panel_loads_its_parts_with_its_own_version():
    """The static path is cached for a long time: the texts, icons and styles must be requested with the
    `?v=` of the panel file, or a browser could mix new code with old texts after an update."""
    assert "new URL(import.meta.url).search" in SOURCE
    for part in ("tariffy-i18n.js", "tariffy-icons.js", "tariffy-style.js"):
        assert f"import(`./{part}${{VERSION}}`)" in SOURCE
        assert (FRONTEND / part).is_file()
    # nothing is imported without the version
    assert not re.search(r"^\s*import\s.*from\s", SOURCE, flags=re.M)
    assert not re.search(r"import\(\"", SOURCE)


@pytest.mark.parametrize("path", [p for p in FILES if p.name != PANEL_FILE], ids=lambda p: p.name)
def test_the_parts_export_what_the_panel_imports(path):
    text = path.read_text(encoding="utf-8")
    name = {"tariffy-i18n.js": "I18N", "tariffy-icons.js": "ICONS", "tariffy-style.js": "STYLE"}[path.name]
    assert f"export const {name} =" in text
    assert "customElements.define" not in text


def _block(language: str) -> str:
    start = TEXTS.index(f"  {language}: {{")
    other = {"en": "de", "de": "en"}[language]
    # the two language blocks follow each other, the second ends at the first "};"
    if TEXTS.index(f"  {other}: {{") > start:
        end = TEXTS.index(f"  {other}: {{")
    else:
        end = TEXTS.index("};", start)
    return TEXTS[start:end]


def _keys(block: str) -> set[str]:
    body = block.split("\n", 1)[1]  # without the "en: {" / "de: {" line itself
    # drop the text literals first, so words inside a text ("Action failed: x")
    # are not mistaken for keys
    body = re.sub(r'"(?:\\.|[^"\\])*"', '""', body)
    return set(re.findall(r"\b([A-Za-z]+):", body))


def test_german_and_english_have_the_same_texts():
    en, de = _keys(_block("en")), _keys(_block("de"))
    assert en - de == set(), f"missing in German: {en - de}"
    assert de - en == set(), f"missing in English: {de - en}"


def test_every_used_text_exists():
    used = set(re.findall(r'this\._t\("([A-Za-z]+)"', SOURCE))
    # texts selected through a variable (tabs, tariff rows)
    used |= {"overview", "costs", "contracts", "highTariff", "lowTariff", "sparte"}
    missing = used - _keys(_block("en"))
    assert missing == set(), f"used but not defined: {missing}"


def test_streaming_has_no_empty_one_time_items_block():
    """A streaming subscription needs no one-time items; one that already has some keeps the block."""
    block = SOURCE[SOURCE.index("  _onceSection(c) {"):]
    block = block[: block.index("\n  }\n")]
    assert 'c.sparte === "streaming"' in block and "!items.length" in block


def test_streaming_says_price_not_instalment_and_the_duplicate_year_row_is_left_out():
    """Texts of a streaming subscription: "price"; the per-year row that repeats "cost per year" is left out (for every flat contract)."""
    for key in ("instalment", "nextInstalment", "secInstal", "instalEdit", "instalEnter", "instalTitle", "instalAmount", "instalNone", "instalHint"):
        assert TEXTS.count(f" {key}_streaming:") == 2, f"{key}_streaming must exist in English and German"
    assert "isNum(c.abschlag_jahr) && !sameAsYearCost" in SOURCE


def test_empty_overview_groups_are_not_appended():
    """Issue #50: with only metered or only flat-rate contracts one group is null.
    `appendChild(null)` throws and leaves the whole panel empty, so the overview
    must never append a group directly."""
    assert "wrap.appendChild(group(" not in SOURCE
    assert "if (section) wrap.appendChild(section)" in SOURCE


# ------------------------------------------------------------------------------ light and dark design
def _block_of(selector: str) -> str:
    start = STYLE.index(selector + " {")
    return STYLE[start : STYLE.index("\n}\n", start)]


def test_the_light_design_redefines_every_colour_of_the_dark_one():
    """The panel is dark by default and light with the class `light` on its host: every colour variable of the dark
    block must have a light counterpart, or a colour would stay dark-on-light."""
    dark = set(re.findall(r"(--[a-z0-9-]+):", _block_of(":host")))
    light = set(re.findall(r"(--[a-z0-9-]+):", _block_of(":host(.light)")))
    colours = {name for name in dark if name not in {"--tile", "--tile-line", "--line"}}  # these derive from --w
    assert colours - light == set(), f"no light value for {colours - light}"
    assert "color-scheme: light" in _block_of(":host(.light)")


def test_no_colour_of_one_design_is_hard_coded_in_the_styles():
    """White overlays and fixed hexadecimal colours would not follow the design: they live in the variables."""
    body = STYLE.split("* { box-sizing", 1)[1]  # everything after the two variable blocks
    assert "rgba(255,255,255" not in STYLE
    assert not re.findall(r"#[0-9a-fA-F]{6}\b", body), re.findall(r"#[0-9a-fA-F]{6}\b", body)


def test_the_panel_follows_the_theme_of_home_assistant():
    assert "this._hass.themes.darkMode" in SOURCE
    assert 'this.classList.toggle("light"' in SOURCE
    assert "this._applyTheme();" in SOURCE  # at every update of hass: a change of the theme shows at once
