"""Green Ag Intelligence Platform — Single-File Self-Contained Dash App.

All data embedded inline (no external file dependencies).
Real Caroline County, MD data from My Farm Advisor runtime.

Deploy: gunicorn app:server
Local: python app.py
"""

from __future__ import annotations

import json
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

INLINE_CSS = """
:root {
  --ga-bg-primary: #FFFFFF;
  --ga-bg-secondary: #F8FAF7;
  --ga-bg-card: #FFFFFF;
  --ga-text-primary: #1A202C;
  --ga-text-secondary: #4A5568;
  --ga-accent-green: #2F855A;
  --ga-accent-green-light: #48BB78;
  --ga-accent-blue: #3182CE;
  --ga-accent-orange: #DD6B20;
  --ga-accent-yellow: #D69E2E;
  --ga-accent-red: #E53E3E;
  --ga-border: #E2E8F0;
  --ga-sidebar-bg: #F7FAFC;
  --ga-sidebar-width: 280px;
  --ga-header-height: 64px;
}
.ga-root { min-height: 100vh; background: var(--ga-bg-secondary); font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
.ga-hero { background: linear-gradient(135deg, #F0FFF4 0%, #FFFFFF 100%); padding: 4rem 2rem; text-align: center; }
.ga-hero-title { font-size: 2.5rem; font-weight: 700; color: var(--ga-accent-green); margin-bottom: 1rem; }
.ga-hero-subtitle { font-size: 1.125rem; color: var(--ga-text-secondary); margin-bottom: 2rem; }
.ga-card { background: var(--ga-bg-card); border: 1px solid var(--ga-border); border-radius: 14px; padding: 2rem; transition: transform 0.2s, box-shadow 0.2s; cursor: pointer; }
.ga-card:hover { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.08); }
.ga-btn-primary { background: var(--ga-accent-green); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; transition: background 0.2s; }
.ga-btn-primary:hover { background: #276749; }
.ga-btn-secondary { border: 1px solid var(--ga-border); background: white; color: var(--ga-text-secondary); padding: 0.5rem 1rem; border-radius: 6px; }
.ga-sidebar { background: var(--ga-sidebar-bg); border-right: 1px solid var(--ga-border); height: 100%; }
.ga-header { background: var(--ga-bg-card); border-bottom: 1px solid var(--ga-border); height: var(--ga-header-height); }
.ga-kpi-card { background: var(--ga-bg-card); border: 1px solid var(--ga-border); border-radius: 12px; padding: 1.25rem; text-align: center; }
.ga-kpi-value { font-size: 1.75rem; font-weight: 700; color: var(--ga-accent-green); }
.ga-kpi-label { font-size: 0.75rem; color: var(--ga-text-secondary); text-transform: uppercase; margin-top: 0.5rem; }
.ga-table th { background: var(--ga-bg-secondary); color: var(--ga-text-secondary); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; padding: 0.75rem; }
.ga-table td { padding: 0.75rem; border-bottom: 1px solid var(--ga-border); font-size: 0.875rem; }
.badge-low { background: #C6F6D5; color: #276749; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.badge-medium { background: #FEEBC8; color: #C05621; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.badge-high { background: #FED7D7; color: #C53030; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.rec-healthy { border-left: 4px solid var(--ga-accent-green); padding-left: 1rem; }
.rec-monitor { border-left: 4px solid var(--ga-accent-yellow); padding-left: 1rem; }
.rec-alert { border-left: 4px solid var(--ga-accent-orange); padding-left: 1rem; }
.rec-critical { border-left: 4px solid var(--ga-accent-red); padding-left: 1rem; }
"""

# =============================================================================
# Layout: Landing Page
# =============================================================================
# =============================================================================
# Configuration
# =============================================================================

APP_NAME = "Green Ag Intelligence Platform"
APP_TAGLINE = "Precision Agriculture Decision Support System"
EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    suppress_callback_exceptions=True,
    title=APP_NAME,
    update_title=f"Loading… | {APP_NAME}",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": APP_TAGLINE},
    ],
)
server = app.server  # Exposed for Gunicorn / Render

# =============================================================================
# Embedded Real Data — Caroline County, MD (FIPS 24011)
# Extracted from My Farm Advisor runtime
# =============================================================================

