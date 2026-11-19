"""The brand images of the integration (Home Assistant and HACS show them in the lists)."""

from __future__ import annotations

import struct
from pathlib import Path

import pytest

BRAND = Path(__file__).parent.parent / "custom_components" / "tariffy" / "brand"
SOURCES = Path(__file__).parent.parent / "docs" / "brand"


def _size(path: Path) -> tuple[int, int]:
    """Width and height from the PNG header (no imaging library needed)."""
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path.name} is not a PNG"
    return struct.unpack(">II", data[16:24])


@pytest.mark.parametrize(
    ("name", "size"),
    [("icon.png", (256, 256)), ("icon@2x.png", (512, 512))],
)
def test_the_icon_is_square_and_has_the_sizes_home_assistant_wants(name, size):
    assert _size(BRAND / name) == size


@pytest.mark.parametrize("name", ["logo", "dark_logo"])
def test_the_logo_is_landscape_and_its_short_side_is_in_range(name):
    """Home Assistant: the shortest side of a logo is 128-256 px, 256-512 px for @2x."""
    width, height = _size(BRAND / f"{name}.png")
    assert width > height and 128 <= height <= 256
    width2, height2 = _size(BRAND / f"{name}@2x.png")
    assert (width2, height2) == (width * 2, height * 2) and 256 <= height2 <= 512


def test_the_sources_exist_and_the_renderer_names_every_image():
    for source in ("icon.svg", "logo.svg", "logo-dark.svg", "render.mjs"):
        assert (SOURCES / source).is_file(), source
    renderer = (SOURCES / "render.mjs").read_text(encoding="utf-8")
    for image in BRAND.glob("*.png"):
        assert f'"{image.name}"' in renderer, (
            f"render.mjs does not produce {image.name}"
        )
