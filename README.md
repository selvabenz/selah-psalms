# Selah Psalms

Selah is a Hebrew-first study reader for all 150 Psalms. It presents proposed poetic segmentation, parallelism, component correspondence, whole-Psalm structure, current IRV Tamil projection, and a user-supplied ESV reference text.

## Current editorial state

- 150 close-reading drafts
- 8 individually authored pilot Psalms: 1, 19, 23, 42, 43, 67, 119, and 136
- 142 systematic Hebrew review drafts
- 4,939 segments
- 2,326 parallelism groups
- 7,179 components
- 1,129 structural units
- 0 technical validation errors

Every literary judgment remains `AI_PROPOSED` until a qualified reviewer records a decision. Technical validation establishes referential and packaging integrity; it does not establish the scholarly correctness of the analysis.

## Repository visibility

**Keep this repository private unless you have confirmed publication rights for every included translation and dataset.** The deployable reader contains complete user-supplied ESV text and TTESV-derived links. ESV is Crossway copyright, and TTESV is CC BY-NC. The repository also contains the supplied IRV Tamil text; its publication terms must be confirmed separately.

The raw source archive and supplied scholarship files are intentionally excluded from this bundle. See [RIGHTS-AND-ATTRIBUTIONS.md](RIGHTS-AND-ATTRIBUTIONS.md) and [PUBLIC-RELEASE-CHECKLIST.md](PUBLIC-RELEASE-CHECKLIST.md).

## Open locally

From the repository root:

```powershell
python -m http.server 8765 --directory site
```

Then open <http://127.0.0.1:8765/>.

The reader has no package dependencies, build step, database, analytics, or external service. Review decisions are stored in the browser and can be exported one Psalm at a time.

## Validate

```powershell
python scripts/validate_bundle.py
```

The validator checks the 150 packaged Psalm files, required reader assets, stored project report, excluded raw-source file types, per-file GitHub size limits, and the expected pilot/systematic split.

## GitHub Pages

The workflow in `.github/workflows/pages.yml` validates and deploys `site/`. It is manual by design: pushing the repository does not publish the copyrighted text. Before running it, complete the public-release checklist and confirm whether the resulting Pages site is publicly accessible under your GitHub plan and organization settings.

When publication is authorized:

1. Open **Settings → Pages** and choose **GitHub Actions** as the source.
2. Open **Actions → Validate and deploy Selah to Pages**.
3. Run the workflow from the reviewed commit.

The workflow follows GitHub's custom Pages deployment model using the official Pages actions.

## Repository layout

| Path | Purpose |
|---|---|
| `site/` | Static reader and 150 per-Psalm packages |
| `reports/project-validation.json` | Latest integrity results and limitations |
| `reports/completion-register.json` | Per-Psalm draft inventory and counts |
| `schema/annotation.v0.4.schema.json` | Working annotation schema |
| `docs/EDITORIAL-REVIEW.md` | Recommended human-review sequence |
| `scripts/validate_bundle.py` | Dependency-free release validation |
| `MANIFEST.sha256` | SHA-256 checksums for the tracked release files |

## Creating a GitHub repository

This folder is already initialized as a local Git repository after bundling. Create an empty private repository on GitHub, then add its remote and push:

```powershell
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin main
```

Do not run the Pages workflow until publication rights and Pages visibility have been checked.
