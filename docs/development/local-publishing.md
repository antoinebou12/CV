# Publish the CV and blog locally

The website has one publication source: `docs/` on `main`. The CV hero is at
`/CV/` and the Hugo blog is at `/CV/blog/`. Edit the source files outside `docs/`.
There is no repository deployment Action or separate publishing branch.

Install Python 3.14, Git, and Hugo extended 0.160.1. Initialize the
theme with `git submodule update --init --recursive`. The existing CV PDFs must
be present in `cv-en/resume.pdf` and `cv-fr/resume.pdf`.

Build and validate both parts of the website locally:

```powershell
uv run --no-project --python 3.14 --with tzdata python scripts/deploy/publish_site.py
```

To publish, first commit the intended source changes. From a clean checkout
containing the current `origin/main`, run:

```powershell
uv run --no-project --python 3.14 --with tzdata python scripts/deploy/publish_site.py --publish
```

The script uses the checked-in theme CSS, stages the CV and blog together, validates the site,
updates `docs/`, commits that folder, and pushes to `main` without force. Existing
development documentation in `docs/` is preserved. Untracked source files are
not included in the commit: commit any new source files before publishing.

GitHub Pages settings must use **Deploy from a branch**, **main**, **/docs**.
GitHub still processes the branch publication on its servers; an account-level
Pages or Actions restriction can prevent publication even when the local build
and push succeed. A successful push alone does not confirm the live release.
