"""Settings page — Theme, notifications, data preferences."""

from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc

from config import APP_NAME, APP_VERSION


def create_settings_page() -> html.Div:
    """Build the Settings page."""
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Settings", className="ga-page-title"),
                    html.Div("Configure your platform preferences", className="ga-page-subtitle"),
                ],
                className="ga-container mb-4",
            ),
            
            dbc.Row(
                [
                    # Appearance
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Appearance", className="ga-card-title mb-3"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Theme", className="fw-medium"),
                                                html.Div("Toggle between light and dark mode", className="text-muted small"),
                                            ],
                                            className="flex-grow-1",
                                        ),
                                        html.Button("Toggle Theme", className="ga-filter-btn ga-filter-btn-primary", id="btn-settings-theme"),
                                    ],
                                    className="d-flex justify-content-between align-items-center py-3 border-bottom",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Reduced Motion", className="fw-medium"),
                                                html.Div("Minimize animations for accessibility", className="text-muted small"),
                                            ],
                                            className="flex-grow-1",
                                        ),
                                        html.Div(
                                            dbc.Switch(
                                                id="setting-reduced-motion",
                                                value=False,
                                                label="",
                                            ),
                                        ),
                                    ],
                                    className="d-flex justify-content-between align-items-center py-3",
                                ),
                            ],
                            className="ga-card p-3 mb-4",
                        ),
                        lg=6,
                    ),
                    
                    # Notifications
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Notifications", className="ga-card-title mb-3"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Email Alerts", className="fw-medium"),
                                                html.Div("Receive risk alerts via email", className="text-muted small"),
                                            ],
                                            className="flex-grow-1",
                                        ),
                                        html.Div(
                                            dbc.Switch(
                                                id="setting-email-alerts",
                                                value=True,
                                                label="",
                                            ),
                                        ),
                                    ],
                                    className="d-flex justify-content-between align-items-center py-3 border-bottom",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Weekly Summary", className="fw-medium"),
                                                html.Div("Get a weekly farm health report", className="text-muted small"),
                                            ],
                                            className="flex-grow-1",
                                        ),
                                        html.Div(
                                            dbc.Switch(
                                                id="setting-weekly-summary",
                                                value=True,
                                                label="",
                                            ),
                                        ),
                                    ],
                                    className="d-flex justify-content-between align-items-center py-3 border-bottom",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Weather Warnings", className="fw-medium"),
                                                html.Div("Alert for extreme weather events", className="text-muted small"),
                                            ],
                                            className="flex-grow-1",
                                        ),
                                        html.Div(
                                            dbc.Switch(
                                                id="setting-weather-warnings",
                                                value=True,
                                                label="",
                                            ),
                                        ),
                                    ],
                                    className="d-flex justify-content-between align-items-center py-3",
                                ),
                            ],
                            className="ga-card p-3 mb-4",
                        ),
                        lg=6,
                    ),
                ],
                className="ga-container mb-4",
            ),
            
            # Data Preferences
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Data Preferences", className="ga-card-title mb-3"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Default Year", className="fw-medium"),
                                                html.Div("Set the default year for analytics", className="text-muted small"),
                                            ],
                                            className="flex-grow-1",
                                        ),
                                        html.Div(
                                            dbc.Select(
                                                id="setting-default-year",
                                                options=[
                                                    {"label": "2025", "value": "2025"},
                                                    {"label": "2024", "value": "2024"},
                                                    {"label": "2023", "value": "2023"},
                                                ],
                                                value="2025",
                                            ),
                                            style={"width": "120px"},
                                        ),
                                    ],
                                    className="d-flex justify-content-between align-items-center py-3 border-bottom",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("Measurement Units", className="fw-medium"),
                                                html.Div("Metric or Imperial", className="text-muted small"),
                                            ],
                                            className="flex-grow-1",
                                        ),
                                        html.Div(
                                            dbc.Select(
                                                id="setting-units",
                                                options=[
                                                    {"label": "Metric", "value": "metric"},
                                                    {"label": "Imperial", "value": "imperial"},
                                                ],
                                                value="metric",
                                            ),
                                            style={"width": "120px"},
                                        ),
                                    ],
                                    className="d-flex justify-content-between align-items-center py-3",
                                ),
                            ],
                            className="ga-card p-3 mb-4",
                        ),
                        lg=6,
                    ),
                    
                    # About
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("About", className="ga-card-title mb-3"),
                                html.Div(
                                    [
                                        html.Div(f"{APP_NAME}", className="fw-bold"),
                                        html.Div(f"Version {APP_VERSION}", className="text-muted small"),
                                        html.Div("Environmental Risk Monitoring & Decision Support", className="text-muted small mt-1"),
                                        html.Div("Real Caroline County, MD data", className="text-muted small"),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    [
                                        html.Div("Data Sources", className="fw-medium mt-3"),
                                        html.Ul(
                                            [
                                                html.Li("NASA POWER Weather (2021–2025)"),
                                                html.Li("USGS 3DEP 1m DEM"),
                                                html.Li("NRCS SSURGO Soils"),
                                                html.Li("USDA NASS CDL"),
                                                html.Li("OpenStreetMap Field Boundaries"),
                                            ],
                                            className="text-muted small",
                                        ),
                                    ],
                                ),
                            ],
                            className="ga-card p-3 mb-4",
                        ),
                        lg=6,
                    ),
                ],
                className="ga-container",
            ),
        ],
        className="ga-main",
    )
