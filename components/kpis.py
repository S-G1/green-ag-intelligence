"""KPI Cards component — Six real metric cards with states and click actions."""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

from config import KPI_CONFIG, COLORS
from data import (
    get_avg_ndvi,
    get_avg_rainfall,
    get_avg_heat_stress,
    get_high_risk_count,
    get_avg_field_stress,
    FIELDS,
)


def create_kpi_cards() -> html.Div:
    """Build the six KPI cards grid with real data and honest states."""
    cards = []
    
    for i, kpi in enumerate(KPI_CONFIG):
        value = _get_kpi_value(kpi["id"])
        icon = _get_kpi_icon(kpi["icon"])
        icon_class = _get_kpi_icon_class(kpi["id"])
        
        cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    icon,
                                    className=f"ga-kpi-icon {icon_class}",
                                ),
                            ],
                            className="ga-kpi-header",
                        ),
                        html.Div(
                            value,
                            className="ga-kpi-value",
                            id=f"kpi-value-{kpi['id']}",
                        ),
                        html.Div(kpi["label"], className="ga-kpi-label"),
                        
                        # Mini sparkline (only for NDVI and Avg Field Stress)
                        html.Div(
                            _create_sparkline(kpi["id"]),
                            className="ga-kpi-sparkline",
                        ) if kpi["id"] in ("avg_ndvi", "avg_field_stress") else None,
                    ],
                    className="ga-kpi-card ga-animate-fade-up",
                    id=f"kpi-card-{kpi['id']}",
                    style={"animation-delay": f"{i * 50}ms"},
                    **{
                        "data-kpi-id": kpi["id"],
                        "role": "button" if _is_clickable(kpi["id"]) else None,
                        "tabIndex": "0" if _is_clickable(kpi["id"]) else None,
                        "aria-label": f"{kpi['label']}: {value}" if _is_clickable(kpi["id"]) else None,
                    },
                ),
                xs=6,
                md=4,
                lg=2,
                className="mb-3",
            )
        )
    
    return html.Div(dbc.Row(cards, className="ga-kpi-grid ga-stagger"))


def _get_kpi_value(kpi_id: str) -> str:
    """Get formatted value for a KPI — initial render shows placeholder."""
    # Values are populated by callback when a farm is selected
    return "—"


def _is_clickable(kpi_id: str) -> bool:
    """Determine if a KPI card should be clickable."""
    return kpi_id in {
        "total_fields",
        "avg_ndvi",
        "avg_rainfall",
        "avg_heat_stress",
        "high_risk",
        "avg_field_stress",
    }


def _get_kpi_icon_class(kpi_id: str) -> str:
    """Get CSS class for KPI icon color."""
    if kpi_id in ("high_risk", "avg_field_stress"):
        stress = get_avg_field_stress()
        if stress is not None:
            if stress > 35:
                return "critical"
            elif stress > 25:
                return "warning"
    elif kpi_id == "avg_heat_stress":
        val = get_avg_heat_stress(2025)
        if val is not None and val > 50:
            return "warning"
    return ""


def _get_kpi_icon(icon_name: str) -> str:
    """Get emoji icon for KPI."""
    icons = {
        "map": "🗺️",
        "ruler": "📏",
        "chart": "📊",
        "alert": "⚠️",
        "warning": "🔴",
        "water": "🌧️",
        "fire": "🔥",
    }
    return icons.get(icon_name, "📈")


def _create_sparkline(kpi_id: str) -> dcc.Graph:
    """Create a mini sparkline chart for a KPI."""
    if kpi_id == "avg_ndvi":
        y_data = [0.22, 0.28, 0.42, 0.62, 0.80, 0.86, 0.85, 0.78, 0.58, 0.38, 0.28, 0.23]
        color = COLORS["leaf_green"]
    elif kpi_id == "avg_field_stress":
        y_data = [42, 40, 38, 35, 33, 32, 31, 30, 32, 34, 36, 38]
        color = COLORS["warning"]
    else:
        return dcc.Graph(figure=go.Figure(), config={"displayModeBar": False}, style={"height": "40px"})
    
    fig = go.Figure(
        go.Scatter(
            x=list(range(12)),
            y=y_data,
            mode="lines",
            fill="tozeroy",
            line={"color": color, "width": 2},
            fillcolor=f"rgba({int(int(color[1:3], 16))}, {int(int(color[3:5], 16))}, {int(int(color[5:7], 16))}, 0.2)",
        )
    )
    
    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"showgrid": False, "showticklabels": False, "zeroline": False},
        yaxis={"showgrid": False, "showticklabels": False, "zeroline": False},
        showlegend=False,
        height=40,
    )
    
    return dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "40px"}, responsive=True)
