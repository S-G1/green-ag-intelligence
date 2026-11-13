# Green Ag Intelligence Platform

**Precision agriculture decision support portfolio application**

A modular Python/Plotly Dash application for exploring field records, NDVI, weather, soil, terrain, and environmental-risk displays in a Caroline County, Maryland case study.

[Source code](https://github.com/S-G1/green-ag-intelligence) · [Technical case study](DASHBOARD.md) · [Live demo preview](https://green-ag-intelligence-1.onrender.com/) · [Data validation status](DATA_VALIDATION.md)

[![Playwright CI](https://github.com/S-G1/green-ag-intelligence/actions/workflows/playwright.yml/badge.svg?branch=main)](https://github.com/S-G1/green-ag-intelligence/actions/workflows/playwright.yml)

## What it does

The project brings agricultural information into an interactive interface for comparing fields and exploring possible scouting priorities. It demonstrates application design, data visualization, and agricultural decision-support workflows.

- Field and map views with selectable analytical layers.
- Monthly NDVI comparisons and crop-health views.
- Weather charts covering 2021–2025.
- Soil, drainage, elevation, slope, and field-comparison displays.
- KPI summaries, illustrative rule-based recommendations, and reports.
- CSV and multi-sheet Excel exports.
- Modular components and callbacks, navigation, search, demo mode, and theme controls.

These are portfolio capabilities. They do not establish commercial customer use, validated agronomic recommendations, or a production farm-management service.

## Preview and current readiness

The hosted application loaded during a desktop browser check on November 13, 2026. Demo activation, weather navigation, and field-search responses were observed. Full readiness has not been established: map rendering encountered a WebGL error in that browser, horizontal overflow and KPI-state changes were observed, and mobile, private-window, and coherent theme behavior still need verification.

Use the source code and technical case study as the primary portfolio references until the live-demo and data checks in [DATA_VALIDATION.md](DATA_VALIDATION.md) are complete. Capture current desktop and mobile screenshots after those checks; this repository does not yet include a verified screenshot preview.

## Data sources and scope

`data.py` embeds ten field records, twelve NDVI values per field for 2025, and sixty monthly weather records for 2021–2025. The application uses this embedded snapshot rather than querying the source services at runtime.

The project documentation attributes upstream data to NASA POWER, USGS 3DEP, NRCS SSURGO, USDA NASS Cropland Data Layer, and OpenStreetMap, and describes Sentinel-2/Landsat NDVI processing. The corresponding source extracts and reproducible upstream processing are not included in this repository, so those attribution and derivation claims need source reconciliation.

Current checks found zero-area polygon rings, impossible monthly counts under the label “heat-stress days,” and differences between documented and embedded acreage, crop, soil, and risk summaries. Do not interpret the displayed recommendations as validated agronomic advice. See [DATA_VALIDATION.md](DATA_VALIDATION.md) for exact findings and acceptance checks.

## Architecture and stack

- **Application:** Python, Plotly Dash, dash-bootstrap-components.
- **Data and charts:** Pandas, NumPy, Plotly; openpyxl for Excel.
- **Structure:** `app.py`, `config.py`, and `data.py`; reusable UI in `components/`; interactions, navigation, themes, and exports in `callbacks/`.
- **Deployment configuration:** Gunicorn, Render blueprint, and Heroku Procfile.
- **Browser checks:** Playwright/Chromium through GitHub Actions.

## Analytical interpretation

The interface presents NDVI, soil, terrain, weather, and risk information together. Quantitative findings and field-level management recommendations remain provisional until the dataset, units, geometry, provenance, and category thresholds pass validation. The technical case study distinguishes documented intentions from current code evidence.

## Testing and CI

The workflow in `.github/workflows/playwright.yml` starts the app and runs:

```bash
python smoke_test.py
python test_app.py
```

A fresh installation on November 13, 2026 selected Plotly 7.1.0 and failed at startup because the app uses the removed `Scattermapbox` API. `requirements.txt` now caps Plotly below 7 pending a tested map migration. Consult the pull request checks for the current result.

The main-branch push workflow for commit `2a0b6f0` completed successfully on August 1, 2026. That result is evidence of that run, not a check of current hosted deployment health or data accuracy. The smoke script logs errors without failing on all of them, and the comprehensive script fails for its collected functional failures but permits console/page errors. Extend meaningful assertions when repairing the application.

## Quick Start

### Prerequisites

- Python 3.10+
- pip
- (Optional) Git

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/S-G1/green-ag-intelligence.git
cd green-ag-intelligence

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
python app.py
```

Open http://localhost:8050 in your browser.

Use **Launch Demo Mode** to explore the Maryland case study. Allow time for server startup and client-side charts.

## Deployment

### Deploy to Render (Recommended)

1. Push this repo to GitHub
2. Connect repo in [Render Dashboard](https://dashboard.render.com)
3. Render auto-detects `render.yaml`
4. Deploys automatically on every push

**Start command:** `gunicorn app:server`

**Environment variables:**
- `MY_FARM_ADVISOR_RUNTIME` — Path to runtime data-pipeline (default: `~/my-farm-advisor-runtime/data-pipeline`)
- `PORT` — Server port (default: `8050`)
- `DASH_DEBUG` — Enable debug mode (`0` or `1`)

### Deploy to Heroku

```bash
heroku create green-ag-intelligence
heroku config:set DASH_DEBUG=0
git push heroku main
```

## Documentation

- [Technical case study and AI development notes](DASHBOARD.md)
- [Data validation findings and repair sequence](DATA_VALIDATION.md)
- [Browser workflow](.github/workflows/playwright.yml)

## AI assistance

Development used AI coding assistance within a human-directed workflow. The project documentation describes human work in defining requirements, reviewing implementation, debugging, interpreting data, and preparing deployment. See the technical case study for the detailed account. The application does not document a deployed machine-learning model or runtime LLM service.

## Author

Stephon Green

## License

A license has not yet been established by a LICENSE file in this repository. The previous Apache-2.0 label was removed pending the owner's explicit license choice. Do not assume a reuse grant from the former label.

