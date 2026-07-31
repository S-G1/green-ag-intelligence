"""Farm Management page — Field listing with management actions."""

from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc

from data import FIELDS
from config import COLORS


def create_farm_management_page() -> html.Div:
    """Build the Farm Management page."""
    
    total_acres = sum(f["area_acres"] for f in FIELDS)
    total_fields = len(FIELDS)
    crops = {}
    for f in FIELDS:
        crops[f["crop_2025"]] = crops.get(f["crop_2025"], 0) + 1
    
    # Summary cards
    summary_cards = [
        dbc.Col(
            html.Div(
                [
                    html.Div("Total Fields", className="text-muted small"),
                    html.Div(f"{total_fields}", className="fs-3 fw-bold"),
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
                    html.Div("Crop Types", className="text-muted small"),
                    html.Div(f"{len(crops)}", className="fs-3 fw-bold"),
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
                    html.Div("Avg Field Size", className="text-muted small"),
                    html.Div(f"{total_acres/total_fields:.1f} ac", className="fs-3 fw-bold"),
                ],
                className="ga-card p-3 h-100",
            ),
            lg=3,
            md=6,
            className="mb-4",
        ),
    ]
    
    # Field cards with actions
    field_cards = []
    for f in FIELDS:
        risk_class = "ga-badge-success" if f["stress_index"] < 25 else "ga-badge-warning" if f["stress_index"] < 35 else "ga-badge-critical"
        risk_label = "Low" if f["stress_index"] < 25 else "Medium" if f["stress_index"] < 35 else "High"
        
        field_cards.append(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span("🚜", className="me-2"),
                                        html.Span(f["name"], className="fw-bold"),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                                html.Span(risk_label, className=f"ga-badge {risk_class}"),
                            ],
                            className="d-flex justify-content-between align-items-center mb-2",
                        ),
                        html.Div(
                            [
                                html.Div(f"{f['area_acres']:.1f} acres", className="text-muted small"),
                                html.Div(f"Crop: {f['crop_2025']}", className="text-muted small"),
                                html.Div(f"Soil: {f['soil_type']}", className="text-muted small"),
                                html.Div(f"NDVI: {f['ndvi_2025'][6]:.2f}  |  Stress: {f['stress_index']}", className="text-muted small"),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            [
                                html.Button("View", className="ga-card-btn me-2", id=f"farm-view-{f['id']}"),
                                html.Button("Edit", className="ga-card-btn me-2", id=f"farm-edit-{f['id']}"),
                                html.Button("Report", className="ga-card-btn", id=f"farm-report-{f['id']}"),
                            ],
                            className="d-flex",
                        ),
                    ],
                    className="ga-card p-3 h-100",
                ),
                lg=4,
                md=6,
                className="mb-4",
            )
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Farm Management", className="ga-page-title"),
                    html.Div("Manage fields, crops, and farm operations", className="ga-page-subtitle"),
                ],
                className="ga-container mb-4",
            ),
            
            # Summary
            dbc.Row(summary_cards, className="ga-container mb-4"),
            
            # Field cards
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Field Inventory", className="ga-card-title"),
                            html.Button("+ Add Field", className="ga-filter-btn ga-filter-btn-primary", id="btn-add-field"),
                        ],
                        className="d-flex justify-content-between align-items-center ga-container mb-3",
                    ),
                    dbc.Row(field_cards, className="ga-container"),
                ],
                className="mb-4",
            ),
        ],
        className="ga-main",
    )
