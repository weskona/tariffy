#!/usr/bin/env bash
# Tests for release-notes.sh. Run: .github/scripts/test-release-notes.sh
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../.." && pwd)"
script="$here/release-notes.sh"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
fail=0
check() { if [ "$2" = "ok" ]; then echo "ok   - $1"; else echo "FAIL - $1"; fail=1; fi; }

cat > "$tmp/c.md" <<'EOF'
# Changelog

## [Unreleased]

## [2.0.0] - 2026-01-02

### Added

- new thing

## [1.0.0] - 2026-01-01

### Fixed

- old thing

## Before 1.0.0

legacy text

[Unreleased]: https://example.invalid/compare/v2.0.0...HEAD
[1.0.0]: https://example.invalid/releases/tag/v1.0.0
EOF

out="$("$script" 2.0.0 "$tmp/c.md")"; rc=$?
[ $rc -eq 0 ] && [ "$out" = "$(printf '### Added\n\n- new thing')" ] && r=ok || r=bad
check "middle section is extracted without neighbours" $r

out="$("$script" 1.0.0 "$tmp/c.md")"; rc=$?
[ $rc -eq 0 ] && [ "$out" = "$(printf '### Fixed\n\n- old thing')" ] && r=ok || r=bad
check "last versioned section stops at the next '## ' heading and omits link refs" $r

"$script" 9.9.9 "$tmp/c.md" >/dev/null 2>&1 && r=bad || r=ok
check "unknown version fails" $r

"$script" Unreleased "$tmp/c.md" >/dev/null 2>&1 && r=bad || r=ok
check "empty section fails" $r

"$script" 2.0 "$tmp/c.md" >/dev/null 2>&1 && r=bad || r=ok
check "prefix of a version does not match" $r

ver="$(python3 -c 'import json;print(json.load(open("'"$root"'/custom_components/tariffy/manifest.json"))["version"])')"
"$script" "$ver" "$root/CHANGELOG.md" >/dev/null 2>&1 && r=ok || r=bad
check "repo CHANGELOG.md has a section for manifest version ${ver}" $r

exit $fail
