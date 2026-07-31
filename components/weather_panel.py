"""Weather Panel — 4-panel weather chart."""

from __future__ import annotations

from dash import html, dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from data import get_weather_by_year


def create_weather_panel(year: int = 2025) -> html.Div:
    """Build the 4-panel weather chart."""
    fig = _build_weather_figure(year)
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Weather Analytics", className="ga-card-title"),
                    html.Div(
                        [
                            html.Button(
                                "📥 CSV",
                                id="btn-export-weather",
                                className="ga-card-btn",
                            ),
                        ],
                        className="ga-card-actions",
                    ),
                ],
                className="ga-card-header",
            ),
            dcc.Graph(
                id="weather-chart",
                figure=fig,
                config={"displayModeBar": True, "modeBarButtonsToRemove": ["lasso2d", "select2d"]},
                style={"height": "400px"},
                className="ga-animate-fade",
            ),
        ],
        className="ga-card",
    )


def _build_weather_figure(year: int) -> go.Figure:
    """Build the 4-panel weather figure."""
    data = get_weather_by_year(year)
    months = [d["month_name"] for d in data]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Temperature (°C)", "Rainfall (mm)", "Solar Radiation (W/m²)", "Humidity (%)"),
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
    )
    
    # Temperature
    fig.add_trace(
        go.Scatter(
            x=months, y=[d["t2m_avg"] for d in data],
            mode="lines", name="Avg",
            line={"color": "#F57F17", "width": 2},
            hovertemplate="%{y:.1f}°C<extra>Avg Temp</extra>",
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=months, y=[d["t2m_max_avg"] for d in data],
            mode="lines", name="Max",
            line={"color": "#C62828", "width": 2, "dash": "dash"},
            hovertemplate="%{y:.1f}°C<extra>Max Temp</extra>",
        ),
        row=1, col=1,
    )
    
    # Rainfall
    fig.add_trace(
        go.Bar(
            x=months, y=[d["rainfall_mm"] for d in data],
            marker_color="#1565C0",
            name="Rainfall",
            hovertemplate="%{y:.1f} mm<extra>Rainfall</extra>",
        ),
        row=1, col=2,
    )
    
    # Solar
    fig.add_trace(
        go.Scatter(
            x=months, y=[d["solar_wm2"] for d in data],
            mode="lines", name="Solar",
            line={"color": "#F9A825", "width": 2},
            fill="tozeroy",
            fillcolor="rgba(249, 168, 37, 0.2)",
            hovertemplate="%{y:.1f} W/m²<extra>Solar</extra>",
        ),
        row=2, col=1,
    )
    
    # Humidity
    fig.add_trace(
        go.Scatter(
            x=months, y=[d["humidity_pct"] for d in data],
            mode="lines", name="Humidity",
            line={"color": "#42A5F5", "width": 2},
            fill="tozeroy",
            fillcolor="rgba(66, 165, 245, 0.2)",
            hovertemplate="%{y:.1f}%<extra>Humidity</extra>",
        ),
        row=2, col=2,
    )
    
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        margin={"l": 50, "r": 20, "t": 50, "b": 30},
        height=400,
    )
    
    # Update all axes
    for i in range(1, 5):
        row = (i - 1) // 2 + 1
        col = (i - 1) % 2 + 1
        fig.update_xaxes(showgrid=False, row=row, col=col)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)", row=row, col=col)
    
    return fig
