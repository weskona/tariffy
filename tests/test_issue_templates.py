"""Guard the GitHub issue forms: GitHub silently disables a form that breaks its schema."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

TEMPLATE_DIR = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
FORMS = sorted(p for p in TEMPLATE_DIR.glob("*.yml") if p.name != "config.yml")
ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
TYPES = {"markdown", "textarea", "input", "dropdown", "checkboxes"}


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_forms_exist():
    assert {p.name for p in FORMS} >= {"bug_report.yml", "feature_request.yml"}


@pytest.mark.parametrize("path", FORMS, ids=lambda p: p.name)
class TestIssueForm:
    def test_top_level_keys(self, path):
        form = _load(path)
        for key in ("name", "description", "body"):
            assert form.get(key), f"{key} missing"

    def test_title_asks_for_a_summary(self, path):
        assert "<short summary>" in _load(path)["title"]

    def test_fields_are_valid(self, path):
        ids = []
        fields = _load(path)["body"]
        assert any(f["type"] != "markdown" for f in fields), "needs an input field"
        for field in fields:
            assert field["type"] in TYPES
            attrs = field.get("attributes", {})
            if field["type"] == "markdown":
                assert attrs.get("value"), "markdown needs a value"
                assert "id" not in field or field["id"]
                continue
            assert attrs.get("label"), f"{field.get('id')} needs a label"
            assert ID_PATTERN.match(field["id"]), field["id"]
            ids.append(field["id"])
            if field["type"] == "dropdown":
                options = attrs["options"]
                assert options and len(options) == len(set(options))
                assert "None" not in options
            if field["type"] == "checkboxes":
                assert "validations" not in field, "use required on the options"
                assert all(o.get("label") for o in attrs["options"])
        assert len(ids) == len(set(ids)), "duplicate ids"

    def test_labels_are_the_known_ones(self, path):
        assert set(_load(path)["labels"]) <= {"bug", "enhancement"}


def test_bug_report_only_requires_what_applies_to_every_bug():
    form = _load(TEMPLATE_DIR / "bug_report.yml")
    required = {
        f["id"] for f in form["body"] if f.get("validations", {}).get("required")
    }
    # consumption sensor, state_class and contract start only matter for some bugs
    assert required == {"tariffy_version", "ha_version", "install_method", "area", "sparte", "problem"}


def test_config_keeps_blank_issues_disabled():
    config = _load(TEMPLATE_DIR / "config.yml")
    assert config["blank_issues_enabled"] is False
    assert all(link["url"].startswith("https://github.com/weskona/tariffy") for link in config["contact_links"])
