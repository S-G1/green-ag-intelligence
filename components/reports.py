"""Reports page — Data summaries, charts, batch export."""

from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from data import FIELDS, WEATHER_MONTHLY
from config import COLORS


def create_reports_page() -> html.Div:
    """Build the Reports page."""
    
    # Farm summary
    total_acres = sum(f["area_acres"] for f in FIELDS)
    avg_stress = int(np.mean([f["stress_index"] for f in FIELDS]))
    avg_ndvi = round(np.mean([f["ndvi_2025"][6] for f in FIELDS]), 2)
    high_risk = sum(1 for f in FIELDS if f["stress_index"] > 35)
    
    # Crop distribution
    crop_counts = {}
    for f in FIELDS:
        crop_counts[f["crop_2025"]] = crop_counts.get(f["crop_2025"], 0) + 1
    
    fig_crops = go.Figure(data=[go.Pie(
        labels=list(crop_counts.keys()),
        values=list(crop_counts.values()),
        hole=0.4,
        marker=dict(colors=[COLORS["leaf_green"], COLORS["ocean_blue"], COLORS["warning"]]),
    )])
    fig_crops.update_layout(
        title="Crop Distribution",
        template="plotly_white",
        height=300,
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
    )
    
    # Stress distribution
    stress_bins = {"Low (<25)": 0, "Medium (25-35)": 0, "High (>35)": 0}
    for f in FIELDS:
        if f["stress_index"] < 25:
            stress_bins["Low (<25)"] += 1
        elif f["stress_index"] < 35:
            stress_bins["Medium (25-35)"] += 1
        else:
            stress_bins["High (>35)"] += 1
    
    fig_stress = go.Figure(data=[go.Bar(
        x=list(stress_bins.keys()),
        y=list(stress_bins.values()),
        marker=dict(color=[COLORS["leaf_green"], COLORS["warning"], COLORS["critical"]]),
    )])
    fig_stress.update_layout(
        title="Stress Risk Distribution",
        xaxis_title="Risk Category",
        yaxis_title="Fields",
        template="plotly_white",
        height=300,
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    # Weather summary table
    df_weather = pd.DataFrame(WEATHER_MONTHLY)
    annual = df_weather.groupby("year").agg({
        "rainfall_mm": "sum",
        "t2m_avg": "mean",
        "heat_stress_days": "sum",
    }).reset_index()
    
    weather_rows = []
    for _, row in annual.iterrows():
        weather_rows.append(html.Tr([
            html.Td(f"{int(row['year'])}"),
            html.Td(f"{row['rainfall_mm']:.0f} mm"),
            html.Td(f"{row['t2m_avg']:.1f} °C"),
            html.Td(f"{int(row['heat_stress_days'])} days"),
        ]))
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Reports", className="ga-page-title"),
                    html.Div("Farm performance summaries and data exports", className="ga-page-subtitle"),
                ],
                className="ga-container mb-4",
            ),
            
            # KPI Summary
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Total Acres", className="text-muted small"),
                                html.Div(f"{total_acres:.1f}", className="fs-3 fw-bold"),
                            ],
                            className="ga-card p-3 h-100",
                        ),
                        lg=3,
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Avg NDVI (Jul)", className="text-muted small"),
                                html.Div(f"{avg_ndvi}", className="fs-3 fw-bold"),
                            ],
                            className="ga-card p-3 h-100",
                        ),
                        lg=3,
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Avg Stress", className="text-muted small"),
                                html.Div(f"{avg_stress}/100", className="fs-3 fw-bold"),
                            ],
                            className="ga-card p-3 h-100",
                        ),
                        lg=3,
                        md=6,
                        className="mb-4",
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("High Risk Fields", className="text-muted small"),
                                html.Div(f"{high_risk}", className="fs-3 fw-bold text-danger"),
                            ],
                            className="ga-card p-3 h-100",
                        ),
                        lg=3,
                        md=6,
                        className="mb-4",
                    ),
                ],
                className="ga-container mb-4",
            ),
            
            # Charts
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(figure=fig_crops, config={"displayModeBar": False}),
                        lg=6,
                        className="ga-card p-3 mb-4",
                    ),
                    dbc.Col(
                        dcc.Graph(figure=fig_stress, config={"displayModeBar": False}),
                        lg=6,
                        className="ga-card p-3 mb-4",
                    ),
                ],
                className="ga-container",
            ),
            
            # Weather summary
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Annual Weather Summary", className="ga-card-title"),
                            html.Div(
                                [
                                    html.Button("📊 Excel", className="ga-card-btn me-2", id="btn-report-excel"),
                                    html.Button("📥 CSV", className="ga-card-btn", id="btn-report-csv"),
                                ],
                                className="ga-card-actions",
                            ),
                        ],
                        className="ga-card-header",
                    ),
                    html.Div(
                        html.Table(
                            [
                                html.Thead(html.Tr([
                                    html.Th("Year"),
                                    html.Th("Total Rainfall"),
                                    html.Th("Avg Temperature"),
                                    html.Th("Heat Stress Days"),
                                ])),
                                html.Tbody(weather_rows),
                            ],
                            className="ga-table",
                        ),
                        className="ga-table-container",
                    ),
                ],
                className="ga-card p-3 ga-container mb-4",
            ),
        ],
        className="ga-main",
    )
