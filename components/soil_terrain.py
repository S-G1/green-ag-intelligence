"""Soil & Terrain page — Soil properties, terrain visualization, drainage analysis."""

from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from data import FIELDS
from config import COLORS


def create_soil_terrain_page() -> html.Div:
    """Build the Soil & Terrain page."""
    
    df = pd.DataFrame([
        {
            "Field": f["name"],
            "Soil": f["soil_type"],
            "pH": f["ph"],
            "OM (%)": f["om_pct"],
            "CEC": f["cec"],
            "Drainage": f["drainage"],
            "Elev Min (m)": f["elevation_min_m"],
            "Elev Max (m)": f["elevation_max_m"],
            "Slope (%)": f["slope_percent"],
            "Area (ac)": f["area_acres"],
        }
        for f in FIELDS
    ])
    
    # Soil properties scatter
    fig_soil = go.Figure()
    for drainage in df["Drainage"].unique():
        subset = df[df["Drainage"] == drainage]
        color = COLORS["ocean_blue"] if "Well" in drainage else COLORS["warning"]
        fig_soil.add_trace(go.Scatter(
            x=subset["pH"],
            y=subset["OM (%)"],
            mode="markers+text",
            text=subset["Field"],
            textposition="top center",
            name=drainage,
            marker=dict(size=subset["Area (ac)"]*2, color=color, opacity=0.7),
            hovertemplate="%{text}<br>pH: %{x:.2f}<br>OM: %{y:.2f}%<extra></extra>",
        ))
    
    fig_soil.update_layout(
        title="Soil Properties — pH vs Organic Matter",
        xaxis_title="pH",
        yaxis_title="Organic Matter (%)",
        template="plotly_white",
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    # Elevation & Slope chart
    fig_elev = go.Figure()
    fig_elev.add_trace(go.Scatter(
        x=df["Field"],
        y=df["Elev Min (m)"],
        mode="lines+markers",
        name="Min Elevation",
        line=dict(color=COLORS["deep_blue"]),
    ))
    fig_elev.add_trace(go.Scatter(
        x=df["Field"],
        y=df["Elev Max (m)"],
        mode="lines+markers",
        name="Max Elevation",
        line=dict(color=COLORS["leaf_green"]),
    ))
    fig_elev.add_trace(go.Bar(
        x=df["Field"],
        y=df["Slope (%)"],
        name="Slope %",
        yaxis="y2",
        marker=dict(color=COLORS["gray_400"], opacity=0.5),
    ))
    
    fig_elev.update_layout(
        title="Elevation Range & Slope by Field",
        xaxis_title="Field",
        yaxis_title="Elevation (m)",
        yaxis2=dict(
            title="Slope (%)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        template="plotly_white",
        height=350,
        margin=dict(l=60, r=60, t=60, b=80),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    
    # Soil table
    table_rows = []
    for _, row in df.iterrows():
        table_rows.append(
            html.Tr([
                html.Td(row["Field"]),
                html.Td(row["Soil"]),
                html.Td(f"{row['pH']:.2f}"),
                html.Td(f"{row['OM (%)']:.2f}"),
                html.Td(f"{row['CEC']:.1f}"),
                html.Td(row["Drainage"]),
                html.Td(f"{row['Elev Min (m)']:.1f} – {row['Elev Max (m)']:.1f}"),
                html.Td(f"{row['Slope (%)']:.1f}"),
            ])
        )
    
    # Drainage summary
    drainage_counts = df["Drainage"].value_counts().to_dict()
    drainage_cards = []
    for drainage, count in drainage_counts.items():
        pct = count / len(df) * 100
        color_class = "text-success" if "Well" in drainage else "text-warning"
        drainage_cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(drainage, className="ga-card-title"),
                        html.Div(
                            [
                                html.Span(f"{count}", className="fs-3 fw-bold me-2"),
                                html.Span(f"({pct:.0f}%)", className="text-muted"),
                            ],
                        ),
                        html.Div(f"of {len(df)} fields", className="text-muted small"),
                    ],
                    className=f"ga-card p-3 h-100 {color_class}",
                ),
                lg=3,
                md=6,
                className="mb-4",
            )
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Soil & Terrain", className="ga-page-title"),
                    html.Div("Soil properties, elevation, and drainage analysis", className="ga-page-subtitle"),
                ],
                className="ga-container mb-4",
            ),
            
            # Drainage summary
            dbc.Row(drainage_cards, className="ga-container mb-4"),
            
            # Soil scatter
            dbc.Row(
                [
                    dbc.Col(
                                dcc.Graph(figure=fig_soil, config={"displayModeBar": False}, responsive=True),
                        className="ga-card p-3 mb-4",
                    ),
                ],
                className="ga-container",
            ),
            
            # Elevation chart
            dbc.Row(
                [
                    dbc.Col(
                                dcc.Graph(figure=fig_elev, config={"displayModeBar": False}, responsive=True),
                        className="ga-card p-3 mb-4",
                    ),
                ],
                className="ga-container",
            ),
            
            # Soil table
            html.Div(
                [
                    html.Div("Soil Properties Detail", className="ga-card-title mb-3"),
                    html.Div(
                        html.Table(
                            [
                                html.Thead(html.Tr([
                                    html.Th("Field"),
                                    html.Th("Soil Type"),
                                    html.Th("pH"),
                                    html.Th("OM (%)"),
                                    html.Th("CEC"),
                                    html.Th("Drainage"),
                                    html.Th("Elevation (m)"),
                                    html.Th("Slope (%)"),
                                ])),
                                html.Tbody(table_rows),
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
