#!/usr/bin/env bash
# Tests for release-plan.sh. Run: .github/scripts/test-release-plan.sh
set -uo pipefail
script="$(cd "$(dirname "$0")" && pwd)/release-plan.sh"
fail=0
check() { if [ "$2" = ok ]; then echo "ok   - $1"; else echo "FAIL - $1"; fail=1; fi; }

# plan <version> <type> <name> <expected key=value lines separated by |>
plan() {
  local desc="$1" out expected="$5"
  out="$("$script" "$2" "$3" "$4" 2>&1 | paste -sd'|' -)"
  [ "$out" = "$expected" ] && check "$desc" ok || { echo "   got: $out"; check "$desc" bad; }
}
fails() {
  "$script" "$2" "$3" "$4" >/dev/null 2>&1 && check "$1" bad || check "$1" ok
}

plan "stable on main is released"       1.27.0        branch main 'tag=v1.27.0|number=1.27.0|prerelease=false|action=release'
plan "beta on beta is a pre-release"    1.27.0-beta.1 branch beta 'tag=v1.27.0-beta.1|number=1.27.0-beta.1|prerelease=true|action=release'
plan "rc on beta is a pre-release"      1.27.0-rc.2   branch beta 'tag=v1.27.0-rc.2|number=1.27.0-rc.2|prerelease=true|action=release'
plan "beta version on main is skipped"  1.27.0-beta.1 branch main 'tag=v1.27.0-beta.1|number=1.27.0-beta.1|prerelease=true|action=skip|reason=pre-release 1.27.0-beta.1 is only released from the beta branch'
plan "stable version on beta is skipped" 1.26.5       branch beta 'tag=v1.26.5|number=1.26.5|prerelease=false|action=skip|reason=stable 1.26.5 is only released from main, the beta branch publishes pre-releases'
plan "other branches are skipped"       1.27.0        branch feature 'tag=v1.27.0|number=1.27.0|prerelease=false|action=skip|reason=branch feature is not a release branch'
plan "matching tag is released"         1.27.0        tag v1.27.0 'tag=v1.27.0|number=1.27.0|prerelease=false|action=release'
plan "matching beta tag is a pre-release" 1.27.0-beta.1 tag v1.27.0-beta.1 'tag=v1.27.0-beta.1|number=1.27.0-beta.1|prerelease=true|action=release'

fails "tag that does not match the version fails"   1.27.0 tag v1.26.9
fails "beta tag for a stable version fails"         1.27.0 tag v1.27.0-beta.1
fails "invalid version fails"                       1.27   branch main
fails "pep440 style beta is rejected"               1.27.0b1 branch beta
fails "leading v in the version is rejected"        v1.27.0 branch main
fails "unknown ref type fails"                      1.27.0 pull_request main

exit $fail
