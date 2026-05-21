# GitHub Pages Setup Instructions

## Enable GitHub Pages

Before the deployment workflow can run, you need to enable GitHub Pages in your repository settings:

1. Go to your repository on GitHub
2. Click on **Settings**
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select:
   - **Source**: `GitHub Actions` (not "Deploy from a branch")
5. Save the settings

Once enabled, the workflow will automatically deploy your site when you push to the `main` or `master` branch.

### Project site URL and repo name

For this repository (`antoinebou12/CV`), the GitHub Pages project URL is:

`https://antoinebou12.github.io/CV/`

The Hugo blog is deployed under **`/CV/blog/`** (the first path segment must match the **repository name** on GitHub exactly, including casing). It is **not** at `https://antoinebou12.github.io/blog/`.

## Alternative: Manual Setup

If you prefer to deploy from a branch instead:

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - **Branch**: `main` (or `master`)
   - **Folder**: `/ (root)`
3. Click **Save**

This serves files **as they exist on that branch**. It will **not** include the Hugo blog at `/blog/` unless you commit a pre-built `blog/` tree (or change the workflow), because the default pipeline builds the blog only on the runner into `_site/blog/` and never commits it to `main`.

For this project, use **GitHub Actions** as the Pages source so `deploy.yml` can publish the full `_site` output.

### Vercel vs GitHub Pages

The canonical public CV URL is the custom domain on GitHub Pages (`https://antoineboucher.info/CV/`). Root `vercel.json` only registers `index-en.html` and `index-fr.html` as static builds; a Vercel deployment must still expose `css/`, `papers/`, hero images, and PDF paths or those assets will 404. Prefer the GitHub Actions `_site` artifact for full-site previews.
