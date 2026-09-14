# NCToolkit website

Source for the NCToolkit marketing/documentation site (`docs-site/` in the
main nctoolkit repository), published to GitHub Pages. Plain static
HTML/CSS/JS — no build step, no dependencies. Layout, theming and the
archiving approach are carried over from the sister project
[OceanVal's docs site](https://github.com/pmlmodelling/oceanVal/tree/main/docs-site),
for a consistent look across PML's Marine Systems Modelling group tools.

## Structure

```
index.html            Landing page
installing.html         \
quickstart.html           \
guide-basics.html           \
guide-analysis.html           Documentation, mirrors docs/source/*.rst and
guide-advanced.html            *.ipynb in the nctoolkit package, redesigned
api.html                      /
data-formats.html            /
backends.html               /
qa.html                    /
about.html                /
news.html                 Release highlights; full history lives on GitHub
version-history.html      Links to archive/vX.Y.Z/ snapshots - see "Archived
                           versions" below
assets/
  css/style.css      Design system (design tokens, components)
  js/main.js         Nav + dropdowns, copy-to-clipboard, FAQ accordion,
                      table search/filter, scrollspy
  img/               Wordmark (NC in ink, Toolkit in teal), PML logo, favicon
archive/             Per-release snapshots of the twelve pages above (minus
                      version-history.html itself) + assets/, written by
                      .github/workflows/docs-archive.yml. Don't hand-edit it.
```

Unlike OceanVal's docs site, this one *does* have an `index.html` landing
page — NCToolkit is a general-purpose library with many more doc pages than
OceanVal, so a proper landing page and grouped dropdown navigation (under
"Guide", "Data" and "About") make sense here. Don't remove it by analogy
with OceanVal; that omission was specific to OceanVal's report-output pages,
not something to copy blindly.

## Previewing locally

```sh
cd docs-site
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploying to GitHub Pages

Deployment is automated by `.github/workflows/pages.yml` (at the repository
root, not under `docs-site/`), which publishes this directory as-is (no build
step) whenever a push to `master` touches `docs-site/**`.

To turn it on:

1. In the repo's **Settings → Pages**, set **Source** to **GitHub Actions**
   (not "Deploy from a branch").
2. Push to `master` (or run the workflow manually from the **Actions** tab —
   it has `workflow_dispatch` enabled). The site publishes to
   `https://pmlmodelling.github.io/nctoolkit/`.

The included `.nojekyll` file stops GitHub Pages from running its default
Jekyll processing, which isn't needed here and can interfere with files/paths
starting with an underscore.

**`pages.yml` must stay the only Pages-deploying workflow.** It replaces an
earlier `static.yml` that uploaded the whole repository root (`path: '.'`) on
every push to `master`, sharing the same `concurrency: group: "pages"` this
workflow uses — a second such workflow will race this one, and whichever
finishes last "wins" and publishes whatever it uploaded, silently. If you're
troubleshooting a deploy, check `.github/workflows/` for exactly one Pages
workflow before assuming anything else is wrong.

## Version badge

Every page shows the latest NCToolkit release next to the header logo
(`<span id="nctoolkit-docs-version" class="brand-version">`). It's entirely
client-side: `assets/js/main.js` fetches `https://pypi.org/pypi/nctoolkit/json`
on page load and fills in the placeholder `v&hellip;` with the current
version. Don't hardcode a version number here — it needs that literal
placeholder text to find and replace.

This is a plain "what's the latest release" indicator, not a version
switcher — only one version of the site is served at the root. See "Archived
versions" below for the version-history page instead.

## Archived versions

`.github/workflows/docs-archive.yml` runs whenever a GitHub Release is
created. It reads the version from `setup.py` (the source of truth — not the
release's tag name, not PyPI, since PyPI's publish can race this workflow),
copies this directory's pages plus `assets/` into `archive/vX.Y.Z/`
(excluding `version-history.html` itself, and rewriting its links to point
back at the live, shared copy two levels up), and freezes the header badge in
the snapshot to a plain "vX.Y.Z (archived)" span — it must never update
again, unlike the live badge. It then updates `archive/versions.json` (newest
first) and rewrites the list between the
`<!-- NCTOOLKIT_VERSION_HISTORY_START -->` /
`<!-- NCTOOLKIT_VERSION_HISTORY_END -->` markers in `version-history.html` to
match. Finally it commits and pushes that to `master` and explicitly
dispatches `pages.yml` (a `GITHUB_TOKEN` push doesn't trigger other workflows
on its own, so this can't just rely on the normal push trigger).

Existing snapshots are never touched by a later release — only a brand new
`archive/vX.Y.Z/` directory gets created each time. If that directory already
exists (e.g. the workflow re-ran for some reason), it's left alone rather
than overwritten.

`version-history.html` itself is a normal hand-authored page (same header,
nav, and footer as the rest of the site — keep it in sync with the other
eleven if you change shared markup) with one auto-generated `<ul>` in the
middle, plus a small "no archived snapshots yet" message that
`assets/js/main.js` hides automatically once the list has entries. Don't
hand-edit between the markers; everything else on the page is yours to edit
like any other.

`archive/versions.json` starts as `[]` — nothing has been archived yet. The
first entry is created automatically the next time a GitHub Release is
published.

## Updating content

Page content is authored by hand to match the current nctoolkit docs
(`docs/source/*.rst`, `docs/source/*.ipynb` and the package README) — there's
no templating engine, so if the underlying package docs change, update the
corresponding `.html` file(s) directly. Shared header/nav/footer markup is
duplicated across pages (no static-site generator), so a nav or footer change
should be applied to all twelve `.html` files (eleven content pages plus
`version-history.html`).

Rough mapping from Sphinx source to site pages:

| `docs/source/*.rst` / `*.ipynb`                                              | `docs-site/*.html`   |
| ------------------------------------------------------------------------------ | --------------------- |
| `installing.rst`                                                               | `installing.html`     |
| `introduction.rst`                                                             | `quickstart.html`     |
| `datasets.ipynb`, `exporting.rst`, `subsetting.rst`, `globals.rst`             | `guide-basics.html`   |
| `temporals.rst`, `verticals.ipynb`, `interpolation.rst`, `ensembles.rst`, `adding.ipynb`, `matchpoint.ipynb` | `guide-analysis.html` |
| `plotting.ipynb`/`visualization.rst`, `parallel.rst`, `hacks.rst`, `troubleshoot.rst` | `guide-advanced.html` |
| `api.rst`                                                                       | `api.html`             |
| `supported.rst`                                                                 | `data-formats.html`   |
| `backends.rst`                                                                  | `backends.html`        |
| `troubleshoot.rst`, `hacks.rst` (as FAQs)                                       | `qa.html`               |
| `info.rst`, `citation.rst`, `contributing.rst`                                 | `about.html`           |
| `news.rst`                                                                      | `news.html`             |
