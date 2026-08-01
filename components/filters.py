"""Filter Toolbar component — Inline compact filters with primary dashboard actions."""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from data import YEARS, CROPS, FIELDS


def create_filter_toolbar() -> html.Div:
    """Build the inline filter toolbar with primary dashboard actions."""
    return html.Div(
        [
            # Primary Dashboard Actions
            html.Div(
                [
                    html.Button(
                        [html.Span("📂", className="me-1"), "Open Existing Farm"],
                        id="btn-open-existing-farm",
                        className="ga-filter-btn ga-filter-btn-primary",
                        type="button",
                        title="Open an existing farm",
                    ),
                    html.Button(
                        [html.Span("＋", className="me-1"), "Add Farm"],
                        id="btn-add-new-farm",
                        className="ga-filter-btn ga-filter-btn-secondary",
                        type="button",
                        title="Add a new farm",
                    ),
                    html.Button(
                        [html.Span("▶", className="me-1"), "Launch Demo Mode"],
                        id="btn-launch-demo-mode",
                        className="ga-filter-btn",
                        type="button",
                        title="Launch demo with Maryland farm data",
                    ),
                ],
                className="ga-dashboard-actions",
            ),
            
            # Filter row
            html.Div(
                [
                    # Grower
                    html.Div(
                        [
                            html.Span("Grower", className="ga-filter-label"),
                            dbc.Select(
                                id="filter-grower",
                                options=[{"label": "md-grower", "value": "md-grower"}],
                                value="md-grower",
                                className="ga-filter-select",
                            ),
                        ],
                        className="ga-filter-group",
                    ),
                    
                    html.Div(className="ga-filter-divider"),
                    
                    # Farm
                    html.Div(
                        [
                            html.Span("Farm", className="ga-filter-label"),
                            dbc.Select(
                                id="filter-farm",
                                options=[{"label": "Caroline County Farm", "value": "md-caroline-farm"}],
                                value="md-caroline-farm",
                                className="ga-filter-select",
                            ),
                        ],
                        className="ga-filter-group",
                    ),
                    
                    html.Div(className="ga-filter-divider"),
                    
                    # Year
                    html.Div(
                        [
                            html.Span("Year", className="ga-filter-label"),
                            dbc.Select(
                                id="filter-year",
                                options=[{"label": str(y), "value": y} for y in YEARS],
                                value=2025,
                                className="ga-filter-select",
                            ),
                        ],
                        className="ga-filter-group",
                    ),
                    
                    html.Div(className="ga-filter-divider"),
                    
                    # Crop
                    html.Div(
                        [
                            html.Span("Crop", className="ga-filter-label"),
                            dbc.Select(
                                id="filter-crop",
                                options=[{"label": c, "value": c} for c in CROPS],
                                value="Soybeans",
                                className="ga-filter-select",
                            ),
                        ],
                        className="ga-filter-group",
                    ),
                    
                    html.Div(className="ga-filter-divider"),
                    
                    # Map Layer
                    html.Div(
                        [
                            html.Span("Layer", className="ga-filter-label"),
                            dbc.Select(
                                id="filter-layer",
                                options=[
                                    {"label": "Environmental Risk", "value": "risk"},
                                    {"label": "NDVI", "value": "ndvi"},
                                    {"label": "Heat Stress", "value": "heat_stress"},
                                    {"label": "Rainfall", "value": "rainfall"},
                                ],
                                value="risk",
                                className="ga-filter-select",
                            ),
                        ],
                        className="ga-filter-group",
                    ),
                    
                    html.Div(className="ga-filter-divider"),
                    
                    # Action buttons
                    html.Button(
                        [html.Span("↺", className="me-1"), "Reset"],
                        id="btn-reset-filters",
                        className="ga-filter-btn",
                        type="button",
                    ),
                    
                    html.Button(
                        [html.Span("↻", className="me-1"), "Refresh"],
                        id="btn-refresh",
                        className="ga-filter-btn",
                        type="button",
                    ),
                    
                    html.Button(
                        [html.Span("📊", className="me-1"), "Export"],
                        id="btn-export",
                        className="ga-filter-btn",
                        type="button",
                    ),
                ],
                className="ga-filter-toolbar",
            ),
        ]
    )
