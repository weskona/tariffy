"""Static guards for the panel JavaScript (no browser needed)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from custom_components.tariffy.panel import PANEL_ELEMENT, PANEL_FILE

SOURCE = (
    Path(__file__).parent.parent / "custom_components" / "tariffy" / "frontend" / PANEL_FILE
).read_text(encoding="utf-8")

# Contract names, providers and tariffs are typed in by the user. They must only
# ever reach the page as text, never as HTML.
FORBIDDEN = (
    "innerHTML", "outerHTML", "insertAdjacentHTML", "document.write",
    "eval(", "new Function", "setAttribute(\"on", "javascript:",
)


@pytest.mark.parametrize("sink", FORBIDDEN)
def test_no_html_sinks(sink):
    assert sink not in SOURCE


def test_registers_the_element_the_backend_announces():
    assert f'customElements.define("{PANEL_ELEMENT}"' in SOURCE


def test_is_small_enough_to_ship():
    assert len(SOURCE.encode("utf-8")) < 160_000


def _block(language: str) -> str:
    start = SOURCE.index(f"  {language}: {{")
    other = {"en": "de", "de": "en"}[language]
    # the two language blocks follow each other, the second ends at the first "};"
    if SOURCE.index(f"  {other}: {{") > start:
        end = SOURCE.index(f"  {other}: {{")
    else:
        end = SOURCE.index("};", start)
    return SOURCE[start:end]


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


def test_empty_overview_groups_are_not_appended():
    """Issue #50: with only metered or only flat-rate contracts one group is null.
    `appendChild(null)` throws and leaves the whole panel empty, so the overview
    must never append a group directly."""
    assert "wrap.appendChild(group(" not in SOURCE
    assert "if (section) wrap.appendChild(section)" in SOURCE
