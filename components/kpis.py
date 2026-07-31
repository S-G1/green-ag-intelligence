"""KPI Cards component — Enhanced with animations, tooltips, and click filtering."""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

from config import KPI_CONFIG, COLORS, TYPOGRAPHY
from data import (
    get_total_acres, get_avg_stress, get_high_risk_count,
    get_well_drained_count, get_avg_ndvi, FIELDS
)


def create_kpi_cards() -> html.Div:
    """Build the KPI cards grid with enhanced interactions."""
    cards = []
    
    for i, kpi in enumerate(KPI_CONFIG):
        value = _get_kpi_value(kpi["id"])
        trend = _get_kpi_trend(kpi["id"])
        icon_class = _get_kpi_icon_class(kpi["id"])
        tooltip = _get_kpi_tooltip(kpi["id"])
        
        cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    _get_kpi_icon(kpi["icon"]),
                                    className=f"ga-kpi-icon {icon_class}",
                                ),
                                html.Div(
                                    [
                                        html.Span(trend["symbol"], className="me-1"),
                                        html.Span(trend["value"]),
                                    ],
                                    className=f"ga-kpi-trend {trend['direction']}",
                                ) if trend else None,
                            ],
                            className="ga-kpi-header",
                        ),
                        html.Div(
                            value,
                            className="ga-kpi-value",
                            id=f"kpi-value-{kpi['id']}",
                        ),
                        html.Div(kpi["label"], className="ga-kpi-label"),
                        
                        # Sparkline
                        html.Div(
                            _create_sparkline(kpi["id"]),
                            className="ga-kpi-sparkline",
                        ),
                        
                        # Hidden tooltip content
                        html.Div(
                            tooltip,
                            id=f"kpi-tooltip-{kpi['id']}",
                            style={"display": "none"},
                        ),
                    ],
                    className=f"ga-kpi-card ga-animate-fade-up",
                    id=f"kpi-card-{kpi['id']}",
                    style={"animation-delay": f"{i * 50}ms"},
                    **{"data-kpi-id": kpi["id"]},
                ),
                xs=6,
                md=4,
                lg=2,
                className="mb-3",
            )
        )
    
    return html.Div(dbc.Row(cards, className="ga-kpi-grid ga-stagger"))


def _get_kpi_value(kpi_id: str) -> str:
    """Get formatted value for a KPI."""
    if kpi_id == "total_fields":
        return str(len(FIELDS))
    elif kpi_id == "total_acres":
        return f"{get_total_acres():.1f}"
    elif kpi_id == "avg_ndvi":
        return f"{get_avg_ndvi():.2f}"
    elif kpi_id == "avg_stress":
        return f"{get_avg_stress()}/100"
    elif kpi_id == "high_risk":
        return str(get_high_risk_count())
    elif kpi_id == "well_drained":
        return str(get_well_drained_count())
    return "0"


def _get_kpi_trend(kpi_id: str) -> dict | None:
    """Get trend indicator for a KPI."""
    trends = {
        "total_fields": {"symbol": "→", "value": "Stable", "direction": "up"},
        "total_acres": {"symbol": "↑", "value": "+2.3%", "direction": "up"},
        "avg_ndvi": {"symbol": "↑", "value": "+0.05", "direction": "up"},
        "avg_stress": {"symbol": "↓", "value": "-3 pts", "direction": "down"},
        "high_risk": {"symbol": "↓", "value": "-1", "direction": "down"},
        "well_drained": {"symbol": "→", "value": "Stable", "direction": "up"},
    }
    return trends.get(kpi_id)


def _get_kpi_icon_class(kpi_id: str) -> str:
    """Get CSS class for KPI icon color."""
    if kpi_id in ["avg_stress", "high_risk"]:
        if get_avg_stress() > 35:
            return "critical"
        elif get_avg_stress() > 25:
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
        "water": "💧",
    }
    return icons.get(icon_name, "📈")


def _get_kpi_tooltip(kpi_id: str) -> str:
    """Get tooltip definition for a KPI."""
    tooltips = {
        "total_fields": "Total number of active fields being monitored in the current farm.",
        "total_acres": "Combined area of all fields in acres. Based on field boundary calculations.",
        "avg_ndvi": "Normalized Difference Vegetation Index (0-1). Higher values indicate healthier vegetation.",
        "avg_stress": "Composite stress index (0-100). Combines heat, moisture, and vegetation stress factors.",
        "high_risk": "Number of fields requiring immediate attention due to stress index > 35.",
        "well_drained": "Fields with adequate drainage. Poor drainage can lead to waterlogging and root diseases.",
    }
    return tooltips.get(kpi_id, "")


def _create_sparkline(kpi_id: str) -> dcc.Graph:
    """Create a mini sparkline chart for a KPI."""
    if kpi_id == "avg_ndvi":
        y_data = [0.45, 0.52, 0.61, 0.73, 0.82, 0.85, 0.83, 0.78, 0.65, 0.48, 0.38, 0.42]
        color = COLORS["leaf_green"]
    elif kpi_id == "avg_stress":
        y_data = [42, 40, 38, 35, 33, 32, 31, 30, 32, 34, 36, 38]
        color = COLORS["warning"]
    else:
        y_data = [10, 12, 11, 13, 14, 15, 16, 15, 14, 13, 12, 11]
        color = COLORS["deep_blue"]
    
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
    
    return dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "40px"})
