# 🌱 Green Ag Intelligence Platform

**Single-File Self-Contained Dash App** — All data embedded, zero external dependencies.

Real Caroline County, MD data from NASA POWER, USGS 3DEP, SSURGO, and CDL.

---

## 🚀 Quick Start

### Local Development

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:8050

### Deploy to Render

1. Push this repo to GitHub
2. Connect repo in [Render Dashboard](https://dashboard.render.com)
3. Render auto-detects `render.yaml`
4. Deploys automatically on every push

### Deploy to Heroku

```bash
heroku create green-ag-intelligence
heroku config:set DASH_DEBUG=0
git push heroku main
```

---

## 📊 Data Sources

- **Field Boundaries**: OpenStreetMap / Overpass API
- **Weather**: NASA POWER S3 Zarr (daily, 2021–2026)
- **Soil**: NRCS SSURGO
- **CDL**: USDA NASS Cropland Data Layer (2021–2025)
- **DEM**: USGS 3DEP 1-meter (TNM)

---

## 📁 File Structure

```
green-ag-intelligence/
├── app.py              # Single self-contained file (~67KB)
├── requirements.txt    # Python dependencies
├── Procfile            # Heroku deployment
├── render.yaml         # Render blueprint
└── README.md           # This file
```

---

## 🎨 Features

- **Landing Page** → Dashboard navigation
- **Interactive Map** — 4 layers: NDVI, Risk, Heat Stress, Rainfall
- **NDVI Animation** — Monthly slider with play/loop
- **Weather Charts** — 4-panel: temp, rainfall, solar, humidity
- **Heat Stress** — Days > 30°C by month
- **Field Table** — Sortable, searchable, exportable
- **Stress Gauge** — 0–100 index per field
- **Recommendations** — Severity-coded advice cards
- **Theme Toggle** — Light/Dark mode
- **CSV Export** — All charts and table data
- **Add Farm Modal** — UI for new farm creation

---

## 👤 Author

**Stephon Green** — Agricultural Data Analytics | Geospatial Intelligence

---

## 📜 License

Apache-2.0