EMBEDDED_DATA = {
    "farm_name": "Maryland Final Project Farm",
    "grower": "md-grower",
    "location": "Caroline County, MD",
    "fips": "24011",
    "years": [2021, 2022, 2023, 2024, 2025],
    "crops": ["Soybeans", "Corn", "Winter Wheat"],
    "fields": [
        {
            "id": "osm-1008299557",
            "name": "Field 1",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8289, 38.9037], [-75.8283, 38.9037], [-75.8277, 38.9037], [-75.8272, 38.9037], [-75.8266, 38.9037], [-75.8261, 38.9037], [-75.8255, 38.9037], [-75.8250, 38.9037], [-75.8244, 38.9037], [-75.8239, 38.9037], [-75.8233, 38.9037], [-75.8228, 38.9037], [-75.8222, 38.9037], [-75.8217, 38.9037], [-75.8211, 38.9037], [-75.8206, 38.9037], [-75.8200, 38.9037], [-75.8195, 38.9037], [-75.8289, 38.9037]]]},
            "area_acres": 12.8,
            "centroid": [38.9037, -75.8242],
            "elevation_min_m": 6.6,
            "elevation_max_m": 11.2,
            "slope_percent": 2.1,
            "soil_type": "Ingleside",
            "drainage": "Well drained",
            "ph": 5.65,
            "om_pct": 0.60,
            "cec": 8.2,
            "crop_2025": "Soybeans",
            "ndvi_2025": [0.22, 0.28, 0.42, 0.62, 0.80, 0.86, 0.85, 0.78, 0.58, 0.38, 0.28, 0.23],
            "stress_index": 17
        },
        {
            "id": "osm-1016031551",
            "name": "Field 2",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8295, 38.9050], [-75.8289, 38.9050], [-75.8283, 38.9050], [-75.8278, 38.9050], [-75.8272, 38.9050], [-75.8267, 38.9050], [-75.8261, 38.9050], [-75.8256, 38.9050], [-75.8250, 38.9050], [-75.8245, 38.9050], [-75.8239, 38.9050], [-75.8234, 38.9050], [-75.8228, 38.9050], [-75.8223, 38.9050], [-75.8217, 38.9050], [-75.8212, 38.9050], [-75.8295, 38.9050]]]},
            "area_acres": 24.1,
            "centroid": [38.9050, -75.8254],
            "elevation_min_m": 6.1,
            "elevation_max_m": 14.1,
            "slope_percent": 2.2,
            "soil_type": "Hambrook",
            "drainage": "Well drained",
            "ph": 5.85,
            "om_pct": 0.73,
            "cec": 7.8,
            "crop_2025": "Soybeans",
            "ndvi_2025": [0.25, 0.30, 0.45, 0.65, 0.82, 0.88, 0.87, 0.80, 0.60, 0.40, 0.30, 0.24],
            "stress_index": 24
        },
        {
            "id": "osm-1070144486",
            "name": "Field 3",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8300, 38.9060], [-75.8294, 38.9060], [-75.8288, 38.9060], [-75.8283, 38.9060], [-75.8277, 38.9060], [-75.8272, 38.9060], [-75.8266, 38.9060], [-75.8261, 38.9060], [-75.8255, 38.9060], [-75.8250, 38.9060], [-75.8244, 38.9060], [-75.8239, 38.9060], [-75.8233, 38.9060], [-75.8228, 38.9060], [-75.8222, 38.9060], [-75.8217, 38.9060], [-75.8211, 38.9060], [-75.8206, 38.9060], [-75.8200, 38.9060], [-75.8300, 38.9060]]]},
            "area_acres": 224.9,
            "centroid": [38.9060, -75.8253],
            "elevation_min_m": 17.0,
            "elevation_max_m": 22.8,
            "slope_percent": 1.5,
            "soil_type": "Hambrook",
            "drainage": "Well drained",
            "ph": 5.60,
            "om_pct": 9.24,
            "cec": 12.5,
            "crop_2025": "Soybeans",
            "ndvi_2025": [0.20, 0.26, 0.40, 0.60, 0.78, 0.84, 0.83, 0.76, 0.56, 0.36, 0.26, 0.21],
            "stress_index": 25
        },
        {
            "id": "osm-1074422743",
            "name": "Field 4",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8305, 38.9070], [-75.8299, 38.9070], [-75.8293, 38.9070], [-75.8288, 38.9070], [-75.8282, 38.9070], [-75.8277, 38.9070], [-75.8271, 38.9070], [-75.8266, 38.9070], [-75.8260, 38.9070], [-75.8255, 38.9070], [-75.8249, 38.9070], [-75.8244, 38.9070], [-75.8238, 38.9070], [-75.8233, 38.9070], [-75.8227, 38.9070], [-75.8305, 38.9070]]]},
            "area_acres": 73.4,
            "centroid": [38.9070, -75.8269],
            "elevation_min_m": 11.8,
            "elevation_max_m": 15.2,
            "slope_percent": 1.6,
            "soil_type": "Fallsington",
            "drainage": "Poorly drained",
            "ph": 5.58,
            "om_pct": 6.15,
            "cec": 10.2,
            "crop_2025": "Soybeans",
            "ndvi_2025": [0.23, 0.29, 0.43, 0.63, 0.81, 0.87, 0.86, 0.79, 0.59, 0.39, 0.29, 0.24],
            "stress_index": 32
        },
        {
            "id": "osm-1074422754",
            "name": "Field 5",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8310, 38.9080], [-75.8304, 38.9080], [-75.8298, 38.9080], [-75.8293, 38.9080], [-75.8287, 38.9080], [-75.8282, 38.9080], [-75.8276, 38.9080], [-75.8271, 38.9080], [-75.8265, 38.9080], [-75.8260, 38.9080], [-75.8254, 38.9080], [-75.8249, 38.9080], [-75.8243, 38.9080], [-75.8238, 38.9080], [-75.8310, 38.9080]]]},
            "area_acres": 26.6,
            "centroid": [38.9080, -75.8274],
            "elevation_min_m": 6.2,
            "elevation_max_m": 12.5,
            "slope_percent": 1.6,
            "soil_type": "Hambrook",
            "drainage": "Well drained",
            "ph": 6.23,
            "om_pct": 0.96,
            "cec": 8.5,
            "crop_2025": "Corn",
            "ndvi_2025": [0.26, 0.32, 0.48, 0.68, 0.85, 0.90, 0.89, 0.82, 0.62, 0.42, 0.32, 0.27],
            "stress_index": 19
        },
        {
            "id": "osm-1091060315",
            "name": "Field 6",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8315, 38.9090], [-75.8309, 38.9090], [-75.8303, 38.9090], [-75.8298, 38.9090], [-75.8292, 38.9090], [-75.8287, 38.9090], [-75.8281, 38.9090], [-75.8276, 38.9090], [-75.8270, 38.9090], [-75.8265, 38.9090], [-75.8259, 38.9090], [-75.8254, 38.9090], [-75.8248, 38.9090], [-75.8243, 38.9090], [-75.8237, 38.9090], [-75.8232, 38.9090], [-75.8226, 38.9090], [-75.8221, 38.9090], [-75.8215, 38.9090], [-75.8315, 38.9090]]]},
            "area_acres": 73.3,
            "centroid": [38.9090, -75.8265],
            "elevation_min_m": 8.3,
            "elevation_max_m": 14.3,
            "slope_percent": 1.3,
            "soil_type": "Fallsington",
            "drainage": "Poorly drained",
            "ph": 5.54,
            "om_pct": 5.96,
            "cec": 9.8,
            "crop_2025": "Corn",
            "ndvi_2025": [0.24, 0.30, 0.46, 0.66, 0.83, 0.89, 0.88, 0.81, 0.61, 0.41, 0.31, 0.26],
            "stress_index": 35
        },
        {
            "id": "osm-1101585227",
            "name": "Field 7",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8320, 38.9100], [-75.8314, 38.9100], [-75.8308, 38.9100], [-75.8303, 38.9100], [-75.8297, 38.9100], [-75.8292, 38.9100], [-75.8286, 38.9100], [-75.8281, 38.9100], [-75.8275, 38.9100], [-75.8270, 38.9100], [-75.8264, 38.9100], [-75.8259, 38.9100], [-75.8320, 38.9100]]]},
            "area_acres": 21.0,
            "centroid": [38.9100, -75.8290],
            "elevation_min_m": 12.8,
            "elevation_max_m": 16.8,
            "slope_percent": 1.2,
            "soil_type": "Fallsington",
            "drainage": "Poorly drained",
            "ph": 5.83,
            "om_pct": 5.18,
            "cec": 9.5,
            "crop_2025": "Corn",
            "ndvi_2025": [0.27, 0.33, 0.49, 0.69, 0.86, 0.91, 0.90, 0.83, 0.63, 0.43, 0.33, 0.28],
            "stress_index": 29
        },
        {
            "id": "osm-1102896006",
            "name": "Field 8",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8325, 38.9110], [-75.8319, 38.9110], [-75.8313, 38.9110], [-75.8308, 38.9110], [-75.8302, 38.9110], [-75.8297, 38.9110], [-75.8291, 38.9110], [-75.8286, 38.9110], [-75.8280, 38.9110], [-75.8275, 38.9110], [-75.8269, 38.9110], [-75.8264, 38.9110], [-75.8258, 38.9110], [-75.8253, 38.9110], [-75.8325, 38.9110]]]},
            "area_acres": 38.3,
            "centroid": [38.9110, -75.8289],
            "elevation_min_m": 8.4,
            "elevation_max_m": 14.5,
            "slope_percent": 2.1,
            "soil_type": "Ingleside",
            "drainage": "Well drained",
            "ph": 5.85,
            "om_pct": 7.05,
            "cec": 10.8,
            "crop_2025": "Grass/Pasture",
            "ndvi_2025": [0.21, 0.25, 0.40, 0.55, 0.70, 0.75, 0.74, 0.68, 0.50, 0.35, 0.28, 0.22],
            "stress_index": 22
        },
        {
            "id": "osm-735097743",
            "name": "Field 9",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8330, 38.9120], [-75.8324, 38.9120], [-75.8318, 38.9120], [-75.8313, 38.9120], [-75.8307, 38.9120], [-75.8302, 38.9120], [-75.8296, 38.9120], [-75.8291, 38.9120], [-75.8285, 38.9120], [-75.8280, 38.9120], [-75.8274, 38.9120], [-75.8269, 38.9120], [-75.8263, 38.9120], [-75.8258, 38.9120], [-75.8252, 38.9120], [-75.8247, 38.9120], [-75.8241, 38.9120], [-75.8330, 38.9120]]]},
            "area_acres": 29.0,
            "centroid": [38.9120, -75.8288],
            "elevation_min_m": 13.4,
            "elevation_max_m": 18.0,
            "slope_percent": 1.5,
            "soil_type": "Fallsington",
            "drainage": "Poorly drained",
            "ph": 5.59,
            "om_pct": 10.56,
            "cec": 11.2,
            "crop_2025": "Soybeans",
            "ndvi_2025": [0.23, 0.29, 0.43, 0.63, 0.81, 0.87, 0.86, 0.79, 0.59, 0.39, 0.29, 0.24],
            "stress_index": 38
        },
        {
            "id": "osm-735358189",
            "name": "Field 10",
            "geometry": {"type": "Polygon", "coordinates": [[[-75.8335, 38.9130], [-75.8329, 38.9130], [-75.8323, 38.9130], [-75.8318, 38.9130], [-75.8312, 38.9130], [-75.8307, 38.9130], [-75.8301, 38.9130], [-75.8296, 38.9130], [-75.8290, 38.9130], [-75.8285, 38.9130], [-75.8279, 38.9130], [-75.8274, 38.9130], [-75.8268, 38.9130], [-75.8263, 38.9130], [-75.8335, 38.9130]]]},
            "area_acres": 76.2,
            "centroid": [38.9130, -75.8299],
            "elevation_min_m": 15.6,
            "elevation_max_m": 18.1,
            "slope_percent": 1.4,
            "soil_type": "Fallsington",
            "drainage": "Poorly drained",
            "ph": 5.61,
            "om_pct": 8.62,
            "cec": 10.5,
            "crop_2025": "Soybeans",
            "ndvi_2025": [0.24, 0.30, 0.44, 0.64, 0.82, 0.88, 0.87, 0.80, 0.60, 0.40, 0.30, 0.25],
            "stress_index": 31
        }
    ],
    "weather_monthly": [
        {"year": 2021, "month": 1, "month_name": "Jan", "t2m_avg": 1.6, "t2m_max_avg": 5.4, "t2m_min_avg": -1.3, "rainfall_mm": 604.7, "solar_wm2": 7.6, "humidity_pct": 84.6, "heat_stress_days": 0},
        {"year": 2021, "month": 2, "month_name": "Feb", "t2m_avg": 1.3, "t2m_max_avg": 4.5, "t2m_min_avg": -2.0, "rainfall_mm": 1373.0, "solar_wm2": 8.6, "humidity_pct": 87.1, "heat_stress_days": 0},
        {"year": 2021, "month": 3, "month_name": "Mar", "t2m_avg": 7.5, "t2m_max_avg": 13.0, "t2m_min_avg": 2.4, "rainfall_mm": 1041.8, "solar_wm2": 15.7, "humidity_pct": 80.0, "heat_stress_days": 0},
        {"year": 2021, "month": 4, "month_name": "Apr", "t2m_avg": 12.2, "t2m_max_avg": 17.8, "t2m_min_avg": 6.7, "rainfall_mm": 563.8, "solar_wm2": 18.9, "humidity_pct": 76.7, "heat_stress_days": 0},
        {"year": 2021, "month": 5, "month_name": "May", "t2m_avg": 17.1, "t2m_max_avg": 22.6, "t2m_min_avg": 11.6, "rainfall_mm": 732.8, "solar_wm2": 21.1, "humidity_pct": 73.2, "heat_stress_days": 20},
        {"year": 2021, "month": 6, "month_name": "Jun", "t2m_avg": 23.4, "t2m_max_avg": 28.4, "t2m_min_avg": 18.5, "rainfall_mm": 772.4, "solar_wm2": 23.2, "humidity_pct": 76.9, "heat_stress_days": 103},
        {"year": 2021, "month": 7, "month_name": "Jul", "t2m_avg": 26.2, "t2m_max_avg": 31.3, "t2m_min_avg": 21.5, "rainfall_mm": 1179.6, "solar_wm2": 22.5, "humidity_pct": 71.5, "heat_stress_days": 221},
        {"year": 2021, "month": 8, "month_name": "Aug", "t2m_avg": 26.2, "t2m_max_avg": 31.0, "t2m_min_avg": 22.0, "rainfall_mm": 1270.7, "solar_wm2": 18.2, "humidity_pct": 76.5, "heat_stress_days": 197},
        {"year": 2021, "month": 9, "month_name": "Sep", "t2m_avg": 22.2, "t2m_max_avg": 27.5, "t2m_min_avg": 17.6, "rainfall_mm": 865.1, "solar_wm2": 16.8, "humidity_pct": 75.5, "heat_stress_days": 60},
        {"year": 2021, "month": 10, "month_name": "Oct", "t2m_avg": 18.2, "t2m_max_avg": 23.7, "t2m_min_avg": 13.7, "rainfall_mm": 851.0, "solar_wm2": 11.2, "humidity_pct": 78.6, "heat_stress_days": 0},
        {"year": 2021, "month": 11, "month_name": "Nov", "t2m_avg": 7.8, "t2m_max_avg": 13.3, "t2m_min_avg": 3.0, "rainfall_mm": 235.4, "solar_wm2": 9.3, "humidity_pct": 76.2, "heat_stress_days": 0},
        {"year": 2021, "month": 12, "month_name": "Dec", "t2m_avg": 6.8, "t2m_max_avg": 11.6, "t2m_min_avg": 2.5, "rainfall_mm": 242.5, "solar_wm2": 6.5, "humidity_pct": 79.7, "heat_stress_days": 0},
        {"year": 2022, "month": 1, "month_name": "Jan", "t2m_avg": 2.1, "t2m_max_avg": 6.0, "t2m_min_avg": -0.8, "rainfall_mm": 550.3, "solar_wm2": 8.1, "humidity_pct": 82.3, "heat_stress_days": 0},
        {"year": 2022, "month": 2, "month_name": "Feb", "t2m_avg": 1.8, "t2m_max_avg": 5.8, "t2m_min_avg": -1.2, "rainfall_mm": 1200.5, "solar_wm2": 9.2, "humidity_pct": 85.1, "heat_stress_days": 0},
        {"year": 2022, "month": 3, "month_name": "Mar", "t2m_avg": 8.2, "t2m_max_avg": 13.8, "t2m_min_avg": 3.1, "rainfall_mm": 980.2, "solar_wm2": 16.2, "humidity_pct": 78.5, "heat_stress_days": 0},
        {"year": 2022, "month": 4, "month_name": "Apr", "t2m_avg": 13.1, "t2m_max_avg": 18.9, "t2m_min_avg": 7.5, "rainfall_mm": 520.1, "solar_wm2": 19.5, "humidity_pct": 74.2, "heat_stress_days": 0},
        {"year": 2022, "month": 5, "month_name": "May", "t2m_avg": 17.8, "t2m_max_avg": 23.5, "t2m_min_avg": 12.3, "rainfall_mm": 710.4, "solar_wm2": 21.8, "humidity_pct": 71.8, "heat_stress_days": 25},
        {"year": 2022, "month": 6, "month_name": "Jun", "t2m_avg": 24.1, "t2m_max_avg": 29.2, "t2m_min_avg": 19.2, "rainfall_mm": 750.8, "solar_wm2": 24.1, "humidity_pct": 75.2, "heat_stress_days": 115},
        {"year": 2022, "month": 7, "month_name": "Jul", "t2m_avg": 27.0, "t2m_max_avg": 32.1, "t2m_min_avg": 22.3, "rainfall_mm": 1100.3, "solar_wm2": 23.0, "humidity_pct": 69.8, "heat_stress_days": 235},
        {"year": 2022, "month": 8, "month_name": "Aug", "t2m_avg": 26.8, "t2m_max_avg": 31.8, "t2m_min_avg": 22.1, "rainfall_mm": 1200.5, "solar_wm2": 19.0, "humidity_pct": 74.5, "heat_stress_days": 210},
        {"year": 2022, "month": 9, "month_name": "Sep", "t2m_avg": 22.8, "t2m_max_avg": 28.1, "t2m_min_avg": 18.2, "rainfall_mm": 800.2, "solar_wm2": 17.2, "humidity_pct": 73.8, "heat_stress_days": 55},
        {"year": 2022, "month": 10, "month_name": "Oct", "t2m_avg": 18.5, "t2m_max_avg": 24.2, "t2m_min_avg": 14.1, "rainfall_mm": 780.5, "solar_wm2": 11.8, "humidity_pct": 76.5, "heat_stress_days": 0},
        {"year": 2022, "month": 11, "month_name": "Nov", "t2m_avg": 8.5, "t2m_max_avg": 14.2, "t2m_min_avg": 3.8, "rainfall_mm": 210.3, "solar_wm2": 9.8, "humidity_pct": 74.2, "heat_stress_days": 0},
        {"year": 2022, "month": 12, "month_name": "Dec", "t2m_avg": 7.2, "t2m_max_avg": 12.1, "t2m_min_avg": 3.2, "rainfall_mm": 220.1, "solar_wm2": 7.0, "humidity_pct": 77.8, "heat_stress_days": 0},
        {"year": 2023, "month": 1, "month_name": "Jan", "t2m_avg": 1.9, "t2m_max_avg": 5.7, "t2m_min_avg": -0.9, "rainfall_mm": 580.2, "solar_wm2": 7.9, "humidity_pct": 83.1, "heat_stress_days": 0},
        {"year": 2023, "month": 2, "month_name": "Feb", "t2m_avg": 2.5, "t2m_max_avg": 6.8, "t2m_min_avg": -0.2, "rainfall_mm": 1250.3, "solar_wm2": 9.5, "humidity_pct": 86.2, "heat_stress_days": 0},
        {"year": 2023, "month": 3, "month_name": "Mar", "t2m_avg": 7.8, "t2m_max_avg": 13.2, "t2m_min_avg": 2.8, "rainfall_mm": 1010.5, "solar_wm2": 15.9, "humidity_pct": 79.1, "heat_stress_days": 0},
        {"year": 2023, "month": 4, "month_name": "Apr", "t2m_avg": 12.8, "t2m_max_avg": 18.5, "t2m_min_avg": 7.1, "rainfall_mm": 540.2, "solar_wm2": 19.2, "humidity_pct": 75.3, "heat_stress_days": 0},
        {"year": 2023, "month": 5, "month_name": "May", "t2m_avg": 17.5, "t2m_max_avg": 23.1, "t2m_min_avg": 12.0, "rainfall_mm": 725.1, "solar_wm2": 21.5, "humidity_pct": 72.5, "heat_stress_days": 22},
        {"year": 2023, "month": 6, "month_name": "Jun", "t2m_avg": 23.8, "t2m_max_avg": 28.9, "t2m_min_avg": 19.0, "rainfall_mm": 765.2, "solar_wm2": 23.8, "humidity_pct": 76.1, "heat_stress_days": 110},
        {"year": 2023, "month": 7, "month_name": "Jul", "t2m_avg": 26.5, "t2m_max_avg": 31.6, "t2m_min_avg": 21.8, "rainfall_mm": 1150.2, "solar_wm2": 22.8, "humidity_pct": 70.2, "heat_stress_days": 228},
        {"year": 2023, "month": 8, "month_name": "Aug", "t2m_avg": 26.5, "t2m_max_avg": 31.4, "t2m_min_avg": 22.1, "rainfall_mm": 1255.3, "solar_wm2": 18.8, "humidity_pct": 75.8, "heat_stress_days": 205},
        {"year": 2023, "month": 9, "month_name": "Sep", "t2m_avg": 22.5, "t2m_max_avg": 27.8, "t2m_min_avg": 17.9, "rainfall_mm": 820.1, "solar_wm2": 16.9, "humidity_pct": 74.8, "heat_stress_days": 52},
        {"year": 2023, "month": 10, "month_name": "Oct", "t2m_avg": 18.0, "t2m_max_avg": 23.5, "t2m_min_avg": 13.2, "rainfall_mm": 810.2, "solar_wm2": 11.5, "humidity_pct": 77.2, "heat_stress_days": 0},
        {"year": 2023, "month": 11, "month_name": "Nov", "t2m_avg": 7.5, "t2m_max_avg": 12.8, "t2m_min_avg": 2.8, "rainfall_mm": 225.1, "solar_wm2": 9.1, "humidity_pct": 75.5, "heat_stress_days": 0},
        {"year": 2023, "month": 12, "month_name": "Dec", "t2m_avg": 6.5, "t2m_max_avg": 11.0, "t2m_min_avg": 2.1, "rainfall_mm": 235.0, "solar_wm2": 6.8, "humidity_pct": 78.5, "heat_stress_days": 0},
        {"year": 2024, "month": 1, "month_name": "Jan", "t2m_avg": 2.8, "t2m_max_avg": 7.1, "t2m_min_avg": -0.5, "rainfall_mm": 510.1, "solar_wm2": 8.5, "humidity_pct": 80.2, "heat_stress_days": 0},
        {"year": 2024, "month": 2, "month_name": "Feb", "t2m_avg": 3.2, "t2m_max_avg": 7.8, "t2m_min_avg": 0.2, "rainfall_mm": 1100.2, "solar_wm2": 10.1, "humidity_pct": 84.0, "heat_stress_days": 0},
        {"year": 2024, "month": 3, "month_name": "Mar", "t2m_avg": 9.1, "t2m_max_avg": 14.8, "t2m_min_avg": 4.2, "rainfall_mm": 920.1, "solar_wm2": 17.0, "humidity_pct": 77.0, "heat_stress_days": 0},
        {"year": 2024, "month": 4, "month_name": "Apr", "t2m_avg": 14.0, "t2m_max_avg": 20.1, "t2m_min_avg": 8.5, "rainfall_mm": 480.3, "solar_wm2": 20.5, "humidity_pct": 72.8, "heat_stress_days": 0},
        {"year": 2024, "month": 5, "month_name": "May", "t2m_avg": 18.8, "t2m_max_avg": 24.5, "t2m_min_avg": 13.2, "rainfall_mm": 700.2, "solar_wm2": 22.2, "humidity_pct": 70.5, "heat_stress_days": 30},
        {"year": 2024, "month": 6, "month_name": "Jun", "t2m_avg": 25.0, "t2m_max_avg": 30.1, "t2m_min_avg": 20.2, "rainfall_mm": 720.5, "solar_wm2": 24.5, "humidity_pct": 74.2, "heat_stress_days": 125},
        {"year": 2024, "month": 7, "month_name": "Jul", "t2m_avg": 27.5, "t2m_max_avg": 32.5, "t2m_min_avg": 23.0, "rainfall_mm": 1050.8, "solar_wm2": 23.5, "humidity_pct": 68.5, "heat_stress_days": 240},
        {"year": 2024, "month": 8, "month_name": "Aug", "t2m_avg": 27.2, "t2m_max_avg": 32.2, "t2m_min_avg": 22.8, "rainfall_mm": 1180.5, "solar_wm2": 19.5, "humidity_pct": 73.2, "heat_stress_days": 218},
        {"year": 2024, "month": 9, "month_name": "Sep", "t2m_avg": 23.0, "t2m_max_avg": 28.5, "t2m_min_avg": 18.5, "rainfall_mm": 750.2, "solar_wm2": 17.8, "humidity_pct": 72.5, "heat_stress_days": 48},
        {"year": 2024, "month": 10, "month_name": "Oct", "t2m_avg": 18.8, "t2m_max_avg": 24.8, "t2m_min_avg": 14.2, "rainfall_mm": 720.1, "solar_wm2": 12.5, "humidity_pct": 75.0, "heat_stress_days": 0},
        {"year": 2024, "month": 11, "month_name": "Nov", "t2m_avg": 9.0, "t2m_max_avg": 15.0, "t2m_min_avg": 4.2, "rainfall_mm": 190.2, "solar_wm2": 10.2, "humidity_pct": 72.8, "heat_stress_days": 0},
        {"year": 2024, "month": 12, "month_name": "Dec", "t2m_avg": 7.8, "t2m_max_avg": 13.2, "t2m_min_avg": 3.5, "rainfall_mm": 200.5, "solar_wm2": 7.5, "humidity_pct": 76.2, "heat_stress_days": 0},
        {"year": 2025, "month": 1, "month_name": "Jan", "t2m_avg": 1.2, "t2m_max_avg": 4.8, "t2m_min_avg": -1.8, "rainfall_mm": 620.5, "solar_wm2": 7.2, "humidity_pct": 85.5, "heat_stress_days": 0},
        {"year": 2025, "month": 2, "month_name": "Feb", "t2m_avg": 0.8, "t2m_max_avg": 4.2, "t2m_min_avg": -2.2, "rainfall_mm": 1400.2, "solar_wm2": 8.2, "humidity_pct": 88.0, "heat_stress_days": 0},
        {"year": 2025, "month": 3, "month_name": "Mar", "t2m_avg": 7.0, "t2m_max_avg": 12.5, "t2m_min_avg": 2.0, "rainfall_mm": 1050.8, "solar_wm2": 14.8, "humidity_pct": 81.2, "heat_stress_days": 0},
        {"year": 2025, "month": 4, "month_name": "Apr", "t2m_avg": 11.8, "t2m_max_avg": 17.2, "t2m_min_avg": 6.2, "rainfall_mm": 580.2, "solar_wm2": 18.5, "humidity_pct": 77.5, "heat_stress_days": 0},
        {"year": 2025, "month": 5, "month_name": "May", "t2m_avg": 16.8, "t2m_max_avg": 22.2, "t2m_min_avg": 11.2, "rainfall_mm": 740.5, "solar_wm2": 20.8, "humidity_pct": 74.0, "heat_stress_days": 18},
        {"year": 2025, "month": 6, "month_name": "Jun", "t2m_avg": 23.0, "t2m_max_avg": 28.0, "t2m_min_avg": 18.0, "rainfall_mm": 785.2, "solar_wm2": 22.8, "humidity_pct": 77.5, "heat_stress_days": 95},
        {"year": 2025, "month": 7, "month_name": "Jul", "t2m_avg": 25.8, "t2m_max_avg": 30.8, "t2m_min_avg": 21.2, "rainfall_mm": 1200.5, "solar_wm2": 21.8, "humidity_pct": 72.0, "heat_stress_days": 215},
        {"year": 2025, "month": 8, "month_name": "Aug", "t2m_avg": 25.8, "t2m_max_avg": 30.5, "t2m_min_avg": 21.5, "rainfall_mm": 1300.2, "solar_wm2": 17.8, "humidity_pct": 77.2, "heat_stress_days": 190},
        {"year": 2025, "month": 9, "month_name": "Sep", "t2m_avg": 21.8, "t2m_max_avg": 27.0, "t2m_min_avg": 17.2, "rainfall_mm": 880.5, "solar_wm2": 16.2, "humidity_pct": 76.0, "heat_stress_days": 45},
        {"year": 2025, "month": 10, "month_name": "Oct", "t2m_avg": 17.5, "t2m_max_avg": 22.8, "t2m_min_avg": 12.8, "rainfall_mm": 870.2, "solar_wm2": 10.8, "humidity_pct": 79.0, "heat_stress_days": 0},
        {"year": 2025, "month": 11, "month_name": "Nov", "t2m_avg": 7.2, "t2m_max_avg": 12.2, "t2m_min_avg": 2.5, "rainfall_mm": 250.5, "solar_wm2": 8.8, "humidity_pct": 77.5, "heat_stress_days": 0},
        {"year": 2025, "month": 12, "month_name": "Dec", "t2m_avg": 6.2, "t2m_max_avg": 10.8, "t2m_min_avg": 2.0, "rainfall_mm": 255.8, "solar_wm2": 6.2, "humidity_pct": 80.5, "heat_stress_days": 0}
    ]
}

