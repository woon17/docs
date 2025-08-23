# Documentation Site

This repository contains technical documentation built with MkDocs Material.

## Local Development

### Prerequisites

Install Python 3.x and pip, then install the required dependencies:

```bash
pip install mkdocs-material pytz
```

### Running Locally

To run the documentation site locally and see your changes in real-time:

```bash
mkdocs serve
```

This will start a local server at `http://127.0.0.1:8000/` with live reload functionality. Any changes you make to the markdown files will automatically refresh the browser.

### Building the Site

To build the static site for deployment:

```bash
mkdocs build
```

The generated site will be in the `site/` directory.

### Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions.

## Project Structure

- `docs/` - All documentation content in Markdown format
- `mkdocs.yml` - MkDocs configuration file
- `overrides/` - Custom templates and theme overrides
- `site/` - Generated static site (auto-generated)

## Adding Content

1. Create new `.md` files in the appropriate `docs/` subdirectory
2. Update the navigation in `mkdocs.yml` if needed
3. Use `mkdocs serve` to preview your changes locally
4. Commit and push to deploy