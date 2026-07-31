"""NDVI Panel — Interactive bar chart with sorting and field filter."""

from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

from data import FIELDS, get_months


def create_ndvi_panel(field_id: str | None = None, month: int = 6, sort_by: str = "value") -> html.Div:
    """Build the NDVI panel with bar chart, slider, and controls."""
    fig = _build_ndvi_bar_chart(field_id, month, sort_by)
    months = get_months()
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("NDVI Comparison", className="ga-card-title"),
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="ndvi-sort",
                                options=[
                                    {"label": "Sort: Value", "value": "value"},
                                    {"label": "Sort: Name", "value": "name"},
                                    {"label": "Sort: Risk", "value": "risk"},
                                ],
                                value="value",
                                clearable=False,
                                className="ndvi-sort-dropdown",
                                style={"width": "120px"},
                            ),
                            html.Button(
                                "▶",
                                id="btn-ndvi-play",
                                className="ga-ndvi-play-btn",
                            ),
                        ],
                        className="ga-card-actions",
                    ),
                ],
                className="ga-card-header",
            ),
            
            html.Div(
                [
                    dcc.Slider(
                        id="ndvi-slider",
                        min=0,
                        max=11,
                        step=1,
                        value=month,
                        marks={i: {"label": m, "style": {"fontSize": "0.7rem"}} for i, m in enumerate(months)},
                        className="ga-ndvi-slider",
                    ),
                ],
                className="mb-3",
            ),
            
            dcc.Interval(
                id="ndvi-interval",
                interval=1000,
                n_intervals=0,
                disabled=True,
            ),
            
            dcc.Graph(
                id="ndvi-chart",
                figure=fig,
                config={"displayModeBar": True, "modeBarButtonsToRemove": ["lasso2d", "select2d"]},
                style={"height": "300px"},
                className="ga-animate-fade",
            ),
        ],
        className="ga-card",
    )


def _build_ndvi_bar_chart(field_id: str | None, month: int, sort_by: str) -> go.Figure:
    """Build the NDVI bar chart with sorting."""
    
    # Prepare data
    data = []
    for f in FIELDS:
        ndvi = f["ndvi_2025"][month]
        data.append({
            "name": f["name"],
            "ndvi": ndvi,
            "stress": f["stress_index"],
            "id": f["id"],
        })
    
    # Sort
    if sort_by == "value":
        data.sort(key=lambda x: x["ndvi"], reverse=True)
    elif sort_by == "name":
        data.sort(key=lambda x: x["name"])
    elif sort_by == "risk":
        data.sort(key=lambda x: x["stress"], reverse=True)
    
    names = [d["name"] for d in data]
    ndvi_values = [d["ndvi"] for d in data]
    colors = [_ndvi_color(v) for v in ndvi_values]
    
    fig = go.Figure()
    
    # Add average line
    avg_ndvi = np.mean(ndvi_values)
    fig.add_hline(
        y=avg_ndvi,
        line_dash="dash",
        line_color="#757575",
        line_width=2,
        annotation_text=f"Avg: {avg_ndvi:.2f}",
        annotation_position="right",
    )
    
    # Add bars
    fig.add_trace(go.Bar(
        x=names,
        y=ndvi_values,
        marker_color=colors,
        text=[f"{v:.2f}" for v in ndvi_values],
        textposition="outside",
        textfont={"size": 10},
        hovertemplate="<b>%{x}</b><br>NDVI: %{y:.3f}<extra></extra>",
    ))
    
    # Highlight selected field
    if field_id:
        for i, d in enumerate(data):
            if d["id"] == field_id:
                fig.add_annotation(
                    x=d["name"],
                    y=d["ndvi"] + 0.05,
                    text="★",
                    showarrow=False,
                    font={"size": 16, "color": "#F57F17"},
                )
    
    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="NDVI",
        yaxis_range=[0, 1.1],
        template="plotly_white",
        margin={"l": 40, "r": 20, "t": 20, "b": 60},
        showlegend=False,
        hovermode="x unified",
        xaxis={"tickangle": -30, "tickfont": {"size": 9}},
    )
    
    return fig


def _ndvi_color(ndvi: float) -> str:
    """Get color based on NDVI value."""
    if ndvi >= 0.7:
        return "#2E7D32"  # Healthy
    elif ndvi >= 0.5:
        return "#F9A825"  # Moderate
    elif ndvi >= 0.3:
        return "#F57F17"  # Poor
    else:
        return "#C62828"  # Critical
