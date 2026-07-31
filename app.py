"""Green Ag Intelligence Platform — Version 2.0.

Enterprise Agricultural Intelligence Platform.
Main entry point — assembles all components and registers callbacks.

Deploy: gunicorn app:server
Local: python app.py
"""

from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

# =============================================================================
# Configuration
# =============================================================================

from config import APP_NAME, APP_TAGLINE

# =============================================================================
# Components
# =============================================================================

from components.header import create_header
from components.search import create_global_search
from components.filters import create_filter_toolbar
from components.kpis import create_kpi_cards
from components.map_component import create_map
from components.ndvi_panel import create_ndvi_panel
from components.weather_panel import create_weather_panel
from components.field_table import create_field_table
from components.gauge import create_gauge
from components.recommendations import create_recommendations
from components.command_palette import create_command_palette
from components.onboarding import create_onboarding
from components.footer import create_footer

# =============================================================================
# Callbacks
# =============================================================================

from callbacks.interactions import register_interaction_callbacks
from callbacks.navigation import register_navigation_callbacks
from callbacks.theme import register_theme_callbacks
from callbacks.export import register_export_callbacks

# =============================================================================
# Application Instance
# =============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/custom.css"],
    suppress_callback_exceptions=True,
    title=APP_NAME,
    update_title=f"Loading… | {APP_NAME}",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": APP_TAGLINE},
    ],
)

server = app.server

# =============================================================================
# Hidden Stores
# =============================================================================

theme_store = dcc.Store(id="theme-store", storage_type="local", data="light")
demo_store = dcc.Store(id="demo-store", storage_type="session", data=False)
selected_field_store = dcc.Store(id="selected-field-store", storage_type="session")

# =============================================================================
# Download Components
# =============================================================================

download_weather = dcc.Download(id="download-weather")
download_fields = dcc.Download(id="download-fields")
download_ndvi = dcc.Download(id="download-ndvi")

# =============================================================================
# Layout Assembly
# =============================================================================

app.layout = html.Div(
    [
        # Stores
        theme_store,
        demo_store,
        selected_field_store,
        
        # Downloads
        download_weather,
        download_fields,
        download_ndvi,
        
        # Onboarding (hidden by default)
        create_onboarding(),
        
        # Command Palette (hidden by default)
        create_command_palette(),
        
        # Main Dashboard
        html.Div(
            [
                # Header
                create_header(),
                
                # Global Search
                create_global_search(),
                
                # Filter Toolbar
                create_filter_toolbar(),
                
                # KPI Cards
                html.Div(
                    create_kpi_cards(),
                    className="ga-container",
                ),
                
                # Main Content Grid
                html.Div(
                    [
                        # Row 1: Map + NDVI
                        dbc.Row(
                            [
                                dbc.Col(
                                    create_map(),
                                    lg=8,
                                    className="mb-4",
                                ),
                                dbc.Col(
                                    create_ndvi_panel(),
                                    lg=4,
                                    className="mb-4",
                                ),
                            ],
                            className="ga-container",
                        ),
                        
                        # Row 2: Weather + Field Table
                        dbc.Row(
                            [
                                dbc.Col(
                                    create_weather_panel(),
                                    lg=8,
                                    className="mb-4",
                                ),
                                dbc.Col(
                                    create_field_table(),
                                    lg=4,
                                    className="mb-4",
                                ),
                            ],
                            className="ga-container",
                        ),
                        
                        # Row 3: Gauge + Recommendations
                        dbc.Row(
                            [
                                dbc.Col(
                                    create_gauge(),
                                    lg=4,
                                    className="mb-4",
                                ),
                                dbc.Col(
                                    create_recommendations(),
                                    lg=8,
                                    className="mb-4",
                                ),
                            ],
                            className="ga-container",
                        ),
                    ],
                    className="ga-main",
                ),
                
                # Footer
                create_footer(),
            ],
            className="ga-app",
        ),
    ],
    id="ga-root",
    className="ga-root",
)

# =============================================================================
# Register Callbacks
# =============================================================================

register_interaction_callbacks(app)
register_navigation_callbacks(app)
register_theme_callbacks(app)
register_export_callbacks(app)

# =============================================================================
# Main Entry
# =============================================================================

if __name__ == "__main__":
    import os
    
    debug = os.environ.get("DASH_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", "8050"))
    host = os.environ.get("HOST", "0.0.0.0")
    
    app.run(debug=debug, host=host, port=port)
