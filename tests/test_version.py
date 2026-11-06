"""Pre-release numbers stay at 9 or below per series.

GitHub sorts the tag names of its release list as text: `v1.27.0-beta.10` lands between
`beta.2` and `beta.1`, so HACS (which takes "the newest" and the versions it offers from the
top of that list) does not offer it. After `beta.9` continue with `rc.1`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

MANIFEST = Path(__file__).parent.parent / "custom_components" / "tariffy" / "manifest.json"
PRERELEASE = re.compile(r"-(?P<kind>[A-Za-z]+)\.(?P<number>\d+)$")


def _check(version: str) -> bool:
    match = PRERELEASE.search(version)
    return match is None or int(match["number"]) <= 9


def test_the_manifest_version_has_a_pre_release_number_below_ten():
    version = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
    assert _check(version), (
        f"{version}: GitHub lists a pre-release number of 10 or more below 2, HACS would not offer it. "
        "Continue with the next series (beta.9 -> rc.1), see docs/beta-releases.md"
    )


@pytest.mark.parametrize("version", ["1.27.0", "1.27.0-beta.1", "1.27.0-beta.9", "1.27.0-rc.1", "1.27.0-rc.9"])
def test_these_versions_are_fine(version):
    assert _check(version)


@pytest.mark.parametrize("version", ["1.27.0-beta.10", "1.27.0-rc.12", "1.28.0-beta.11"])
def test_these_versions_are_not(version):
    assert not _check(version)
