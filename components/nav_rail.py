"""Navigation Rail component — Collapsible left sidebar with 8 sections."""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

NAV_ITEMS = [
    {"id": "overview", "label": "Overview", "icon": "📊", "active": True},
    {"id": "map-explorer", "label": "Map Explorer", "icon": "🗺️", "active": False},
    {"id": "crop-health", "label": "Crop Health", "icon": "🌱", "active": False},
    {"id": "weather", "label": "Weather", "icon": "🌦️", "active": False},
    {"id": "soil-terrain", "label": "Soil & Terrain", "icon": "🌍", "active": False},
    {"id": "reports", "label": "Reports", "icon": "📑", "active": False},
    {"id": "farm-mgmt", "label": "Farm Management", "icon": "🚜", "active": False},
    {"id": "settings", "label": "Settings", "icon": "⚙️", "active": False},
]


def create_nav_rail(collapsed: bool = False) -> html.Div:
    """Build the collapsible left navigation rail."""
    items = []
    for item in NAV_ITEMS:
        items.append(
            html.Div(
                [
                    html.Span(item["icon"], className="nav-rail-icon"),
                    html.Span(item["label"], className="nav-rail-label"),
                ],
                id=f"nav-{item['id']}",
                className=f"nav-rail-item {'active' if item['active'] else ''}",
                **{"data-section": item["id"]},
            )
        )
    
    width = "72px" if collapsed else "240px"
    
    return html.Div(
        [
            # Toggle button
            html.Button(
                "☰" if not collapsed else "→",
                id="nav-rail-toggle",
                className="nav-rail-toggle",
            ),
            
            # Brand (mini)
            html.Div(
                [
                    html.Div("🌱", className="nav-rail-brand-icon") if collapsed else
                    html.Div(
                        [
                            html.Div("🌱", className="nav-rail-brand-icon me-2"),
                            html.Span("Green Ag", className="nav-rail-brand-text"),
                        ],
                        className="d-flex align-items-center",
                    ),
                ],
                className="nav-rail-brand",
            ),
            
            # Divider
            html.Hr(className="nav-rail-divider"),
            
            # Navigation items
            html.Div(items, className="nav-rail-items"),
            
            # Bottom section
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("❓", className="nav-rail-icon"),
                            html.Span("Help", className="nav-rail-label"),
                        ],
                        className="nav-rail-item",
                        id="nav-help",
                    ),
                ],
                className="nav-rail-bottom",
            ),
        ],
        id="nav-rail",
        className=f"nav-rail {'collapsed' if collapsed else ''}",
        style={"width": width},
    )
