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

## Alternative: Manual Setup

If you prefer to deploy from a branch instead:

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - **Branch**: `main` (or `master`)
   - **Folder**: `/ (root)`
3. Click **Save**

This will serve your `index.html` directly from the root of your repository.
