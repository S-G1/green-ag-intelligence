"""Add Farm modal — Create a new farm with text fields only."""

from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc

from data import YEARS, CROPS


def create_add_farm_modal() -> html.Div:
    """Build the Add Farm modal with text fields only."""
    
    return html.Div(
        [
            # Backdrop
            html.Div(
                className="modal-backdrop",
                id="add-farm-backdrop",
            ),
            
            # Modal
            html.Div(
                [
                    html.Div(
                        [
                            # Header
                            html.Div(
                                [
                                    html.H2("Add New Farm", className="modal-title h5 mb-0", id="add-farm-title"),
                                    html.Button(
                                        "✕",
                                        className="modal-close-btn",
                                        id="btn-close-add-farm",
                                        type="button",
                                        **{"aria-label": "Close add farm modal"},
                                    ),
                                ],
                                className="modal-header",
                            ),
                            
                            # Body
                            html.Div(
                                [
                                    # Farm Name
                                    html.Div(
                                        [
                                            dbc.Label("Farm Name *", html_for="add-farm-name", className="fw-medium"),
                                            dbc.Input(
                                                id="add-farm-name",
                                                placeholder="e.g., Willow Creek Farm",
                                                type="text",
                                                maxLength=100,
                                            ),
                                            html.Div(
                                                "Farm name is required",
                                                id="add-farm-name-error",
                                                className="text-danger small mt-1",
                                                style={"display": "none"},
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    
                                    # Grower
                                    html.Div(
                                        [
                                            dbc.Label("Grower *", html_for="add-farm-grower", className="fw-medium"),
                                            dbc.Input(
                                                id="add-farm-grower",
                                                placeholder="e.g., jdoe",
                                                type="text",
                                                value="md-grower",
                                                maxLength=50,
                                            ),
                                            html.Div(
                                                "Grower is required",
                                                id="add-farm-grower-error",
                                                className="text-danger small mt-1",
                                                style={"display": "none"},
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    
                                    # State & County row
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Label("State *", html_for="add-farm-state", className="fw-medium"),
                                                    dbc.Input(
                                                        id="add-farm-state",
                                                        placeholder="e.g., Maryland",
                                                        type="text",
                                                        maxLength=50,
                                                    ),
                                                    html.Div(
                                                        "State is required",
                                                        id="add-farm-state-error",
                                                        className="text-danger small mt-1",
                                                        style={"display": "none"},
                                                    ),
                                                ],
                                                className="flex-grow-1 me-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("County *", html_for="add-farm-county", className="fw-medium"),
                                                    dbc.Input(
                                                        id="add-farm-county",
                                                        placeholder="e.g., Caroline",
                                                        type="text",
                                                        maxLength=50,
                                                    ),
                                                    html.Div(
                                                        "County is required",
                                                        id="add-farm-county-error",
                                                        className="text-danger small mt-1",
                                                        style={"display": "none"},
                                                    ),
                                                ],
                                                className="flex-grow-1",
                                            ),
                                        ],
                                        className="d-flex mb-3",
                                    ),
                                    
                                    # Crop & Year row
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Label("Primary Crop *", html_for="add-farm-crop", className="fw-medium"),
                                                    dbc.Select(
                                                        id="add-farm-crop",
                                                        options=[{"label": c, "value": c} for c in CROPS],
                                                        value="Soybeans",
                                                    ),
                                                ],
                                                className="flex-grow-1 me-2",
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Label("Analysis Year *", html_for="add-farm-year", className="fw-medium"),
                                                    dbc.Select(
                                                        id="add-farm-year",
                                                        options=[{"label": str(y), "value": y} for y in YEARS],
                                                        value=2025,
                                                    ),
                                                ],
                                                className="flex-grow-1",
                                            ),
                                        ],
                                        className="d-flex mb-3",
                                    ),
                                    
                                    # Notes
                                    html.Div(
                                        [
                                            dbc.Label("Notes", html_for="add-farm-notes", className="fw-medium"),
                                            dbc.Textarea(
                                                id="add-farm-notes",
                                                placeholder="Optional notes about this farm...",
                                                rows=3,
                                                maxLength=500,
                                            ),
                                        ],
                                        className="mb-3",
                                    ),

                                    # Boundary Upload
                                    html.Div(
                                        [
                                            dbc.Label("Boundary Sources", className="fw-medium"),
                                            html.Div(
                                                [
                                                    # GeoJSON upload
                                                    dcc.Upload(
                                                        id="add-farm-upload-geojson",
                                                        children=html.Div(
                                                            [
                                                                html.Span("📄", className="me-2"),
                                                                html.Span("Drag & Drop or ", className="text-muted"),
                                                                html.A("Select GeoJSON", className="text-primary"),
                                                            ]
                                                        ),
                                                        style={
                                                            "width": "100%",
                                                            "height": "60px",
                                                            "lineHeight": "60px",
                                                            "borderWidth": "1px",
                                                            "borderStyle": "dashed",
                                                            "borderRadius": "8px",
                                                            "textAlign": "center",
                                                            "marginBottom": "8px",
                                                        },
                                                        multiple=False,
                                                        accept=".geojson,.json",
                                                    ),
                                                    html.Div(
                                                        id="add-farm-geojson-status",
                                                        className="text-muted small mb-2",
                                                    ),

                                                    # Shapefile/ZIP upload
                                                    dcc.Upload(
                                                        id="add-farm-upload-shapefile",
                                                        children=html.Div(
                                                            [
                                                                html.Span("📦", className="me-2"),
                                                                html.Span("Drag & Drop or ", className="text-muted"),
                                                                html.A("Select Zipped Shapefile", className="text-primary"),
                                                            ]
                                                        ),
                                                        style={
                                                            "width": "100%",
                                                            "height": "60px",
                                                            "lineHeight": "60px",
                                                            "borderWidth": "1px",
                                                            "borderStyle": "dashed",
                                                            "borderRadius": "8px",
                                                            "textAlign": "center",
                                                            "marginBottom": "8px",
                                                        },
                                                        multiple=False,
                                                        accept=".zip",
                                                    ),
                                                    html.Div(
                                                        id="add-farm-shapefile-status",
                                                        className="text-muted small mb-2",
                                                    ),

                                                    # File validation error
                                                    html.Div(
                                                        id="add-farm-file-error",
                                                        className="text-danger small mt-1",
                                                        style={"display": "none"},
                                                    ),
                                                ],
                                                className="mt-2",
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                ],
                                className="modal-body",
                            ),
                            
                            # Footer
                            html.Div(
                                [
                                    html.Button(
                                        "Cancel",
                                        id="btn-cancel-add-farm",
                                        className="ga-filter-btn me-2",
                                        type="button",
                                    ),
                                    html.Button(
                                        "Save Farm",
                                        id="btn-save-farm",
                                        className="ga-filter-btn ga-filter-btn-secondary me-2",
                                        type="button",
                                    ),
                                    html.Button(
                                        "Save & Open Dashboard",
                                        id="btn-save-open-farm",
                                        className="ga-filter-btn ga-filter-btn-primary",
                                        type="button",
                                    ),
                                ],
                                className="modal-footer",
                            ),
                        ],
                        className="modal-content",
                        role="dialog",
                        **{"aria-modal": "true", "aria-labelledby": "add-farm-title"},
                    ),
                ],
                className="modal-container modal-lg",
                id="add-farm-overlay",
            ),
        ],
        id="add-farm-wrapper",
        style={"display": "none"},
    )