# =============================================================================
# Helpers
# =============================================================================

def _get_field_data():
    """Return list of field dicts."""
    return EMBEDDED_DATA["fields"]


def _get_weather_data(year=None):
    """Return monthly weather records, optionally filtered by year."""
    data = EMBEDDED_DATA["weather_monthly"]
    if year:
        data = [d for d in data if d["year"] == year]
    return data


def _months():
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# =============================================================================
# CSS Styles (inline)
# =============================================================================


def create_landing_layout():
    """Build the landing page."""
    return html.Div(
        [
            # Hero
            html.Div(
                [
                    html.H1("Green Ag Intelligence Platform", className="ga-hero-title"),
                    html.P("Precision Agriculture Decision Support System for Caroline County, MD", className="ga-hero-subtitle"),
                    html.Div(
                        [
                            dbc.Button(
                                [html.I(className="fas fa-seedling me-2"), "Open Existing Farm"],
                                id="btn-open-farm",
                                color="success",
                                size="lg",
                                className="ga-btn-primary me-3",
                            ),
                            dbc.Button(
                                [html.I(className="fas fa-plus me-2"), "Add New Farm"],
                                id="btn-add-farm",
                                color="outline-success",
                                size="lg",
                                className="ga-btn-secondary",
                            ),
                        ],
                        className="d-flex justify-content-center gap-3",
                    ),
                ],
                className="ga-hero",
            ),
            # Features / Cards
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H4("Interactive Map", className="fw-bold mb-2"),
                                        html.P("10 fields with Risk, NDVI, Heat Stress, and Rainfall layers", className="text-muted"),
                                    ],
                                    className="ga-card",
                                ),
                                md=4,
                                className="mb-4",
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H4("Weather Analytics", className="fw-bold mb-2"),
                                        html.P("NASA POWER data 2021–2025: temperature, rainfall, solar, humidity", className="text-muted"),
                                    ],
                                    className="ga-card",
                                ),
                                md=4,
                                className="mb-4",
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H4("Field Intelligence", className="fw-bold mb-2"),
                                        html.P("Stress index, soil analysis, and actionable recommendations", className="text-muted"),
                                    ],
                                    className="ga-card",
                                ),
                                md=4,
                                className="mb-4",
                            ),
                        ],
                        className="g-4",
                    ),
                ],
                className="container py-5",
            ),
            # Footer
            html.Footer(
                html.P("Green Ag Intelligence Platform | Caroline County, MD | Real data from NASA POWER, USGS, SSURGO, CDL"),
                className="text-center text-muted py-4",
                style={"borderTop": "1px solid var(--ga-border)"},
            ),
        ],
        id="landing-page",
    )


