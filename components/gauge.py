"""Gauge component — Enhanced with risk categories and historical comparison."""

from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

from data import FIELDS


def create_gauge(field_id: str | None = None) -> html.Div:
    """Build the enhanced stress gauge with risk categories."""
    if field_id:
        field = next((f for f in FIELDS if f["id"] == field_id), FIELDS[0])
        value = field["stress_index"]
        title = f"{field['name']} Stress"
    else:
        value = int(np.mean([f["stress_index"] for f in FIELDS]))
        title = "Avg Field Stress"
    
    risk_category = _get_risk_category(value)
    risk_color = _get_risk_color(value)
    
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            number={
                "suffix": "/100",
                "font": {"size": 36, "color": risk_color},
            },
            title={
                "text": f"<b>{title}</b><br><span style='font-size:12px;color:#757575;'>{risk_category}</span>",
                "font": {"size": 14},
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
                    "color": risk_color,
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
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        height=300,
    )
    
    # Historical mini-chart
    hist_data = [30, 32, 31, 33, 35, 34, 33, 32, 31, 30, 32, value]
    hist_fig = go.Figure(
        go.Scatter(
            x=list(range(12)),
            y=hist_data,
            mode="lines+markers",
            line={"color": risk_color, "width": 2},
            marker={"size": 4},
        )
    )
    hist_fig.update_layout(
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"showgrid": False, "showticklabels": False},
        yaxis={"showgrid": False, "showticklabels": False},
        showlegend=False,
        height=60,
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
                responsive=True,
            ),
            
            # Risk category breakdown
            html.Div(
                [
                    html.Div("Risk Breakdown", className="gauge-section-title"),
                    html.Div(
                        [
                            _risk_bar("Healthy", sum(1 for f in FIELDS if f["stress_index"] < 25), len(FIELDS), "#2E7D32"),
                            _risk_bar("Moderate", sum(1 for f in FIELDS if 25 <= f["stress_index"] < 35), len(FIELDS), "#F57F17"),
                            _risk_bar("Critical", sum(1 for f in FIELDS if f["stress_index"] >= 35), len(FIELDS), "#C62828"),
                        ],
                        className="gauge-risk-bars",
                    ),
                ],
                className="gauge-footer",
            ),
            
            # Historical trend
            html.Div(
                [
                    html.Div("12-Month Trend", className="gauge-section-title"),
                    dcc.Graph(
                        figure=hist_fig,
                        config={"displayModeBar": False},
                        style={"height": "60px"},
                        responsive=True,
                    ),
                ],
                className="gauge-footer",
            ),
        ],
        className="ga-card",
    )


def _get_risk_category(value: int) -> str:
    """Get risk category based on stress value."""
    if value < 25:
        return "✅ Healthy"
    elif value < 35:
        return "⚠️ Moderate Risk"
    elif value < 50:
        return "🔴 Elevated Risk"
    else:
        return "🚨 Critical Risk"


def _get_risk_color(value: int) -> str:
    """Get color based on stress value."""
    if value < 25:
        return "#2E7D32"
    elif value < 35:
        return "#F57F17"
    elif value < 50:
        return "#E65100"
    else:
        return "#C62828"


def _risk_bar(label: str, count: int, total: int, color: str) -> html.Div:
    """Create a risk distribution bar."""
    pct = (count / total * 100) if total > 0 else 0
    return html.Div(
        [
            html.Div(
                [
                    html.Span(label, className="risk-label"),
                    html.Span(f"{count} fields", className="risk-count"),
                ],
                className="risk-header",
            ),
            html.Div(
                html.Div(
                    style={
                        "width": f"{pct}%",
                        "height": "100%",
                        "background": color,
                        "borderRadius": "2px",
                        "transition": "width 500ms ease",
                    },
                ),
                className="risk-bar-bg",
            ),
        ],
        className="risk-bar-item",
    )
