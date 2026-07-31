"""Header component — Enterprise header with brand, farm info, actions."""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from config import APP_NAME, APP_SUBTITLE
from data import FARM_NAME, LOCATION


def create_header(is_demo: bool = False) -> html.Header:
    """Build the enterprise header."""
    return html.Header(
        [
            # Brand
            html.Div(
                [
                    html.Div("🌱", className="ga-header-logo"),
                    html.Div(
                        [
                            html.Div(APP_NAME, className="ga-header-title"),
                            html.Div(APP_SUBTITLE, className="ga-header-subtitle d-none d-md-block"),
                        ]
                    ),
                ],
                className="ga-header-brand",
            ),
            
            # Farm Info (center)
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("🏠", className="me-1"),
                            html.Span(FARM_NAME, className="value"),
                        ],
                        className="ga-header-info-item",
                    ),
                    html.Div(
                        [
                            html.Span("📍", className="me-1"),
                            html.Span(LOCATION, className="value"),
                        ],
                        className="ga-header-info-item d-none d-lg-flex",
                    ),
                    html.Div(
                        [
                            html.Span("🌾", className="me-1"),
                            html.Span("Soybeans 2025", className="value"),
                        ],
                        className="ga-header-info-item d-none d-xl-flex",
                    ),
                ],
                className="ga-header-info d-none d-md-flex",
            ),
            
            # Actions
            html.Div(
                [
                    # Demo badge
                    html.Div(
                        [
                            html.Span(className="pulse"),
                            html.Span("Demo Mode"),
                        ],
                        className="ga-demo-badge me-2",
                        id="demo-badge",
                        style={"display": "flex" if is_demo else "none"},
                    ),
                    
                    # Notification bell
                    html.Button(
                        "🔔",
                        id="btn-notifications",
                        className="ga-header-btn",
                        title="Notifications",
                    ),
                    
                    # Theme toggle
                    html.Button(
                        "🌙",
                        id="btn-theme-toggle",
                        className="ga-header-btn",
                        title="Toggle Theme",
                    ),
                    
                    # Help
                    html.Button(
                        "❓",
                        id="btn-help",
                        className="ga-header-btn d-none d-sm-flex",
                        title="Help",
                    ),
                    
                    # Settings
                    html.Button(
                        "⚙️",
                        id="btn-settings",
                        className="ga-header-btn d-none d-sm-flex",
                        title="Settings",
                    ),
                    
                    # Export
                    html.Button(
                        "📥",
                        id="btn-export-dashboard",
                        className="ga-header-btn",
                        title="Export Dashboard",
                    ),
                ],
                className="ga-header-actions",
            ),
        ],
        className="ga-header",
    )