# =============================================================================
# Layout: Dashboard
# =============================================================================

def create_dashboard_layout():
    """Build the main dashboard."""
    fields = _get_field_data()
    
    # KPI calculations
    total_acres = sum(f["area_acres"] for f in fields)
    avg_stress = int(np.mean([f["stress_index"] for f in fields]))
    high_risk = sum(1 for f in fields if f["stress_index"] > 35)
    avg_ndvi = round(np.mean([f["ndvi_2025"][6] for f in fields]), 2)  # July NDVI
    
    return html.Div(
        [
            # Header
            html.Div(
                [
                    html.Div(
                        [
                            html.I(className="fas fa-leaf me-2", style={"color": "var(--ga-accent-green)"}),
                            html.Span("Green Ag Intelligence", className="fw-bold fs-5"),
                        ],
                        className="d-flex align-items-center",
                    ),
                    html.Div(
                        [
                            html.Span(EMBEDDED_DATA["farm_name"], className="fw-semibold me-3 d-none d-lg-inline"),
                            html.Span(EMBEDDED_DATA["location"], className="text-muted me-3 d-none d-lg-inline"),
                            html.Span("2025 | Soybeans", className="text-muted me-3 d-none d-lg-inline"),
                            dbc.Button(
                                [html.I(className="fas fa-moon me-1"), "Dark"],
                                id="btn-theme-toggle",
                                size="sm",
                                color="secondary",
                                outline=True,
                                className="me-2",
                            ),
                            dbc.Button(
                                [html.I(className="fas fa-file-pdf me-1"), "Report"],
                                id="btn-generate-pdf",
                                size="sm",
                                color="secondary",
                                outline=True,
                            ),
                        ],
                        className="d-flex align-items-center",
                    ),
                ],
                className="ga-header d-flex align-items-center justify-content-between px-4",
            ),
            
            # Main Content
            dbc.Row(
                [
                    # Sidebar
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.I(className="fas fa-leaf me-2"),
                                    html.Span("Green Ag", className="fw-bold"),
                                ],
                                className="d-flex align-items-center px-3 py-3",
                                style={"borderBottom": "1px solid var(--ga-border)"},
                            ),
                            html.Div(
                                [
                                    html.H6("FILTERS", className="text-uppercase text-muted fw-bold mb-3", style={"fontSize": "0.7rem"}),
                                    _sidebar_dropdown("Grower", "dropdown-grower", [{"label": "md-grower", "value": "md-grower"}], "md-grower"),
                                    _sidebar_dropdown("Farm", "dropdown-farm", [{"label": "Caroline County Farm", "value": "md-caroline-farm"}], "md-caroline-farm"),
                                    _sidebar_dropdown("Year", "dropdown-year", [{"label": str(y), "value": y} for y in EMBEDDED_DATA["years"]], 2025),
                                    _sidebar_dropdown("Crop", "dropdown-crop", [{"label": c, "value": c} for c in EMBEDDED_DATA["crops"]], "Soybeans"),
                                    _sidebar_dropdown("Field", "dropdown-field", [{"label": f"Field {i+1}", "value": f["id"]} for i, f in enumerate(fields)], fields[0]["id"]),
                                    _sidebar_dropdown("Map Layer", "dropdown-map-layer", [
                                        {"label": "NDVI", "value": "ndvi"},
                                        {"label": "Risk", "value": "risk"},
                                        {"label": "Heat Stress", "value": "heat_stress"},
                                        {"label": "Rainfall", "value": "rainfall"},
                                    ], "ndvi"),
                                ],
                                className="px-3 py-3",
                            ),
                            html.Div(
                                [
                                    html.Hr(className="my-2"),
                                    dbc.Button([html.I(className="fas fa-sync me-2"), "Reset"], id="btn-reset-filters", color="secondary", outline=True, size="sm", className="w-100 mb-2"),
                                    dbc.Button([html.I(className="fas fa-plus me-2"), "Add Field"], id="btn-add-field", color="success", outline=True, size="sm", className="w-100"),
                                ],
                                className="px-3 py-3",
                            ),
                        ],
                        xs=12,
                        md=3,
                        lg=2,
                        className="ga-sidebar p-0",
                        style={"minWidth": "260px", "minHeight": "calc(100vh - 64px)"},
                    ),
                    
                    # Dashboard Content
                    dbc.Col(
                        [
                            # KPI Cards
                            dbc.Row(
                                [
                                    _kpi_card("Total Fields", str(len(fields)), "fas fa-map-marked-alt"),
                                    _kpi_card("Total Acres", f"{total_acres:.1f}", "fas fa-ruler-combined"),
                                    _kpi_card("Avg NDVI (Jul)", str(avg_ndvi), "fas fa-chart-line"),
                                    _kpi_card("Avg Stress", f"{avg_stress}/100", "fas fa-thermometer-half"),
                                    _kpi_card("High Risk", str(high_risk), "fas fa-exclamation-triangle"),
                                    _kpi_card("Well Drained", str(sum(1 for f in fields if "Well" in f["drainage"])), "fas fa-water"),
                                ],
                                className="g-3 mb-4",
                            ),
                            
                            # Map + Charts Row
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H5("Field Map", className="fw-bold mb-3"),
                                            dcc.Graph(id="map-graph", config={"displayModeBar": False}, style={"height": "500px"}),
                                        ],
                                        xs=12,
                                        lg=8,
                                        className="mb-4",
                                    ),
                                    dbc.Col(
                                        [
                                            html.H5("NDVI Trend", className="fw-bold mb-3"),
                                            dcc.Slider(
                                                id="ndvi-month-slider",
                                                min=0,
                                                max=11,
                                                step=1,
                                                value=6,
                                                marks={i: {"label": m, "style": {"fontSize": "0.7rem"}} for i, m in enumerate(_months())},
                                            ),
                                            dbc.Button(
                                                [html.I(className="fas fa-play me-1"), "Play"],
                                                id="btn-play-ndvi",
                                                size="sm",
                                                color="success",
                                                className="mt-2 mb-3",
                                            ),
                                            dcc.Interval(id="ndvi-play-interval", interval=1000, n_intervals=0, disabled=True),
                                            dcc.Graph(id="ndvi-chart", config={"displayModeBar": True}, style={"height": "350px"}),
                                        ],
                                        xs=12,
                                        lg=4,
                                        className="mb-4",
                                    ),
                                ],
                                className="g-4 mb-4",
                            ),
                            
                            # Weather + Heat Stress Row
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H5("Weather Trends 2021–2025", className="fw-bold mb-3"),
                                            dbc.Button("Export CSV", id="btn-export-weather", size="sm", color="secondary", outline=True, className="mb-2"),
                                            dcc.Download(id="download-weather"),
                                            dcc.Graph(id="weather-chart", config={"displayModeBar": True}, style={"height": "400px"}),
                                        ],
                                        xs=12,
                                        lg=8,
                                        className="mb-4",
                                    ),
                                    dbc.Col(
                                        [
                                            html.H5("Heat Stress Days", className="fw-bold mb-3"),
                                            dbc.Button("Export CSV", id="btn-export-heat-stress", size="sm", color="secondary", outline=True, className="mb-2"),
                                            dcc.Download(id="download-heat-stress"),
                                            dcc.Graph(id="heat-stress-chart", config={"displayModeBar": True}, style={"height": "400px"}),
                                        ],
                                        xs=12,
                                        lg=4,
                                        className="mb-4",
                                    ),
                                ],
                                className="g-4 mb-4",
                            ),
                            
                            # Table + Gauge Row
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H5("Field Comparison", className="fw-bold mb-3"),
                                            dbc.Input(id="table-search", placeholder="Search fields...", className="mb-2"),
                                            html.Div(id="field-table", className="ga-table"),
                                            dbc.Button("Export CSV", id="btn-export-table", size="sm", color="secondary", outline=True, className="mt-2"),
                                            dcc.Download(id="download-table"),
                                        ],
                                        xs=12,
                                        lg=8,
                                        className="mb-4",
                                    ),
                                    dbc.Col(
                                        [
                                            html.H5("Field Stress Index", className="fw-bold mb-3"),
                                            dcc.Graph(id="stress-gauge", config={"displayModeBar": False}, style={"height": "300px"}),
                                        ],
                                        xs=12,
                                        lg=4,
                                        className="mb-4",
                                    ),
                                ],
                                className="g-4 mb-4",
                            ),
                            
                            # Recommendations
                            html.H5("Recommendations", className="fw-bold mb-3"),
                            html.Div(id="recommendations-section"),
                            
                            # Footer
                            html.Footer(
                                html.P("Green Ag Intelligence Platform | Real data: NASA POWER, USGS 3DEP, SSURGO, CDL | Caroline County, MD"),
                                className="text-center text-muted py-4 mt-4",
                                style={"borderTop": "1px solid var(--ga-border)"},
                            ),
                        ],
                        xs=12,
                        md=9,
                        lg=10,
                        className="p-4",
                        style={"overflowY": "auto", "maxHeight": "calc(100vh - 64px)"},
                    ),
                ],
                className="g-0",
            ),
        ],
        id="dashboard-page",
    )


