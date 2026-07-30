#!/usr/bin/env python3
"""Generate Plotly Chart Studio JSON files from embedded data.

Usage:
    python generate_charts.py

Output:
    charts/chart_map.json
    charts/chart_ndvi.json
    charts/chart_weather.json
    charts/chart_heat_stress.json
    charts/chart_gauge.json
"""

from __future__ import annotations

import json
import numpy as np
from pathlib import Path

# Import the embedded data from app.py
import sys
sys.path.insert(0, str(Path(__file__).parent))
from app import EMBEDDED_DATA, _get_field_data, _get_weather_data, _months

import plotly.graph_objects as go
from plotly.subplots import make_subplots

OUTPUT_DIR = Path(__file__).parent / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_map_chart() -> dict:
    """Generate map figure with field boundaries colored by risk."""
    fields = _get_field_data()
    
    fig = go.Figure()
    
    for f in fields:
        coords = f["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        stress = f["stress_index"]
        if stress < 25:
            fill_color = "rgba(72, 187, 120, 0.6)"
        elif stress < 35:
            fill_color = "rgba(214, 158, 46, 0.6)"
        else:
            fill_color = "rgba(252, 129, 129, 0.6)"
        
        fig.add_trace(go.Scattermapbox(
            lon=lons,
            lat=lats,
            mode="lines",
            fill="toself",
            fillcolor=fill_color,
            line={"width": 1, "color": "#4A5568"},
            name=f["name"],
            text=f"{f['name']}<br>{f['area_acres']} acres<br>{f['crop_2025']}<br>Stress: {f['stress_index']}/100",
            hoverinfo="text",
        ))
    
    fig.update_layout(
        mapbox={"style": "open-street-map", "center": {"lat": 38.91, "lon": -75.83}, "zoom": 12},
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        showlegend=False,
        title="Caroline County, MD — Field Risk Map",
    )
    
    return fig.to_dict()


def generate_ndvi_chart() -> dict:
    """Generate NDVI time series chart."""
    fields = _get_field_data()
    months = _months()
    
    fig = go.Figure()
    
    # Add individual field lines
    colors = ["#2F855A", "#3182CE", "#DD6B20", "#805AD5", "#D53F8C"]
    for i, f in enumerate(fields[:5]):  # Top 5 fields for clarity
        fig.add_trace(go.Scatter(
            x=months,
            y=f["ndvi_2025"],
            mode="lines+markers",
            name=f["name"],
            line={"color": colors[i % len(colors)], "width": 2},
            marker={"size": 6},
        ))
    
    # Add average line
    avg_ndvi = [np.mean([f["ndvi_2025"][i] for f in fields]) for i in range(12)]
    fig.add_trace(go.Scatter(
        x=months,
        y=avg_ndvi,
        mode="lines+markers",
        name="Average",
        line={"color": "#1A202C", "width": 3, "dash": "dash"},
        marker={"size": 8},
    ))
    
    fig.update_layout(
        title="NDVI Monthly Trend (2025) — Caroline County Farm",
        xaxis_title="Month",
        yaxis_title="NDVI",
        yaxis_range=[0, 1],
        template="plotly_white",
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.3},
    )
    
    return fig.to_dict()


def generate_weather_chart() -> dict:
    """Generate 4-panel weather chart."""
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
        height=500,
    )
    
    return fig.to_dict()


def generate_heat_stress_chart() -> dict:
    """Generate heat stress days chart."""
    data = _get_weather_data(2025)
    months = [d["month_name"] for d in data]
    heat_days = [d["heat_stress_days"] for d in data]
    
    colors = ["#48BB78" if d < 10 else "#F6AD55" if d < 50 else "#FC8181" for d in heat_days]
    
    fig = go.Figure(data=[go.Bar(x=months, y=heat_days, marker_color=colors, name="Heat Stress Days")])
    
    fig.update_layout(
        title="Heat Stress Days (Tmax > 30°C) — Caroline County, MD 2025",
        xaxis_title="Month",
        yaxis_title="Days",
        template="plotly_white",
    )
    
    return fig.to_dict()


def generate_gauge_chart() -> dict:
    """Generate stress index gauge."""
    fields = _get_field_data()
    avg_stress = int(np.mean([f["stress_index"] for f in fields]))
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_stress,
        number={"suffix": "/100", "font": {"size": 48}},
        title={"text": "Field Stress Index<br><sub>Caroline County Farm</sub>"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#D69E2E", "thickness": 0.75},
            "steps": [
                {"range": [0, 25], "color": "rgba(72, 187, 120, 0.2)"},
                {"range": [25, 50], "color": "rgba(214, 158, 46, 0.2)"},
                {"range": [50, 100], "color": "rgba(252, 129, 129, 0.2)"},
            ],
            "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 50},
        },
    ))
    
    fig.update_layout(template="plotly_white", height=400)
    
    return fig.to_dict()


def main():
    """Generate all chart JSON files."""
    print("=" * 60)
    print("Generating Plotly Chart Studio JSON files...")
    print("=" * 60)
    
    charts = {
        "chart_map.json": generate_map_chart(),
        "chart_ndvi.json": generate_ndvi_chart(),
        "chart_weather.json": generate_weather_chart(),
        "chart_heat_stress.json": generate_heat_stress_chart(),
        "chart_gauge.json": generate_gauge_chart(),
    }
    
    for filename, chart_data in charts.items():
        filepath = OUTPUT_DIR / filename
        with open(filepath, "w") as f:
            json.dump(chart_data, f, indent=2)
        size = filepath.stat().st_size / 1024
        print(f"✓ {filename} ({size:.1f} KB)")
    
    print()
    print("=" * 60)
    print(f"All charts saved to: {OUTPUT_DIR}")
    print()
    print("Upload to Plotly Chart Studio:")
    print("  1. Visit https://chart-studio.plotly.com/create/")
    print("  2. Click 'Import' → 'Upload JSON'")
    print("  3. Select each .json file")
    print("=" * 60)


if __name__ == "__main__":
    main()
