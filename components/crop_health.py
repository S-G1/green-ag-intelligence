"""Crop Health page — NDVI analytics, field comparison, health timeline."""

from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from data import FIELDS, get_months
from config import COLORS


def create_crop_health_page() -> html.Div:
    """Build the Crop Health page with NDVI analytics."""
    months = get_months()
    
    # Field comparison chart
    fig_compare = go.Figure()
    for f in FIELDS:
        color = _get_field_color(f["stress_index"])
        fig_compare.add_trace(go.Scatter(
            x=months,
            y=f["ndvi_2025"],
            mode="lines+markers",
            name=f["name"],
            line=dict(color=color, width=2),
            marker=dict(size=6),
        ))
    
    fig_compare.update_layout(
        title="NDVI Timeline Comparison — All Fields",
        xaxis_title="Month",
        yaxis_title="NDVI",
        yaxis_range=[0, 1],
        hovermode="x unified",
        template="plotly_white",
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    # Health cards for each field
    health_cards = []
    for f in FIELDS:
        avg_ndvi = np.mean(f["ndvi_2025"])
        peak_ndvi = max(f["ndvi_2025"])
        peak_month = months[f["ndvi_2025"].index(peak_ndvi)]
        health_status, health_class = _get_health_status(f["stress_index"], avg_ndvi)
        
        health_cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(f["name"], className="ga-card-title"),
                                html.Span(health_status, className=f"ga-badge {health_class}"),
                            ],
                            className="d-flex justify-content-between align-items-start mb-2",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(f"{avg_ndvi:.2f}", className="fs-4 fw-bold"),
                                        html.Div("Avg NDVI", className="text-muted small"),
                                    ],
                                    className="text-center me-3",
                                ),
                                html.Div(
                                    [
                                        html.Div(f"{peak_ndvi:.2f}", className="fs-4 fw-bold"),
                                        html.Div(f"Peak ({peak_month})", className="text-muted small"),
                                    ],
                                    className="text-center me-3",
                                ),
                                html.Div(
                                    [
                                        html.Div(f"{f['stress_index']}", className="fs-4 fw-bold"),
                                        html.Div("Stress", className="text-muted small"),
                                    ],
                                    className="text-center",
                                ),
                            ],
                            className="d-flex justify-content-around mb-2",
                        ),
                        html.Div(
                            f"Crop: {f['crop_2025']}  |  Acres: {f['area_acres']:.1f}",
                            className="text-muted small text-center",
                        ),
                    ],
                    className="ga-card p-3 h-100",
                ),
                lg=3,
                md=6,
                className="mb-4",
            )
        )
    
    # Heatmap of NDVI by field and month
    ndvi_matrix = np.array([f["ndvi_2025"] for f in FIELDS])
    field_names = [f["name"] for f in FIELDS]
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=ndvi_matrix,
        x=months,
        y=field_names,
        colorscale="RdYlGn",
        zmin=0,
        zmax=1,
        colorbar=dict(title="NDVI"),
        hovertemplate="%{y}<br>%{x}: %{z:.2f}<extra></extra>",
    ))
    
    fig_heatmap.update_layout(
        title="NDVI Heatmap — Field x Month",
        xaxis_title="Month",
        yaxis_title="Field",
        height=350,
        margin=dict(l=80, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Crop Health", className="ga-page-title"),
                    html.Div("NDVI analytics and field health monitoring", className="ga-page-subtitle"),
                ],
                className="ga-container mb-4",
            ),
            
            # NDVI Comparison
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(figure=fig_compare, config={"displayModeBar": False}, responsive=True),
                                className="ga-card p-3",
                            ),
                        ],
                        className="ga-container mb-4",
                    ),
                ]
            ),
            
            # NDVI Heatmap
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(figure=fig_heatmap, config={"displayModeBar": False}, responsive=True),
                                className="ga-card p-3",
                            ),
                        ],
                        className="ga-container mb-4",
                    ),
                ]
            ),
            
            # Field Health Cards
            html.Div(
                [
                    html.Div("Field Health Summary", className="ga-card-title ga-container mb-3"),
                    dbc.Row(health_cards, className="ga-container"),
                ],
                className="mb-4",
            ),
        ],
        className="ga-main",
    )


def _get_field_color(stress: int) -> str:
    """Get color for field based on stress."""
    if stress < 25:
        return COLORS["leaf_green"]
    elif stress < 35:
        return COLORS["warning"]
    else:
        return COLORS["critical"]


def _get_health_status(stress: int, avg_ndvi: float) -> tuple[str, str]:
    """Get health status and badge class."""
    if stress < 25 and avg_ndvi > 0.6:
        return "Healthy", "ga-badge-success"
    elif stress < 35:
        return "Monitor", "ga-badge-warning"
    else:
        return "At Risk", "ga-badge-critical"
