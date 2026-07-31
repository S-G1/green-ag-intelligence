"""Map Explorer page — Full-screen interactive map with layer controls and field sidebar."""

from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from data import FIELDS
from config import MAP_CONFIG, COLORS


def create_map_explorer_page() -> html.Div:
    """Build the Map Explorer page with full-width map and field sidebar."""
    
    # Field list sidebar
    field_items = []
    for f in FIELDS:
        field_items.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("📍", className="me-2"),
                            html.Span(f["name"], className="fw-medium"),
                        ],
                        className="d-flex align-items-center",
                    ),
                    html.Div(
                        [
                            html.Span(f"{f['area_acres']:.1f} ac", className="text-muted small me-2"),
                            html.Span(f["crop_2025"], className="badge bg-light text-dark small"),
                        ],
                        className="d-flex align-items-center mt-1",
                    ),
                ],
                className="map-sidebar-field p-2 mb-1 rounded",
                id={"type": "map-field-item", "index": f["id"]},
            )
        )
    
    # Layer selector
    layer_options = []
    for layer in MAP_CONFIG["layers"]:
        layer_options.append(
            html.Button(
                layer["label"],
                id=f"map-layer-btn-{layer['id']}",
                className="map-layer-btn me-2 mb-2",
            )
        )
    
    # Create the map figure
    fig = go.Figure()
    
    # Add field polygons
    for f in FIELDS:
        coords = f["geometry"]["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        fig.add_trace(go.Scattermapbox(
            lon=lons,
            lats=lats,
            mode="lines",
            fill="toself",
            fillcolor="rgba(76, 175, 80, 0.3)",
            line=dict(color=COLORS["forest_green"], width=2),
            name=f["name"],
            text=f"{f['name']}<br>{f['area_acres']:.1f} ac<br>NDVI: {f['ndvi_2025'][6]:.2f}",
            hoverinfo="text",
        ))
    
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=MAP_CONFIG["center_lat"], lon=MAP_CONFIG["center_lon"]),
            zoom=MAP_CONFIG["default_zoom"],
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        uirevision=True,
    )
    
    return html.Div(
        [
            dbc.Row(
                [
                    # Sidebar
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.Div("Map Layers", className="ga-card-title mb-2"),
                                    html.Div(layer_options, className="d-flex flex-wrap"),
                                ],
                                className="ga-card p-3 mb-3",
                            ),
                            html.Div(
                                [
                                    html.Div("Fields", className="ga-card-title mb-2"),
                                    html.Div(field_items, className="map-sidebar-fields"),
                                ],
                                className="ga-card p-3",
                            ),
                        ],
                        lg=3,
                        className="mb-4",
                    ),
                    # Map
                    dbc.Col(
                        [
                            html.Div(
                                dcc.Graph(
                                    id="map-explorer-graph",
                                    figure=fig,
                                    config={"displayModeBar": True, "scrollZoom": True},
                                    style={"height": "calc(100vh - 240px)", "minHeight": "500px"},
                                ),
                                className="ga-card p-0 overflow-hidden",
                            ),
                        ],
                        lg=9,
                        className="mb-4",
                    ),
                ],
                className="ga-container",
            ),
        ],
        className="ga-main",
    )


