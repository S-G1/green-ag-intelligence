"""Green Ag Intelligence Platform — Version 2.2 Dashboard-First.

Enterprise Agricultural Intelligence Platform with left navigation.

Deploy: gunicorn app:server
Local: python app.py
"""

from __future__ import annotations

import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from flask import request, send_from_directory

# =============================================================================
# Configuration
# =============================================================================

from config import APP_NAME, APP_TAGLINE

# =============================================================================
# Components
# =============================================================================

from components.nav_rail import create_nav_rail
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
from components.footer import create_footer
from components.map_explorer import create_map_explorer_page
from components.crop_health import create_crop_health_page
from components.weather_page import create_weather_page
from components.soil_terrain import create_soil_terrain_page
from components.farm_management import create_farm_management_page
from components.reports import create_reports_page
from components.settings import create_settings_page
from components.farm_selector import create_farm_selector
from components.add_farm import create_add_farm_modal
from components.toast import create_toast

# =============================================================================
# Callbacks
# =============================================================================

from callbacks.interactions import register_interaction_callbacks
from callbacks.navigation import register_navigation_callbacks
from callbacks.theme import register_theme_callbacks
from callbacks.export import register_export_callbacks
from callbacks.ui_controls import register_ui_control_callbacks

# =============================================================================
# Application Instance
# =============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/custom.css", "/assets/nav_rail.css"],
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
# Report Serving Route
# =============================================================================

RUNTIME_ROOT = os.environ.get(
    "MY_FARM_ADVISOR_RUNTIME",
    os.path.expanduser("~/my-farm-advisor-runtime/data-pipeline"),
)


@server.route("/reports/<path:filename>")
def serve_report(filename: str):
    """Serve farm reports from the runtime directory."""
    safe_name = os.path.basename(filename)
    report_dir = os.path.join(
        RUNTIME_ROOT,
        "growers",
        "md-grower",
        "farms",
        "md-caroline-farm",
        "derived",
        "reports",
    )
    full_path = os.path.join(report_dir, safe_name)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_from_directory(report_dir, safe_name)
    return f"Report not found: {safe_name}", 404


# =============================================================================
# Hidden Stores — Canonical Application State
# =============================================================================

theme_store = dcc.Store(id="theme-store", storage_type="local", data="light")
demo_store = dcc.Store(id="demo-store", storage_type="session", data=False)
selected_field_store = dcc.Store(id="selected-field-store", storage_type="session")
active_section_store = dcc.Store(id="active-section", storage_type="session", data="overview")
nav_collapsed_store = dcc.Store(id="nav-collapsed", storage_type="local", data=False)
farm_selector_open_store = dcc.Store(id="farm-selector-open", storage_type="session", data=False)
add_farm_open_store = dcc.Store(id="add-farm-open", storage_type="session", data=False)
toast_store = dcc.Store(id="toast-message", storage_type="session")
selected_farm_id_store = dcc.Store(id="selected-farm-id", storage_type="session")
selected_grower_store = dcc.Store(id="selected-grower", storage_type="session")
active_map_layer_store = dcc.Store(id="active-map-layer", storage_type="session", data="risk")
active_weather_metric_store = dcc.Store(id="active-weather-metric", storage_type="session", data="combined")

# =============================================================================
# Download Components
# =============================================================================

download_weather = dcc.Download(id="download-weather")
download_fields = dcc.Download(id="download-fields")
download_ndvi = dcc.Download(id="download-ndvi")
download_excel = dcc.Download(id="download-excel")

# =============================================================================
# Overview Page Layout
# =============================================================================

