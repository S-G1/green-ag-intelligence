"""Weather page — Dedicated weather dashboard with multi-year analytics."""

from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from data import WEATHER_MONTHLY, get_months
from config import COLORS


def create_weather_page() -> html.Div:
    """Build the dedicated Weather analytics page."""
    df = pd.DataFrame(WEATHER_MONTHLY)
    months = get_months()
    
    # Temperature trends by year
    fig_temp = go.Figure()
    for year in sorted(df["year"].unique()):
        year_data = df[df["year"] == year]
        fig_temp.add_trace(go.Scatter(
            x=year_data["month_name"],
            y=year_data["t2m_avg"],
            mode="lines+markers",
            name=f"{year} Avg",
            line=dict(width=2),
        ))
        fig_temp.add_trace(go.Scatter(
            x=year_data["month_name"],
            y=year_data["t2m_max_avg"],
            mode="lines",
            name=f"{year} Max",
            line=dict(width=1, dash="dash"),
            opacity=0.6,
            showlegend=False,
        ))
    
    fig_temp.update_layout(
        title="Temperature Trends (2021–2025)",
        xaxis_title="Month",
        yaxis_title="Temperature (°C)",
        hovermode="x unified",
        template="plotly_white",
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    # Rainfall chart
    fig_rain = go.Figure()
    for year in sorted(df["year"].unique()):
        year_data = df[df["year"] == year]
        fig_rain.add_trace(go.Bar(
            x=year_data["month_name"],
            y=year_data["rainfall_mm"],
            name=str(year),
            opacity=0.7,
        ))
    
    fig_rain.update_layout(
        title="Monthly Rainfall (2021–2025)",
        xaxis_title="Month",
        yaxis_title="Rainfall (mm)",
        barmode="group",
        template="plotly_white",
        height=350,
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    # Heat stress days
    fig_stress = go.Figure()
    for year in sorted(df["year"].unique()):
        year_data = df[df["year"] == year]
        fig_stress.add_trace(go.Scatter(
            x=year_data["month_name"],
            y=year_data["heat_stress_days"],
            mode="lines+markers",
            name=str(year),
            fill="tozeroy",
            line=dict(width=2),
        ))
    
    fig_stress.update_layout(
        title="Heat Stress Days (2021–2025)",
        xaxis_title="Month",
        yaxis_title="Days",
        hovermode="x unified",
        template="plotly_white",
        height=350,
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    # Annual summary stats
    annual_summary = df.groupby("year").agg({
        "rainfall_mm": "sum",
        "t2m_avg": "mean",
        "heat_stress_days": "sum",
        "solar_wm2": "mean",
    }).reset_index()
    
    summary_cards = []
    for _, row in annual_summary.iterrows():
        summary_cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(f"{int(row['year'])}", className="ga-card-title mb-2"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(f"{row['rainfall_mm']:.0f}", className="fs-5 fw-bold"),
                                        html.Div("mm Rain", className="text-muted small"),
                                    ],
                                    className="text-center me-2",
                                ),
                                html.Div(
                                    [
                                        html.Div(f"{row['t2m_avg']:.1f}°C", className="fs-5 fw-bold"),
                                        html.Div("Avg Temp", className="text-muted small"),
                                    ],
                                    className="text-center me-2",
                                ),
                                html.Div(
                                    [
                                        html.Div(f"{int(row['heat_stress_days'])}", className="fs-5 fw-bold"),
                                        html.Div("Stress Days", className="text-muted small"),
                                    ],
                                    className="text-center",
                                ),
                            ],
                            className="d-flex justify-content-around",
                        ),
                    ],
                    className="ga-card p-3 h-100",
                ),
                lg=2,
                md=4,
                className="mb-4",
            )
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Weather Analytics", className="ga-page-title"),
                    html.Div("Multi-year weather trends and heat stress analysis", className="ga-page-subtitle"),
                ],
                className="ga-container mb-4",
            ),
            
            # Annual summary
            dbc.Row(summary_cards, className="ga-container mb-4"),
            
            # Temperature
            dbc.Row(
                [
                    dbc.Col(
                                dcc.Graph(figure=fig_temp, config={"displayModeBar": False}, responsive=True),
                        className="ga-card p-3 mb-4",
                    ),
                ],
                className="ga-container",
            ),
            
            # Rainfall & Heat Stress
            dbc.Row(
                [
                    dbc.Col(
                                dcc.Graph(figure=fig_rain, config={"displayModeBar": False}, responsive=True),
                        lg=6,
                        className="ga-card p-3 mb-4",
                    ),
                    dbc.Col(
                                dcc.Graph(figure=fig_stress, config={"displayModeBar": False}, responsive=True),
                        lg=6,
                        className="ga-card p-3 mb-4",
                    ),
                ],
                className="ga-container",
            ),
        ],
        className="ga-main",
    )
