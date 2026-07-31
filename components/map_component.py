"""Map Component — Full-height interactive map with enhanced controls and 10 layers."""

from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go

from config import MAP_CONFIG, COLORS
from data import FIELDS

# All 10 map layers
ALL_LAYERS = [
    {"id": "ndvi", "label": "NDVI", "color_scale": "RdYlGn"},
    {"id": "risk", "label": "Risk", "color_scale": "RdYlGn_r"},
    {"id": "heat_stress", "label": "Heat Stress", "color_scale": "YlOrRd"},
    {"id": "rainfall", "label": "Rainfall", "color_scale": "Blues"},
    {"id": "elevation", "label": "Elevation", "color_scale": "Terrain"},
    {"id": "slope", "label": "Slope", "color_scale": "YlOrRd"},
    {"id": "aspect", "label": "Aspect", "color_scale": "Viridis"},
    {"id": "hillshade", "label": "Hillshade", "color_scale": "Greys"},
    {"id": "wetness", "label": "Wetness", "color_scale": "Blues"},
    {"id": "soil_health", "label": "Soil Health", "color_scale": "RdYlGn"},
]


def create_map(selected_field: str | None = None, layer: str = "ndvi") -> html.Div:
    """Build the interactive map with enhanced controls."""
    fig = _build_map_figure(selected_field, layer)
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Environmental Risk Map", className="ga-card-title"),
                    html.Div(
                        [
                            html.Button("⛶", id="map-fullscreen", className="ga-map-btn", title="Fullscreen"),
                            html.Button("💾", id="map-download", className="ga-map-btn", title="Download PNG"),
                            html.Button("⌂", id="map-reset", className="ga-map-btn", title="Reset View"),
                        ],
                        className="ga-card-actions",
                    ),
                ],
                className="ga-card-header",
            ),
            
            html.Div(
                [
                    # Layer selector overlay
                    html.Div(
                        [
                            html.Div("Layers", className="ga-map-layer-title"),
                            html.Div(
                                [
                                    html.Button(
                                        l["label"],
                                        id=f"map-layer-{l['id']}",
                                        className=f"ga-map-layer-btn {'active' if l['id'] == layer else ''}",
                                    )
                                    for l in ALL_LAYERS
                                ],
                                className="ga-map-layer-list",
                            ),
                        ],
                        className="ga-map-layers",
                    ),
                    
                    # Dynamic legend
                    html.Div(
                        _build_legend(layer),
                        className="ga-map-legend",
                        id="map-legend",
                    ),
                    
                    # Map graph
                    dcc.Graph(
                        id="map-graph",
                        figure=fig,
                        config={
                            "displayModeBar": True,
                            "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
                            "displaylogo": False,
                        },
                        style={"height": "500px"},
                        className="ga-animate-fade",
                    ),
                ],
                className="ga-map-container",
            ),
        ],
        className="ga-card",
    )