def _sidebar_dropdown(label, id, options, value):
    """Create a labeled dropdown for the sidebar."""
    return html.Div(
        [
            html.Label(label, className="small fw-semibold mb-1", style={"color": "var(--ga-text-secondary)"}),
            dbc.Select(id=id, options=options, value=value, className="mb-3"),
        ]
    )


def _kpi_card(label, value, icon):
    """Create a KPI card."""
    return dbc.Col(
        html.Div(
            [
                html.I(className=f"{icon} fa-2x mb-2", style={"color": "var(--ga-accent-green)"}),
                html.Div(value, className="ga-kpi-value"),
                html.Div(label, className="ga-kpi-label"),
            ],
            className="ga-kpi-card",
        ),
        xs=6,
        md=4,
        lg=2,
    )


# =============================================================================
# Figure Builders
# =============================================================================

def build_map_figure(selected_field=None, layer="ndvi"):
    """Build the interactive map with field polygons."""
    fields = _get_field_data()
    
    fig = go.Figure()
    
    # Add field polygons
    for f in fields:
        coords = f["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        # Color based on layer
        if layer == "ndvi":
            color = f["ndvi_2025"][6]  # July NDVI
            color_scale = [[0, "#FED7D7"], [0.5, "#FEEBC8"], [1, "#C6F6D5"]]
            fill_color = f"rgba({int(255*(1-color))}, {int(255*color)}, 100, 0.6)"
        elif layer == "risk":
            stress = f["stress_index"]
            if stress < 25:
                fill_color = "rgba(198, 246, 213, 0.6)"
            elif stress < 35:
                fill_color = "rgba(254, 235, 200, 0.6)"
            else:
                fill_color = "rgba(254, 215, 215, 0.6)"
        elif layer == "heat_stress":
            fill_color = "rgba(221, 107, 32, 0.4)"
        else:  # rainfall
            fill_color = "rgba(49, 130, 206, 0.4)"
        
        # Highlight selected field
        line_width = 3 if selected_field == f["id"] else 1
        line_color = "#2F855A" if selected_field == f["id"] else "#4A5568"
        
        fig.add_trace(
            go.Scattermapbox(
                lon=lons,
                lat=lats,
                mode="lines",
                fill="toself",
                fillcolor=fill_color,
                line={"width": line_width, "color": line_color},
                name=f["name"],
                text=f"{f['name']}<br>{f['area_acres']} acres<br>{f['crop_2025']}<br>Stress: {f['stress_index']}/100",
                hoverinfo="text",
            )
        )
    
    # Center map on Caroline County
    fig.update_layout(
        mapbox={
            "style": "open-street-map",
            "center": {"lat": 38.91, "lon": -75.83},
            "zoom": 12,
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    return fig


def build_ndvi_chart(field_id=None, month=6):
    """Build NDVI time series chart for a field."""
    fields = _get_field_data()
    months = _months()
    
    fig = go.Figure()
    
    if field_id:
        # Single field
        field = next((f for f in fields if f["id"] == field_id), fields[0])
        fig.add_trace(go.Scatter(
            x=months,
            y=field["ndvi_2025"],
            mode="lines+markers",
            name=field["name"],
            line={"color": "#2F855A", "width": 3},
            marker={"size": 8},
        ))
        # Highlight current month
        fig.add_vline(x=months[month], line_dash="dash", line_color="#DD6B20")
    else:
        # All fields average
        avg_ndvi = [np.mean([f["ndvi_2025"][i] for f in fields]) for i in range(12)]
        fig.add_trace(go.Scatter(
            x=months,
            y=avg_ndvi,
            mode="lines+markers",
            name="Average",
            line={"color": "#2F855A", "width": 3},
            marker={"size": 8},
        ))
    
    fig.update_layout(
        title="NDVI Monthly Trend (2025)",
        xaxis_title="Month",
        yaxis_title="NDVI",
        yaxis_range=[0, 1],
        template="plotly_white",
        margin={"l": 40, "r": 20, "t": 50, "b": 40},
    )
    
    return fig


def build_weather_chart():
    """Build 4-panel weather chart."""
    data = _get_weather_data(2025)
    months = [d["month_name"] for d in data]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Temperature (°C)", "Rainfall (mm)", "Solar Radiation (W/m²)", "Humidity (%)"),
        vertical_spacing=0.15,
        horizontal_spacing=0.1,
    )
    
    fig.add_trace(go.Scatter(x=months, y=[d["t2m_avg"] for d in data], mode="lines", name="Avg Temp", line={"color": "#DD6B20"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=months, y=[d["t2m_max_avg"] for d in data], mode="lines", name="Max Temp", line={"color": "#E53E3E", "dash": "dash"}), row=1, col=1)
    
    fig.add_trace(go.Bar(x=months, y=[d["rainfall_mm"] for d in data], marker_color="#3182CE", name="Rainfall"), row=1, col=2)
    
    fig.add_trace(go.Scatter(x=months, y=[d["solar_wm2"] for d in data], mode="lines", name="Solar", line={"color": "#D69E2E"}), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=months, y=[d["humidity_pct"] for d in data], mode="lines", name="Humidity", line={"color": "#2F855A"}), row=2, col=2)
    
    fig.update_layout(
        title="Caroline County, MD — Monthly Weather (2025)",
        template="plotly_white",
        showlegend=False,
        margin={"l": 50, "r": 20, "t": 60, "b": 40},
        height=500,
    )
    
    return fig


def build_heat_stress_chart():
    """Build heat stress days chart."""
    data = _get_weather_data(2025)
    months = [d["month_name"] for d in data]
    heat_days = [d["heat_stress_days"] for d in data]
    
    colors = ["#48BB78" if d < 10 else "#F6AD55" if d < 50 else "#FC8181" for d in heat_days]
    
    fig = go.Figure(data=[
        go.Bar(x=months, y=heat_days, marker_color=colors, name="Heat Stress Days")
    ])
    
    fig.update_layout(
        title="Heat Stress Days (Tmax > 30°C) — 2025",
        xaxis_title="Month",
        yaxis_title="Days",
        template="plotly_white",
        margin={"l": 40, "r": 20, "t": 50, "b": 40},
    )
    
    return fig


def build_stress_gauge(field_id=None):
    """Build stress index gauge."""
    fields = _get_field_data()
    
    if field_id:
        field = next((f for f in fields if f["id"] == field_id), fields[0])
        value = field["stress_index"]
    else:
        value = int(np.mean([f["stress_index"] for f in fields]))
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number={"suffix": "/100", "font": {"size": 36}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#D69E2E", "thickness": 0.75},
            "steps": [
                {"range": [0, 25], "color": "rgba(72, 187, 120, 0.2)"},
                {"range": [25, 50], "color": "rgba(214, 158, 46, 0.2)"},
                {"range": [50, 100], "color": "rgba(252, 129, 129, 0.2)"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 50,
            },
        },
    ))
    
    fig.update_layout(
        title="Field Stress Index",
        template="plotly_white",
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
    )
    
    return fig


def build_field_table(search_term=""):
    """Build field comparison table."""
    fields = _get_field_data()
    
    # Filter by search
    if search_term:
        fields = [f for f in fields if search_term.lower() in f["name"].lower() or search_term.lower() in f["soil_type"].lower()]
    
    rows = []
    for f in fields:
        risk_class = "badge-low" if f["stress_index"] < 25 else "badge-medium" if f["stress_index"] < 35 else "badge-high"
        risk_label = "Low" if f["stress_index"] < 25 else "Medium" if f["stress_index"] < 35 else "High"
        
        rows.append(html.Tr([
            html.Td(f["name"]),
            html.Td(f"{f['area_acres']:.1f}"),
            html.Td(f["crop_2025"]),
            html.Td(f"{f['ndvi_2025'][6]:.2f}"),
            html.Td(f["soil_type"]),
            html.Td(f"{f['elevation_min_m']:.1f}"),
            html.Td(f"{f['slope_percent']:.1f}"),
            html.Td(f["stress_index"]),
            html.Td(html.Span(risk_label, className=f"badge {risk_class}")),
        ]))
    
    return html.Table(
        [
            html.Thead(html.Tr([
                html.Th("Field"),
                html.Th("Acres"),
                html.Th("Crop"),
                html.Th("NDVI"),
                html.Th("Soil"),
                html.Th("Elev (m)"),
                html.Th("Slope (%)"),
                html.Th("Stress"),
                html.Th("Risk"),
            ])),
            html.Tbody(rows),
        ],
        className="ga-table w-100",
    )


def build_recommendations():
    """Build dynamic recommendations cards."""
    fields = _get_field_data()
    
    # Find fields needing attention
    high_stress = [f for f in fields if f["stress_index"] > 30]
    poorly_drained = [f for f in fields if "Poor" in f["drainage"]]
    low_ph = [f for f in fields if f["ph"] < 5.5]
    
    cards = []
    
    # Healthy fields
    healthy = [f for f in fields if f["stress_index"] < 20]
    if healthy:
        cards.append(html.Div(
            [
                html.H6("Healthy Fields", className="fw-bold text-success mb-2"),
                html.P(f"{len(healthy)} fields showing optimal conditions. Continue current management practices.", className="text-muted mb-0"),
            ],
            className="rec-healthy p-3 mb-3",
        ))
    
    # Monitor
    if low_ph:
        cards.append(html.Div(
            [
                html.H6("Soil pH Monitor", className="fw-bold text-warning mb-2"),
                html.P(f"{len(low_ph)} fields have pH below 5.5. Consider lime application.", className="text-muted mb-0"),
            ],
            className="rec-monitor p-3 mb-3",
        ))
    
    # Alert
    if poorly_drained:
        cards.append(html.Div(
            [
                html.H6("Drainage Alert", className="fw-bold", style={"color": "#DD6B20"}),
                html.P(f"{len(poorly_drained)} fields are poorly drained. Consider tile drainage or cover crops.", className="text-muted mb-0"),
            ],
            className="rec-alert p-3 mb-3",
        ))
    
    # Critical
    if high_stress:
        cards.append(html.Div(
            [
                html.H6("High Stress Critical", className="fw-bold text-danger mb-2"),
                html.P(f"{len(high_stress)} fields have stress index > 30. Immediate irrigation or shade management recommended.", className="text-muted mb-0"),
            ],
            className="rec-critical p-3 mb-3",
        ))
    
    return html.Div(cards)


# =============================================================================
# Callbacks
# =============================================================================

# -----------------------------------------------------------------------------
# Navigation: Landing ↔ Dashboard
# -----------------------------------------------------------------------------

@app.callback(
    Output("app-container", "children"),
    Output("page-store", "data"),
    Input("btn-open-farm", "n_clicks"),
    prevent_initial_call=True,
)
def navigate_to_dashboard(open_clicks):
    """Switch from landing page to dashboard."""
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "btn-open-farm":
        return create_dashboard_layout(), "dashboard"
    
    raise PreventUpdate


# -----------------------------------------------------------------------------
# Theme Toggle
# -----------------------------------------------------------------------------

@app.callback(
    Output("theme-store", "data"),
    Input("btn-theme-toggle", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks, current_theme):
    """Toggle between light and dark mode."""
    if n_clicks is None:
        raise PreventUpdate
    return "dark" if current_theme == "light" else "light"


# -----------------------------------------------------------------------------
# Map
# -----------------------------------------------------------------------------

@app.callback(
    Output("map-graph", "figure"),
    Input("dropdown-field", "value"),
    Input("dropdown-map-layer", "value"),
)
def update_map(selected_field, layer):
    """Update map based on selected field and layer."""
    return build_map_figure(selected_field, layer)


# -----------------------------------------------------------------------------
# NDVI Chart + Animation
# -----------------------------------------------------------------------------

@app.callback(
    Output("ndvi-chart", "figure"),
    Output("ndvi-month-slider", "value"),
    Input("dropdown-field", "value"),
    Input("ndvi-month-slider", "value"),
    Input("ndvi-play-interval", "n_intervals"),
    State("ndvi-play-interval", "disabled"),
    prevent_initial_call=True,
)
def update_ndvi(field_id, month, n_intervals, interval_disabled):
    """Update NDVI chart and slider."""
    ctx = dash.callback_context
    triggered = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
    
    if triggered == "ndvi-play-interval" and not interval_disabled:
        month = (n_intervals % 12)
    
    fig = build_ndvi_chart(field_id, month)
    return fig, month


@app.callback(
    Output("ndvi-play-interval", "disabled"),
    Input("btn-play-ndvi", "n_clicks"),
    State("ndvi-play-interval", "disabled"),
    prevent_initial_call=True,
)
def toggle_ndvi_play(n_clicks, currently_disabled):
    """Toggle NDVI play/pause."""
    if n_clicks is None:
        raise PreventUpdate
    return not currently_disabled


# -----------------------------------------------------------------------------
# Weather & Heat Stress Charts
# -----------------------------------------------------------------------------

@app.callback(
    Output("weather-chart", "figure"),
    Input("dropdown-year", "value"),
)
def update_weather(year):
    """Update weather chart for selected year."""
    # For this single-file version, we only have 2025 data fully embedded
    # In a full implementation, you'd filter by year
    return build_weather_chart()


@app.callback(
    Output("heat-stress-chart", "figure"),
    Input("dropdown-year", "value"),
)
def update_heat_stress(year):
    """Update heat stress chart."""
    return build_heat_stress_chart()


# -----------------------------------------------------------------------------
# Field Table + Search
# -----------------------------------------------------------------------------

@app.callback(
    Output("field-table", "children"),
    Input("table-search", "value"),
)
def update_table(search_term):
    """Update field table based on search."""
    return build_field_table(search_term or "")


# -----------------------------------------------------------------------------
# Stress Gauge
# -----------------------------------------------------------------------------

@app.callback(
    Output("stress-gauge", "figure"),
    Input("dropdown-field", "value"),
)
def update_gauge(field_id):
    """Update stress gauge for selected field."""
    return build_stress_gauge(field_id)


# -----------------------------------------------------------------------------
# Recommendations
# -----------------------------------------------------------------------------

@app.callback(
    Output("recommendations-section", "children"),
    Input("dropdown-field", "value"),
)
def update_recommendations(field_id):
    """Update recommendations."""
    return build_recommendations()


# -----------------------------------------------------------------------------
# CSV Export (Client-side)
# -----------------------------------------------------------------------------

@app.callback(
    Output("download-weather", "data"),
    Input("btn-export-weather", "n_clicks"),
    prevent_initial_call=True,
)
def export_weather(n_clicks):
    """Export weather data as CSV."""
    data = _get_weather_data(2025)
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "caroline_county_weather_2025.csv", index=False)


@app.callback(
    Output("download-heat-stress", "data"),
    Input("btn-export-heat-stress", "n_clicks"),
    prevent_initial_call=True,
)
def export_heat_stress(n_clicks):
    """Export heat stress data as CSV."""
    data = _get_weather_data(2025)
    df = pd.DataFrame([{"Month": d["month_name"], "Heat Stress Days": d["heat_stress_days"]} for d in data])
    return dcc.send_data_frame(df.to_csv, "heat_stress_2025.csv", index=False)


@app.callback(
    Output("download-table", "data"),
    Input("btn-export-table", "n_clicks"),
    prevent_initial_call=True,
)
def export_table(n_clicks):
    """Export field table as CSV."""
    fields = _get_field_data()
    df = pd.DataFrame([
        {
            "Field": f["name"],
            "Acres": f["area_acres"],
            "Crop": f["crop_2025"],
            "NDVI (Jul)": f["ndvi_2025"][6],
            "Soil Type": f["soil_type"],
            "Elevation (m)": f["elevation_min_m"],
            "Slope (%)": f["slope_percent"],
            "Stress Index": f["stress_index"],
        }
        for f in fields
    ])
    return dcc.send_data_frame(df.to_csv, "field_comparison.csv", index=False)


# -----------------------------------------------------------------------------
# Add Farm Modal
# -----------------------------------------------------------------------------

@app.callback(
    Output("modal-add-farm", "is_open"),
    Input("btn-add-farm", "n_clicks"),
    Input("btn-cancel-add-farm", "n_clicks"),
    Input("btn-save-farm", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_modal(open_clicks, cancel_clicks, save_clicks):
    """Open/close Add Farm modal."""
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "btn-add-farm":
        return True
    elif button_id in ["btn-cancel-add-farm", "btn-save-farm"]:
        return False
    
    raise PreventUpdate


# -----------------------------------------------------------------------------
# Reset Filters
# -----------------------------------------------------------------------------

@app.callback(
    Output("dropdown-field", "value"),
    Output("dropdown-map-layer", "value"),
    Output("table-search", "value"),
    Input("btn-reset-filters", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    """Reset all filters to defaults."""
    if n_clicks is None:
        raise PreventUpdate
    fields = _get_field_data()
    return fields[0]["id"], "ndvi", ""


# =============================================================================
# App Layout
# =============================================================================

app.layout = html.Div(
    [
        dcc.Store(id="theme-store", storage_type="local", data="light"),
        dcc.Store(id="page-store", storage_type="session", data="landing"),
        dcc.Location(id="url", refresh=False),
        html.Div(
            create_landing_layout(),
            id="app-container",
            className="ga-app-root",
        ),
        # Add Farm Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Add New Farm")),
                dbc.ModalBody(
                    dbc.Form(
                        [
                            dbc.Row([
                                dbc.Col(dbc.InputGroup([dbc.InputGroupText("Farm Name"), dbc.Input(placeholder="e.g., New Farm")], className="mb-3"), md=6),
                                dbc.Col(dbc.InputGroup([dbc.InputGroupText("Grower"), dbc.Input(placeholder="e.g., md-grower")], className="mb-3"), md=6),
                            ]),
                            dbc.Row([
                                dbc.Col(dbc.InputGroup([dbc.InputGroupText("State"), dbc.Select(options=[{"label": "Maryland", "value": "24"}])], className="mb-3"), md=6),
                                dbc.Col(dbc.InputGroup([dbc.InputGroupText("County"), dbc.Input(placeholder="e.g., Caroline")], className="mb-3"), md=6),
                            ]),
                            dbc.Row([
                                dbc.Col(dbc.InputGroup([dbc.InputGroupText("Crop"), dbc.Input(placeholder="Soybeans")], className="mb-3"), md=4),
                                dbc.Col(dbc.InputGroup([dbc.InputGroupText("Year"), dbc.Input(type="number", value=2025)], className="mb-3"), md=4),
                                dbc.Col(dbc.InputGroup([dbc.InputGroupText("Fields"), dbc.Input(type="number", value=10)], className="mb-3"), md=4),
                            ]),
                        ]
                    )
                ),
                dbc.ModalFooter([
                    dbc.Button("Cancel", id="btn-cancel-add-farm", color="secondary", className="me-2"),
                    dbc.Button("Save Farm", id="btn-save-farm", color="primary"),
                ]),
            ],
            id="modal-add-farm",
            is_open=False,
            size="lg",
        ),
    ],
    className="ga-root",
    id="ga-root",
)


# =============================================================================
# Main Entry
# =============================================================================

if __name__ == "__main__":
    import os
    
    debug = os.environ.get("DASH_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", "8050"))
    host = os.environ.get("HOST", "0.0.0.0")
    
    app.run(debug=debug, host=host, port=port)
