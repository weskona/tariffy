#!/usr/bin/env bash
# Print the changelog section of one version (without its heading) to stdout.
# Usage: release-notes.sh <version without "v"> [changelog file]
# Exits 1 if the section is missing or empty, so a release never ships without notes.
set -euo pipefail

version="${1:?usage: release-notes.sh <version> [changelog]}"
changelog="${2:-CHANGELOG.md}"

notes="$(awk -v ver="$version" '
  index($0, "## [" ver "]") == 1 { found = 1; next }
  found && /^## / { exit }
  found { print }
' "$changelog")"

# trim leading/trailing blank lines
notes="$(printf '%s\n' "$notes" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' | sed '/./,$!d')"

if [ -z "$notes" ]; then
  echo "No changelog section found for version ${version} in ${changelog}" >&2
  exit 1
fi
printf '%s\n' "$notes"