def create_overview_page() -> html.Div:
    """Build the Overview page (Dashboard-first)."""
    return html.Div(
        [
            # KPI Cards (always rendered; update via callbacks)
            html.Div(
                create_kpi_cards(),
                className="ga-container",
                id="kpi-section",
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
        ],
    )


# =============================================================================
# Page Router
# =============================================================================

PAGE_CREATORS = {
    "overview": create_overview_page,
    "map-explorer": create_map_explorer_page,
    "crop-health": create_crop_health_page,
    "weather": create_weather_page,
    "soil-terrain": create_soil_terrain_page,
    "reports": create_reports_page,
    "farm-mgmt": create_farm_management_page,
    "settings": create_settings_page,
}


def create_page(section: str) -> html.Div:
    """Create the page for the given section."""
    creator = PAGE_CREATORS.get(section, create_overview_page)
    return creator()


# =============================================================================
# Main Layout Assembly
# =============================================================================

app.layout = html.Div(
    [
        # Stores
        theme_store,
        demo_store,
        selected_field_store,
        active_section_store,
        nav_collapsed_store,
        farm_selector_open_store,
        add_farm_open_store,
        toast_store,
        selected_farm_id_store,
        selected_grower_store,
        active_map_layer_store,
        active_weather_metric_store,
        
        # Downloads
        download_weather,
        download_fields,
        download_ndvi,
        download_excel,
        
        # Empty-state banner (hidden when farm is selected)
        html.Div(
            [
                html.Div(
                    [
                        html.Span("ℹ️", className="me-2"),
                        html.Strong("No farm selected. "),
                        html.Span("Select an existing farm, add a farm, or launch the Maryland demo."),
                    ],
                    className="ga-empty-state-inner",
                ),
            ],
            id="empty-state-banner",
            className="ga-empty-state-banner",
            style={"display": "flex"},
        ),
        
        # Farm Selector Modal
        create_farm_selector(),
        
        # Add Farm Modal
        create_add_farm_modal(),
        
        # Toast Notification
        create_toast(),
        
        # Command Palette (hidden by default)
        create_command_palette(),
        
        # Mobile overlay for nav
        html.Div(id="mobile-nav-overlay", className="mobile-nav-overlay", style={"display": "none"}),
        
        # Main App Structure
        html.Div(
            [
                # Navigation Rail
                create_nav_rail(collapsed=False),
                
                # Content Area
                html.Div(
                    [
                        # Header
                        create_header(),
                        
                        # Global Search
                        create_global_search(),
                        
                        # Filter Toolbar (includes primary actions)
                        create_filter_toolbar(),
                        
                        # Page Content (switches based on active section)
                        html.Div(
                            id="page-content",
                            children=create_overview_page(),
                        ),
                        
                        # Footer
                        create_footer(),
                    ],
                    className="main-content",
                    id="main-content",
                ),
            ],
            className="app-with-nav",
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
register_ui_control_callbacks(app)

# =============================================================================
# Clientside Callbacks
# =============================================================================

# Ctrl+K keyboard shortcut to open command palette
app.clientside_callback(
    """
    function(id) {
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                var overlay = document.getElementById('command-palette-overlay');
                if (overlay) {
                    overlay.style.display = 'flex';
                    setTimeout(function() {
                        var input = document.getElementById('command-palette-input');
                        if (input) {
                            input.focus();
                            input.value = '';
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    }, 50);
                }
            }
            if (e.key === 'Escape') {
                var overlay = document.getElementById('command-palette-overlay');
                if (overlay && overlay.style.display === 'flex') {
                    overlay.style.display = 'none';
                }
            }
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("ga-root", "data-keyboard"),
    Input("ga-root", "id"),
)

# =============================================================================
# Main Entry
# =============================================================================

if __name__ == "__main__":
    import os
    
    debug = os.environ.get("DASH_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", "8050"))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # Log update-component request bodies for debugging
    @server.before_request
    def log_update_component():
        if request.path == '/_dash-update-component' and request.method == 'POST':
            try:
                body = request.get_data(as_text=True)
                import json, sys
                data = json.loads(body)
                print(f"UPDATE-COMPONENT: output={data.get('output', 'unknown')[:80]}, inputs={data.get('inputs', [])}", file=sys.stderr)
            except Exception as e:
                print(f"UPDATE-COMPONENT: error reading body: {e}", file=sys.stderr)
    
    app.run(debug=debug, host=host, port=port)
