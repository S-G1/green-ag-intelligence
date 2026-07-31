"""Gauge component — Animated circular stress gauge."""

from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

from data import FIELDS


def create_gauge(field_id: str | None = None) -> html.Div:
    """Build the stress index gauge."""
    if field_id:
        field = next((f for f in FIELDS if f["id"] == field_id), FIELDS[0])
        value = field["stress_index"]
        title = f"{field['name']} Stress"
    else:
        value = int(np.mean([f["stress_index"] for f in FIELDS]))
        title = "Avg Field Stress"
    
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            number={
                "suffix": "/100",
                "font": {"size": 36, "color": _get_gauge_color(value)},
            },
            title={
                "text": title,
                "font": {"size": 14, "color": "#757575"},
            },
            delta={
                "reference": 50,
                "relative": False,
                "valueformat": ".0f",
                "increasing": {"color": "#C62828"},
                "decreasing": {"color": "#2E7D32"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#E0E0E0",
                },
                "bar": {
                    "color": _get_gauge_color(value),
                    "thickness": 0.75,
                },
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#E0E0E0",
                "steps": [
                    {"range": [0, 25], "color": "rgba(46, 125, 50, 0.1)"},
                    {"range": [25, 50], "color": "rgba(245, 127, 23, 0.1)"},
                    {"range": [50, 100], "color": "rgba(198, 40, 40, 0.1)"},
                ],
                "threshold": {
                    "line": {"color": "#C62828", "width": 3},
                    "thickness": 0.8,
                    "value": 50,
                },
            },
        )
    )
    
    fig.update_layout(
        template="plotly_white",
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        height=300,
    )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Stress Index", className="ga-card-title"),
                ],
                className="ga-card-header",
            ),
            dcc.Graph(
                id="stress-gauge",
                figure=fig,
                config={"displayModeBar": False},
                style={"height": "300px"},
                className="ga-animate-fade",
            ),
        ],
        className="ga-card",
    )


def _get_gauge_color(value: int) -> str:
    """Get color based on stress value."""
    if value < 25:
        return "#2E7D32"
    elif value < 50:
        return "#F57F17"
    else:
        return "#C62828"
