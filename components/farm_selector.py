"""Farm Selector modal — Select an existing farm from the runtime dataset."""

from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc

from data import FARM_NAME, GROWER, LOCATION, FIPS, FIELDS


def create_farm_selector() -> html.Div:
    """Build the farm selection modal overlay."""
    
    # Build the single available farm card from embedded data
    farm_card = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("🏠", className="me-2"),
                            html.Span(FARM_NAME, className="fw-bold"),
                        ],
                        className="d-flex align-items-center",
                    ),
                    html.Div(
                        [
                            html.Span("✓", className="text-success fw-bold"),
                        ],
                        className="farm-selector-check",
                        id="farm-check-md-caroline-farm",
                        style={"display": "none"},
                    ),
                ],
                className="d-flex justify-content-between align-items-center",
            ),
            html.Div(
                [
                    html.Span(f"Grower: {GROWER}", className="text-muted small me-3"),
                    html.Span(f"Location: {LOCATION}", className="text-muted small me-3"),
                    html.Span(f"FIPS: {FIPS}", className="text-muted small me-3"),
                    html.Span(f"Fields: {len(FIELDS)}", className="text-muted small"),
                ],
                className="d-flex flex-wrap gap-2 mt-1",
            ),
        ],
        className="farm-selector-item p-3 mb-2 rounded",
        id="farm-item-md-caroline-farm",
        **{"data-farm-id": "md-caroline-farm", "data-grower": GROWER},
    )
    
    return html.Div(
        [
            # Backdrop
            html.Div(
                className="modal-backdrop",
                id="farm-selector-backdrop",
            ),
            
            # Modal
            html.Div(
                [
                    html.Div(
                        [
                            # Header
                            html.Div(
                                [
                                    html.H2("Select Farm", className="modal-title h5 mb-0", id="farm-selector-title"),
                                    html.Button(
                                        "✕",
                                        className="modal-close-btn",
                                        id="btn-close-farm-selector",
                                        type="button",
                                        **{"aria-label": "Close farm selector"},
                                    ),
                                ],
                                className="modal-header",
                            ),
                            
                            # Body
                            html.Div(
                                [
                                    # Search
                                    dbc.Input(
                                        id="farm-selector-search",
                                        placeholder="Search farms...",
                                        className="mb-3",
                                        type="text",
                                    ),
                                    
                                    # Farm list
                                    html.Div(
                                        [farm_card],
                                        id="farm-selector-list",
                                        className="farm-selector-list",
                                    ),
                                    
                                    # Empty state (hidden when farms exist)
                                    html.Div(
                                        [
                                            html.Div("📂", className="fs-1 mb-2"),
                                            html.P("No farms found", className="fw-medium"),
                                            html.P("Get started by adding a new farm or launching demo mode.", className="text-muted small"),
                                        ],
                                        id="farm-selector-empty",
                                        className="text-center py-4",
                                        style={"display": "none"},
                                    ),
                                ],
                                className="modal-body",
                            ),
                            
                            # Footer
                            html.Div(
                                [
                                    html.Button(
                                        "Cancel",
                                        id="btn-cancel-farm-selector",
                                        className="ga-filter-btn me-2",
                                        type="button",
                                    ),
                                    html.Button(
                                        "Add New Farm",
                                        id="btn-add-farm-from-selector",
                                        className="ga-filter-btn ga-filter-btn-secondary me-2",
                                        type="button",
                                    ),
                                    html.Button(
                                        "Open Farm",
                                        id="btn-open-selected-farm",
                                        className="ga-filter-btn ga-filter-btn-primary",
                                        type="button",
                                        disabled=True,
                                    ),
                                ],
                                className="modal-footer",
                            ),
                        ],
                        className="modal-content",
                        role="dialog",
                        **{"aria-modal": "true", "aria-labelledby": "farm-selector-title"},
                    ),
                ],
                className="modal-container",
                id="farm-selector-overlay",
            ),
        ],
        id="farm-selector-wrapper",
        style={"display": "none"},
    )
