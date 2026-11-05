#!/usr/bin/env bash
# Decide what the release workflow does for a manifest version on a ref.
# Usage: release-plan.sh <manifest version> <ref type: branch|tag> <ref name>
# Prints key=value lines: tag, number, prerelease, action (release|skip) and,
# for skip, a reason. Exits 1 on an invalid version or a tag that does not match.
#
# Rules:
#   - stable versions (1.27.0) are released from main, pre-releases (1.27.0-beta.1)
#     only from the beta branch. A version on the "wrong" branch is skipped, so
#     merging main into beta (or the reverse) never publishes anything by accident.
#   - a pushed tag must be exactly v<version> and is always released.
set -euo pipefail

version="${1:?usage: release-plan.sh <version> <ref type> <ref name>}"
ref_type="${2:?usage: release-plan.sh <version> <ref type> <ref name>}"
ref_name="${3:?usage: release-plan.sh <version> <ref type> <ref name>}"

semver='^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z]+(\.[0-9A-Za-z]+)*)?$'
if ! [[ "$version" =~ $semver ]]; then
  echo "Version '${version}' is not a valid semantic version (expected 1.2.3 or 1.2.3-beta.1)" >&2
  exit 1
fi

prerelease=false
if [[ "$version" == *-* ]]; then
  prerelease=true
fi
tag="v${version}"
action=release
reason=""

case "$ref_type" in
  tag)
    if [ "$ref_name" != "$tag" ]; then
      echo "Tag ${ref_name} does not match manifest.json version ${version} (expected ${tag})" >&2
      exit 1
    fi
    ;;
  branch)
    case "$ref_name" in
      main)
        if [ "$prerelease" = true ]; then
          action=skip
          reason="pre-release ${version} is only released from the beta branch"
        fi
        ;;
      beta)
        if [ "$prerelease" = false ]; then
          action=skip
          reason="stable ${version} is only released from main, the beta branch publishes pre-releases"
        fi
        ;;
      *)
        action=skip
        reason="branch ${ref_name} is not a release branch"
        ;;
    esac
    ;;
  *)
    echo "Unknown ref type '${ref_type}'" >&2
    exit 1
    ;;
esac

printf 'tag=%s\nnumber=%s\nprerelease=%s\naction=%s\n' "$tag" "$version" "$prerelease" "$action"
if [ -n "$reason" ]; then
  printf 'reason=%s\n' "$reason"
fi
