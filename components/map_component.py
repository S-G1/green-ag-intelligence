"""Map Component — Full-height interactive map with field polygons."""

from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go

from config import MAP_CONFIG, COLORS
from data import FIELDS


def create_map(selected_field: str | None = None, layer: str = "ndvi") -> html.Div:
    """Build the interactive map with field polygons."""
    fig = go.Figure()
    
    # Add field polygons
    for f in FIELDS:
        coords = f["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        # Color based on layer
        if layer == "ndvi":
            ndvi_val = f["ndvi_2025"][6]  # July
            fill_color = _ndvi_to_color(ndvi_val)
        elif layer == "risk":
            stress = f["stress_index"]
            if stress < 25:
                fill_color = "rgba(46, 125, 50, 0.6)"
            elif stress < 35:
                fill_color = "rgba(245, 127, 23, 0.6)"
            else:
                fill_color = "rgba(198, 40, 40, 0.6)"
        elif layer == "heat_stress":
            fill_color = "rgba(245, 127, 23, 0.5)"
        else:  # rainfall
            fill_color = "rgba(21, 101, 192, 0.5)"
        
        # Highlight selected
        line_width = 3 if selected_field == f["id"] else 1
        line_color = COLORS["forest_green"] if selected_field == f["id"] else COLORS["gray_600"]
        
        fig.add_trace(
            go.Scattermapbox(
                lon=lons,
                lat=lats,
                mode="lines",
                fill="toself",
                fillcolor=fill_color,
                line={"width": line_width, "color": line_color},
                name=f["name"],
                text=f"<b>{f['name']}</b><br>{f['area_acres']} acres | {f['crop_2025']}<br>Stress: {f['stress_index']}/100<br>Soil: {f['soil_type']}",
                hoverinfo="text",
                hoverlabel={
                    "bgcolor": "white",
                    "bordercolor": COLORS["gray_300"],
                    "font": {"color": COLORS["gray_900"], "size": 12},
                },
            )
        )
    
    fig.update_layout(
        mapbox={
            "style": MAP_CONFIG["style"],
            "center": {"lat": MAP_CONFIG["center_lat"], "lon": MAP_CONFIG["center_lon"]},
            "zoom": MAP_CONFIG["default_zoom"],
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=500,
    )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Field Map", className="ga-card-title"),
                    html.Div(
                        [
                            html.Button(
                                "NDVI",
                                id="map-layer-ndvi",
                                className=f"ga-map-layer-btn {'active' if layer == 'ndvi' else ''}",
                            ),
                            html.Button(
                                "Risk",
                                id="map-layer-risk",
                                className=f"ga-map-layer-btn {'active' if layer == 'risk' else ''}",
                            ),
                            html.Button(
                                "Heat",
                                id="map-layer-heat",
                                className=f"ga-map-layer-btn {'active' if layer == 'heat_stress' else ''}",
                            ),
                            html.Button(
                                "Rain",
                                id="map-layer-rain",
                                className=f"ga-map-layer-btn {'active' if layer == 'rainfall' else ''}",
                            ),
                        ],
                        className="ga-map-controls",
                    ),
                ],
                className="ga-card-header",
            ),
            dcc.Graph(
                id="map-graph",
                figure=fig,
                config={"displayModeBar": False},
                style={"height": "500px"},
                className="ga-animate-fade",
            ),
        ],
        className="ga-card",
    )


def _ndvi_to_color(ndvi: float) -> str:
    """Convert NDVI value to RGBA color."""
    if ndvi < 0.3:
        return f"rgba(198, 40, 40, {0.3 + ndvi})"
    elif ndvi < 0.5:
        return f"rgba(245, 127, 23, {0.3 + ndvi * 0.5})"
    elif ndvi < 0.7:
        return f"rgba(255, 193, 7, {0.3 + ndvi * 0.4})"
    else:
        return f"rgba(46, 125, 50, {0.4 + ndvi * 0.4})"
