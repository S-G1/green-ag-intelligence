# 🌱 Green Ag Intelligence Platform

**Version 2.2 — Enterprise Agricultural Intelligence Platform**

Environmental Risk Monitoring & Decision Support

Real Caroline County, MD data from NASA POWER, USGS 3DEP, SSURGO, and CDL.

---

## 🚀 Quick Start

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

### Deploy to Render (Recommended)

1. Push this repo to GitHub
2. Connect repo in [Render Dashboard](https://dashboard.render.com)
3. Render auto-detects `render.yaml`
4. Deploys automatically on every push

**Start command:** `gunicorn app:server`

### Deploy to Heroku

```bash
heroku create green-ag-intelligence
heroku config:set DASH_DEBUG=0
git push heroku main
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `dash` | >=2.18.0 | Web application framework |
| `dash-bootstrap-components` | >=1.6.0 | Bootstrap UI components |
| `plotly` | >=5.24.0 | Interactive visualizations |
| `pandas` | >=2.2.0 | Data manipulation |
| `numpy` | >=2.0.0 | Numerical computing |
| `gunicorn` | >=23.0.0 | WSGI production server |
| `openpyxl` | >=3.1.0 | Excel export engine |

See `requirements.txt` for exact versions.

---

## 📁 Architecture

```
green-ag-intelligence/
├── app.py                    # Entry point — layout + routing + stores
├── config.py                 # Design tokens, KPI config, map config
├── data.py                   # Embedded real Caroline County data (10 fields, 5yr weather)
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment
├── render.yaml               # Render auto-deploy config
│
├── assets/
│   ├── custom.css            # Complete design system (900+ lines, light/dark themes)
│   └── nav_rail.css          # Navigation rail styles
│
├── components/               # Reusable UI components
│   ├── header.py             # Enterprise header with farm pill, notifications, theme
│   ├── nav_rail.py           # Collapsible 8-section sidebar
│   ├── search.py             # Global search bar with field dropdown results
│   ├── filters.py            # Inline filter toolbar
│   ├── kpis.py               # 6 KPI cards with sparklines
│   ├── map_component.py      # Overview interactive map (10 layers)
│   ├── map_explorer.py       # Full-screen Map Explorer page
│   ├── ndvi_panel.py         # NDVI bar chart + slider + play/loop
│   ├── weather_panel.py      # Overview 4-panel weather analytics
│   ├── weather_page.py       # Dedicated Weather page (multi-year)
│   ├── field_table.py        # Sortable, paginated, searchable table
│   ├── crop_health.py        # NDVI heatmap + field health cards
│   ├── soil_terrain.py       # Soil scatter, elevation chart, soil table
│   ├── farm_management.py    # Field inventory + management actions
│   ├── reports.py            # Crop pie, stress bar, weather summaries
│   ├── settings.py           # Theme, notifications, data preferences
│   ├── gauge.py              # Animated circular stress gauge
│   ├── recommendations.py    # Severity-coded advice cards
│   ├── command_palette.py    # Ctrl+K overlay with fuzzy search
│   ├── onboarding.py         # First-time welcome dialog
│   └── footer.py             # Professional footer
│
├── callbacks/                # Business logic
│   ├── interactions.py       # Cross-component filtering, search, NDVI play
│   ├── navigation.py         # Page routing, demo mode, command palette
│   ├── theme.py              # Light/dark toggle
│   └── export.py             # CSV, Excel, multi-sheet export
│
└── charts/                   # Plotly Chart Studio JSON snapshots
    ├── chart_map.json
    ├── chart_ndvi.json
    ├── chart_weather.json
    ├── chart_heat_stress.json
    └── chart_gauge.json
```

---

## 📊 Dashboard Pages (8 Sections)

The app launches directly into the **Overview** dashboard. All sections are accessible via the left navigation rail.

### 1. Overview (Default)
- **6 KPI Cards** — Total Fields, Total Acres, Avg NDVI, Avg Stress, High Risk count, Well Drained count
- **Interactive Map** — Plotly Mapbox with field boundaries, 10 layer toggles (NDVI, Risk, Heat Stress, Rainfall, Soil, Slope, Elevation, Satellite, Dark, Light)
- **NDVI Panel** — Bar chart with monthly sorting + play/loop animation
- **Weather Panel** — 4-tab analytics: Combined, Rainfall, Temperature, Heat Stress
- **Field Table** — Paginated, searchable, exportable (CSV + multi-sheet Excel)
- **Stress Gauge** — Circular gauge with risk categories + historical trend
- **Recommendations** — Confidence-scored cards with severity (healthy/monitor/alert/critical)

### 2. Map Explorer
- Full-screen interactive Plotly Mapbox
- Field polygon overlays from OpenStreetMap
- Sidebar with layer toggles and field list
- Hover info with acres, crop, NDVI values

### 3. Crop Health
- **NDVI Timeline Comparison** — All 10 fields on one chart (color-coded by stress)
- **NDVI Heatmap** — Field × Month matrix (RdYlGn colorscale)
- **Field Health Cards** — Per-field avg NDVI, peak NDVI, peak month, stress, health status badge

### 4. Weather
- **Temperature Trends** — 2021–2025 multi-line with max temp dashed overlay
- **Monthly Rainfall** — Grouped bar chart by year
- **Heat Stress Days** — Area chart showing cumulative stress days per month
- **Annual Summary Cards** — Rainfall, avg temp, heat stress days per year

### 5. Soil & Terrain
- **pH vs Organic Matter Scatter** — Bubble size = field area, color = drainage
- **Elevation & Slope Combo Chart** — Dual-axis line + bar chart
- **Drainage Summary Cards** — Well drained vs poorly drained field counts
- **Soil Properties Table** — Full 10-field detail with pH, OM%, CEC, drainage, elevation, slope

### 6. Farm Management
- **Summary Cards** — Total fields, acres, crop types, avg field size
- **Field Inventory Cards** — Per-field cards with crop, soil, NDVI, stress, View/Edit/Report actions

### 7. Reports
- **Crop Distribution** — Donut pie chart
- **Stress Risk Distribution** — Bar chart (Low/Medium/High)
- **Annual Weather Summary Table** — 2021–2025 rainfall, temp, stress days
- **Batch Export** — CSV and Excel download buttons

### 8. Settings
- **Appearance** — Theme toggle, reduced motion switch
- **Notifications** — Email alerts, weekly summary, weather warnings
- **Data Preferences** — Default year selector, measurement units
- **About** — Version, data sources, author info

---

## 🎨 UX Features

- **Command Palette** — `Ctrl+K` opens overlay, real-time filtering, navigates to any page, launches demo, exports data
- **Onboarding** — First-time dialog: Open Farm / Add Farm / Launch Demo
- **Demo Mode** — Auto-starts NDVI animation, badge in header, exit button
- **Theme Toggle** — Light/dark mode with CSS custom properties
- **Global Search** — Search fields by name, crop, or soil type; dropdown results
- **Responsive** — Collapsible navigation rail (240px → 72px), stacked layout below 768px
- **Keyboard Shortcuts** — `Ctrl+K` command palette, `Ctrl+Shift+L` theme, `Ctrl+Shift+D` demo, `Esc` close overlays

---

## 📊 Data Sources & Runtime Dataset

All data is **embedded inline in `data.py`** — no external file reads required. The data was extracted from the My Farm Advisor runtime pipeline.

### Farm
- **Name**: Maryland Final Project Farm
- **Grower**: md-grower
- **Location**: Caroline County, MD (FIPS 24011)

### Fields (10)
Field boundaries from **OpenStreetMap / Overpass API**.
Geometries, acreage, centroids, elevation (min/max), slope, soil type, drainage, pH, organic matter, CEC, 2025 crop, full-year NDVI timeseries, and stress index.

### Weather (2021–2025)
Monthly aggregates from **NASA POWER S3 Zarr**:
- Average, max, min temperature (°C)
- Rainfall (mm)
- Solar radiation (W/m²)
- Humidity (%)
- Heat stress days (count)

### Additional Sources
- **DEM**: USGS 3DEP 1-meter (TNM)
- **Soils**: NRCS SSURGO (Ingleside, Hambrook, Fallsington series)
- **CDL**: USDA NASS Cropland Data Layer (Soybeans, Corn, Winter Wheat, Grass/Pasture)

### Where to Find Data in Code
- `data.py:FIELDS` — List of 10 field dictionaries
- `data.py:WEATHER_MONTHLY` — List of 60 monthly records
- `data.py:get_field_by_id()` — Field lookup helper
- `data.py:get_weather_by_year()` — Year filter helper
- `data.py:get_total_acres()` / `get_avg_stress()` / `get_high_risk_count()` / `get_well_drained_count()` / `get_avg_ndvi()` — Aggregate helpers

---

## 👤 Author

**Stephon Green** — Agricultural Data Analytics | Geospatial Intelligence

---

## 📜 License

Apache-2.0

---

## 🔗 Links

- **GitHub Repository**: https://github.com/S-G1/green-ag-intelligence
- **Dashboard Info**: See `DASHBOARD.md` for supplementary documentation
- **Supplementary Documentation**: See `DASHBOARD.md` for project overview, dataset description, dashboard explanation, analytical interpretation, and AI usage documentation.
- **Pull Request**: All changes committed directly to `main`. See commit history: `git log --oneline`
- **Hosted Dashboard**: Deploy via Render blueprint (`render.yaml`) — see Quick Start above
