# 🌱 Green Ag Intelligence Platform

**Version 2.0 — Enterprise Agricultural Intelligence Platform**

Environmental Risk Monitoring & Decision Support

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

## 📁 Architecture

```
green-ag-intelligence/
├── app.py                    # Entry point (150 lines)
├── config.py                 # Design tokens, constants, KPI config
├── data.py                   # Embedded real Caroline County data
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment
├── render.yaml               # Render auto-deploy config
│
├── assets/
│   └── custom.css            # Complete design system (800+ lines)
│
├── components/
│   ├── header.py             # Enterprise header with notifications
│   ├── search.py             # Global search bar (Ctrl+K)
│   ├── filters.py            # Inline filter toolbar
│   ├── kpis.py               # 6 KPI cards with sparklines
│   ├── map_component.py      # Full-height interactive map
│   ├── ndvi_panel.py         # Chart + slider + play/loop
│   ├── weather_panel.py      # 4-panel weather analytics
│   ├── field_table.py        # Sortable, searchable table
│   ├── gauge.py              # Animated circular stress gauge
│   ├── recommendations.py    # Severity-coded advice cards
│   ├── command_palette.py    # Ctrl+K overlay
│   ├── onboarding.py         # First-time welcome dialog
│   └── footer.py             # Professional footer
│
├── callbacks/
│   ├── interactions.py       # Connected field→all updates
│   ├── navigation.py         # Demo mode, onboarding
│   ├── theme.py              # Light/dark toggle
│   └── export.py             # CSV/PDF export
│
└── charts/                   # Plotly Chart Studio JSON files
    ├── chart_map.json
    ├── chart_ndvi.json
    ├── chart_weather.json
    ├── chart_heat_stress.json
    └── chart_gauge.json
```

---

## 🎨 Features

### Dashboard (Direct Launch — No Landing Page)
- **Enterprise Header** — Farm info pill, notifications, theme/settings/export
- **Global Search** — Centered search bar, fuzzy matching, Ctrl+K shortcut
- **Filter Toolbar** — Inline compact filters, instant updates, reset/refresh/export
- **KPI Cards** — 6 metrics with sparkline trends, color-coded indicators
- **Interactive Map** — Full-height Plotly Mapbox, 4 layers (NDVI/Risk/Heat/Rain)
- **NDVI Panel** — Time series chart, month slider, play/loop animation
- **Weather Analytics** — 4-panel: temperature, rainfall, solar, humidity
- **Field Table** — Sortable, searchable, status badges, row actions
- **Stress Gauge** — Animated circular gauge with color zones
- **Recommendations** — Severity cards: healthy/monitor/alert/critical

### UX Features
- **Command Palette** — Ctrl+K, fuzzy search, action shortcuts
- **Onboarding** — First-time dialog: Open Farm / Add Farm / Launch Demo
- **Demo Mode** — Auto-populates all data, plays NDVI animation, badge in header
- **Theme Toggle** — Light/dark with system preference detection
- **Empty States** — Professional placeholders with action buttons
- **Loading States** — Skeleton loaders for all components
- **Animations** — Fade-in, slide-up, hover elevation, smooth transitions
- **Accessibility** — WCAG AA, keyboard nav, focus rings, ARIA labels
- **Responsive** — Collapsible navigation, stacked layout below 768px

---

## 📊 Data Sources

- **Field Boundaries**: OpenStreetMap / Overpass API
- **Weather**: NASA POWER S3 Zarr (daily, 2021–2026)
- **Soil**: NRCS SSURGO
- **CDL**: USDA NASS Cropland Data Layer (2021–2025)
- **DEM**: USGS 3DEP 1-meter (TNM)

---

## 👤 Author

**Stephon Green** — Agricultural Data Analytics | Geospatial Intelligence

---

## 📜 License

Apache-2.0