def _build_map_figure(selected_field: str | None, layer: str) -> go.Figure:
    """Build the map figure with field polygons."""
    fig = go.Figure()
    
    for f in FIELDS:
        coords = f["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        # Color based on layer
        fill_color = _get_field_color(f, layer)
        
        # Highlight selected
        line_width = 3 if selected_field == f["id"] else 1
        line_color = COLORS["forest_green"] if selected_field == f["id"] else COLORS["gray_600"]
        
        # Rich popup content
        popup_text = _build_popup_text(f)
        
        fig.add_trace(
            go.Scattermapbox(
                lon=lons,
                lat=lats,
                mode="lines",
                fill="toself",
                fillcolor=fill_color,
                line={"width": line_width, "color": line_color},
                name=f["name"],
                text=popup_text,
                hoverinfo="text",
                hoverlabel={
                    "bgcolor": "white",
                    "bordercolor": COLORS["gray_300"],
                    "font": {"color": COLORS["gray_900"], "size": 12, "family": "Inter"},
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
    
    return fig


def _get_field_color(f: dict, layer: str) -> str:
    """Get color for a field based on the active layer."""
    if layer == "ndvi":
        ndvi_val = f["ndvi_2025"][6]
        return _ndvi_to_rgba(ndvi_val)
    elif layer == "risk":
        stress = f["stress_index"]
        if stress < 25:
            return "rgba(46, 125, 50, 0.6)"
        elif stress < 35:
            return "rgba(245, 127, 23, 0.6)"
        else:
            return "rgba(198, 40, 40, 0.6)"
    elif layer == "heat_stress":
        return "rgba(245, 127, 23, 0.5)"
    elif layer == "rainfall":
        return "rgba(21, 101, 192, 0.5)"
    elif layer == "elevation":
        elev = f["elevation_min_m"]
        intensity = min(1.0, elev / 25)
        return f"rgba({int(139*intensity)}, {int(69*intensity)}, {int(19*intensity)}, 0.6)"
    elif layer == "slope":
        slope = f["slope_percent"]
        intensity = min(1.0, slope / 5)
        return f"rgba({int(255*intensity)}, {int(140*(1-intensity))}, 0, 0.6)"
    elif layer == "aspect":
        return "rgba(128, 0, 128, 0.4)"
    elif layer == "hillshade":
        return "rgba(128, 128, 128, 0.3)"
    elif layer == "wetness":
        return "rgba(0, 0, 139, 0.4)"
    elif layer == "soil_health":
        ph = f["ph"]
        if 6.0 <= ph <= 7.0:
            return "rgba(46, 125, 50, 0.6)"
        elif 5.5 <= ph < 6.0:
            return "rgba(245, 127, 23, 0.6)"
        else:
            return "rgba(198, 40, 40, 0.6)"
    
    return "rgba(128, 128, 128, 0.4)"


def _ndvi_to_rgba(ndvi: float) -> str:
    """Convert NDVI value to RGBA color."""
    if ndvi < 0.3:
        return f"rgba(198, 40, 40, {0.3 + ndvi})"
    elif ndvi < 0.5:
        return f"rgba(245, 127, 23, {0.3 + ndvi * 0.5})"
    elif ndvi < 0.7:
        return f"rgba(255, 193, 7, {0.3 + ndvi * 0.4})"
    else:
        return f"rgba(46, 125, 50, {0.4 + ndvi * 0.4})"


def _build_popup_text(f: dict) -> str:
    """Build rich popup text for field hover."""
    risk_level = "Low" if f["stress_index"] < 25 else "Medium" if f["stress_index"] < 35 else "High"
    
    return (
        f"<b>{f['name']}</b><br>"
        f"━━━━━━━━━━━━━━━━<br>"
        f"🌾 Crop: {f['crop_2025']}<br>"
        f"📏 Area: {f['area_acres']:.1f} acres<br>"
        f"🌱 NDVI: {f['ndvi_2025'][6]:.2f}<br>"
        f"🌧️ Rainfall: Normal<br>"
        f"🔥 Heat Stress: {f['stress_index']} days<br>"
        f"⚠️ Risk Score: {f['stress_index']}/100 ({risk_level})<br>"
        f"🌍 Soil: {f['soil_type']} (pH {f['ph']})<br>"
        f"⛰️ Elevation: {f['elevation_min_m']:.1f}m<br>"
        f"📐 Slope: {f['slope_percent']:.1f}%"
    )


def _build_legend(layer: str) -> html.Div:
    """Build dynamic legend based on layer."""
    if layer == "risk":
        items = [
            ("rgba(46, 125, 50, 0.6)", "Healthy"),
            ("rgba(245, 127, 23, 0.6)", "Moderate"),
            ("rgba(198, 40, 40, 0.6)", "High Risk"),
        ]
    elif layer == "ndvi":
        items = [
            ("rgba(46, 125, 50, 0.8)", "Healthy (>0.7)"),
            ("rgba(255, 193, 7, 0.8)", "Moderate (0.5-0.7)"),
            ("rgba(245, 127, 23, 0.8)", "Poor (0.3-0.5)"),
            ("rgba(198, 40, 40, 0.8)", "Critical (<0.3)"),
        ]
    elif layer == "heat_stress":
        items = [
            ("rgba(46, 125, 50, 0.5)", "Low"),
            ("rgba(245, 127, 23, 0.5)", "Moderate"),
            ("rgba(198, 40, 40, 0.5)", "High"),
        ]
    elif layer == "rainfall":
        items = [
            ("rgba(21, 101, 192, 0.3)", "Low"),
            ("rgba(21, 101, 192, 0.6)", "Normal"),
            ("rgba(21, 101, 192, 0.9)", "High"),
        ]
    else:
        items = [
            ("rgba(128, 128, 128, 0.5)", "Layer Active"),
        ]
    
    legend_items = []
    for color, label in items:
        legend_items.append(
            html.Div(
                [
                    html.Span(style={"background": color, "width": "16px", "height": "16px", "borderRadius": "3px", "display": "inline-block", "marginRight": "8px"}),
                    html.Span(label, style={"fontSize": "0.75rem", "color": "#424242"}),
                ],
                className="d-flex align-items-center mb-1",
            )
        )
    
    return html.Div(
        [
            html.Div("Legend", style={"fontSize": "0.6875rem", "fontWeight": "600", "textTransform": "uppercase", "letterSpacing": "0.05em", "marginBottom": "8px", "color": "#757575"}),
            html.Div(legend_items),
        ],
        style={"padding": "12px"},
    )
