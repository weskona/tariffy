# Beta releases

Unfinished work (for example the planned Tariffy panel) is published as **beta pre-releases**,
so normal users never receive it by accident.

## For testers

1. HACS → Tariffy → ⋮ → **Redownload**, enable **Show beta versions**.
2. Pick a version like `1.27.0-beta.1` and restart Home Assistant.
3. Report problems with the bug report form and mention the exact beta version.

Without "Show beta versions" HACS only offers stable releases. A beta never replaces the
stable version for anyone who did not opt in.

## For maintainers

| | stable | beta |
|---|---|---|
| Branch | `main` | `beta` |
| Version in `manifest.json` | `1.27.0` | `1.27.0-beta.1`, `-beta.2`, ... (`-rc.1` before a stable release) |
| Changelog section | `## [1.27.0]` | `## [1.27.0-beta.1]` |
| GitHub release | normal, marked latest | **pre-release**, never marked latest |

How it works:

- The `Release` workflow runs on pushes to `main` and `beta` and reads the version from
  `manifest.json`. A version without a release gets a tag, a release and `tariffy.zip`.
- A version on the wrong branch is **skipped** (a stable version on `beta`, a beta version on
  `main`), so merging `main` into `beta` never publishes anything. The rules live in
  `.github/scripts/release-plan.sh` and are tested in `.github/scripts/test-release-plan.sh`.
- **One pull request per beta:** a feature pull request into `beta` also raises the version in
  `manifest.json` and moves its `Unreleased` changelog entries into the new section. Merging it
  publishes the beta, so no separate version pull request is needed.
- `main` is merged into `beta` only after a stable release (or when a fix from `main` is
  needed in the beta), not after every hotfix.
- Hotfixes for stable users go to `main` and are released from there. They never contain
  unfinished beta code. Merge `main` into `beta` afterwards to keep the beta current.
- To promote a beta, merge `beta` into `main` through a pull request, set the stable version
  and changelog section there, and merge. The workflow then publishes the stable release.
- Run the `Release` workflow manually with `dry_run` to build the zip and notes without
  publishing anything.
