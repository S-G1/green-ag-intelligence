"""NDVI Panel — Chart with slider and play/loop animation."""

from __future__ import annotations

from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

from data import FIELDS, get_months


def create_ndvi_panel(field_id: str | None = None, month: int = 6) -> html.Div:
    """Build the NDVI panel with chart, slider, and controls."""
    fig = _build_ndvi_figure(field_id, month)
    months = get_months()
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("NDVI Trend", className="ga-card-title"),
                    html.Div(
                        [
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


def _build_ndvi_figure(field_id: str | None, highlight_month: int) -> go.Figure:
    """Build the NDVI time series figure."""
    months = get_months()
    fig = go.Figure()
    
    if field_id:
        # Single field
        field = next((f for f in FIELDS if f["id"] == field_id), FIELDS[0])
        fig.add_trace(go.Scatter(
            x=months,
            y=field["ndvi_2025"],
            mode="lines+markers",
            name=field["name"],
            line={"color": "#1B5E20", "width": 3},
            marker={"size": 8, "color": "#1B5E20"},
            fill="tozeroy",
            fillcolor="rgba(27, 94, 32, 0.1)",
        ))
    else:
        # All fields average
        avg_ndvi = [np.mean([f["ndvi_2025"][i] for f in FIELDS]) for i in range(12)]
        fig.add_trace(go.Scatter(
            x=months,
            y=avg_ndvi,
            mode="lines+markers",
            name="Average",
            line={"color": "#1B5E20", "width": 3},
            marker={"size": 8},
            fill="tozeroy",
            fillcolor="rgba(27, 94, 32, 0.1)",
        ))
        
        # Add individual field lines (faint)
        colors = ["#42A5F5", "#F57F17", "#7B1FA2", "#C62828"]
        for i, f in enumerate(FIELDS[:4]):
            fig.add_trace(go.Scatter(
                x=months,
                y=f["ndvi_2025"],
                mode="lines",
                name=f["name"],
                line={"color": colors[i], "width": 1, "dash": "dot"},
                opacity=0.5,
            ))
    
    # Highlight current month with a shape
    fig.add_shape(
        type="line",
        x0=highlight_month,
        x1=highlight_month,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="#F57F17", width=2, dash="dash"),
    )
    
    fig.add_annotation(
        x=highlight_month,
        y=1.02,
        yref="paper",
        text="Current",
        showarrow=False,
        font=dict(color="#F57F17", size=12),
    )
    
    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="NDVI",
        yaxis_range=[0, 1],
        template="plotly_white",
        margin={"l": 40, "r": 20, "t": 20, "b": 40},
        showlegend=False,
        hovermode="x unified",
    )
    
    return fig
