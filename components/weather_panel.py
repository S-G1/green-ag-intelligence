"""Weather Panel — Tabbed weather analytics with brush selection."""

from __future__ import annotations

from dash import html, dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from data import get_weather_by_year


def create_weather_panel(year: int = 2025, active_tab: str = "combined") -> html.Div:
    """Build the tabbed weather panel."""
    
    tabs = html.Div(
        [
            html.Button(
                "🌡️ Combined",
                id="weather-tab-combined",
                className=f"weather-tab {'active' if active_tab == 'combined' else ''}",
            ),
            html.Button(
                "🌧️ Rainfall",
                id="weather-tab-rainfall",
                className=f"weather-tab {'active' if active_tab == 'rainfall' else ''}",
            ),
            html.Button(
                "🌡️ Temperature",
                id="weather-tab-temperature",
                className=f"weather-tab {'active' if active_tab == 'temperature' else ''}",
            ),
            html.Button(
                "🔥 Heat Stress",
                id="weather-tab-heat",
                className=f"weather-tab {'active' if active_tab == 'heat' else ''}",
            ),
        ],
        className="weather-tabs",
    )
    
    fig = _build_weather_figure(year, active_tab)
    
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
            
            tabs,
            
            dcc.Graph(
                id="weather-chart",
                figure=fig,
                config={
                    "displayModeBar": True,
                    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                    "displaylogo": False,
                },
                style={"height": "400px"},
                className="ga-animate-fade",
                responsive=True,
            ),
        ],
        className="ga-card",
    )


def _build_weather_figure(year: int, tab: str) -> go.Figure:
    """Build weather figure based on active tab."""
    data = get_weather_by_year(year)
    months = [d["month_name"] for d in data]
    
    if tab == "combined":
        return _build_combined_figure(data, months)
    elif tab == "rainfall":
        return _build_rainfall_figure(data, months)
    elif tab == "temperature":
        return _build_temperature_figure(data, months)
    elif tab == "heat":
        return _build_heat_stress_figure(data, months)
    
    return _build_combined_figure(data, months)


def _build_combined_figure(data, months):
    """Build 4-panel combined weather figure."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Temperature (°C)", "Rainfall (mm)", "Solar Radiation (W/m²)", "Humidity (%)"),
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
    )
    
    fig.add_trace(
        go.Scatter(
            x=months, y=[d["t2m_avg"] for d in data],
            mode="lines", name="Avg Temp",
            line={"color": "#F57F17", "width": 2},
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Bar(
            x=months, y=[d["rainfall_mm"] for d in data],
            marker_color="#1565C0", name="Rainfall",
        ),
        row=1, col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=months, y=[d["solar_wm2"] for d in data],
            mode="lines", name="Solar",
            line={"color": "#F9A825", "width": 2},
        ),
        row=2, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=months, y=[d["humidity_pct"] for d in data],
            mode="lines", name="Humidity",
            line={"color": "#42A5F5", "width": 2},
        ),
        row=2, col=2,
    )
    
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        margin={"l": 50, "r": 20, "t": 50, "b": 30},
        height=400,
    )
    
    return fig


def _build_rainfall_figure(data, months):
    """Build rainfall-focused figure."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=[d["rainfall_mm"] for d in data],
        marker_color="#1565C0",
        name="Rainfall",
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=[sum([d["rainfall_mm"] for d in data[:i+1]]) for i in range(len(data))],
        mode="lines",
        name="Cumulative",
        line={"color": "#F57F17", "width": 2},
        yaxis="y2",
    ))
    
    fig.update_layout(
        title="Monthly Rainfall & Cumulative",
        yaxis_title="Rainfall (mm)",
        yaxis2=dict(title="Cumulative (mm)", overlaying="y", side="right"),
        template="plotly_white",
        height=400,
        margin={"l": 50, "r": 50, "t": 40, "b": 30},
    )
    
    return fig


def _build_temperature_figure(data, months):
    """Build temperature-focused figure."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=[d["t2m_avg"] for d in data],
        mode="lines+markers", name="Average",
        line={"color": "#42A5F5", "width": 2},
        marker={"size": 8},
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=[d["t2m_max_avg"] for d in data],
        mode="lines", name="Max",
        line={"color": "#F57F17", "width": 2, "dash": "dash"},
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=[d["t2m_min_avg"] for d in data],
        mode="lines", name="Min",
        line={"color": "#1565C0", "width": 2, "dash": "dot"},
    ))
    
    fig.update_layout(
        title="Temperature Trends",
        yaxis_title="Temperature (°C)",
        template="plotly_white",
        height=400,
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.2},
        margin={"l": 50, "r": 20, "t": 40, "b": 60},
    )
    
    return fig


def _build_heat_stress_figure(data, months):
    """Build heat stress figure."""
    heat_days = [d["heat_stress_days"] for d in data]
    colors = ["#48BB78" if d < 10 else "#F6AD55" if d < 50 else "#FC8181" for d in heat_days]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=heat_days,
        marker_color=colors,
        name="Heat Stress Days",
        text=heat_days,
        textposition="outside",
    ))
    
    fig.add_hline(y=30, line_dash="dash", line_color="#C62828", annotation_text="Alert Threshold")
    
    fig.update_layout(
        title="Heat Stress Days (Tmax > 30°C)",
        yaxis_title="Days",
        template="plotly_white",
        height=400,
        margin={"l": 50, "r": 20, "t": 40, "b": 30},
    )
    
    return fig
