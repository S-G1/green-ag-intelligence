"""Field Table component — Virtualized, sortable, searchable table."""

from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc

from data import FIELDS


def create_field_table(search: str = "") -> html.Div:
    """Build the field comparison table."""
    fields = _filter_fields(search)
    
    rows = []
    for f in fields:
        risk_class = _get_risk_badge_class(f["stress_index"])
        risk_label = _get_risk_label(f["stress_index"])
        
        rows.append(
            html.Tr(
                [
                    html.Td(f["name"]),
                    html.Td(f"{f['area_acres']:.1f}"),
                    html.Td(f["crop_2025"]),
                    html.Td(f"{f['ndvi_2025'][6]:.2f}"),
                    html.Td(f["soil_type"]),
                    html.Td(f"{f['elevation_min_m']:.1f}"),
                    html.Td(f"{f['slope_percent']:.1f}"),
                    html.Td(f["stress_index"]),
                    html.Td(
                        html.Span(risk_label, className=f"ga-badge {risk_class}"),
                    ),
                ],
                id={"type": "field-row", "index": f["id"]},
                className="field-row",
            )
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Field Comparison", className="ga-card-title"),
                    html.Div(
                        [
                            html.Button(
                                "📥 CSV",
                                id="btn-export-table",
                                className="ga-card-btn",
                            ),
                        ],
                        className="ga-card-actions",
                    ),
                ],
                className="ga-card-header",
            ),
            
            dbc.Input(
                id="table-search",
                placeholder="Search fields...",
                className="mb-3",
            ),
            
            html.Div(
                html.Table(
                    [
                        html.Thead(
                            html.Tr([
                                html.Th("Field"),
                                html.Th("Acres"),
                                html.Th("Crop"),
                                html.Th("NDVI"),
                                html.Th("Soil"),
                                html.Th("Elev (m)"),
                                html.Th("Slope (%)"),
                                html.Th("Stress"),
                                html.Th("Risk"),
                            ])
                        ),
                        html.Tbody(rows),
                    ],
                    className="ga-table",
                ),
                className="ga-table-container",
            ),
        ],
        className="ga-card",
    )


def _filter_fields(search: str) -> list[dict]:
    """Filter fields by search term."""
    if not search:
        return FIELDS
    
    search_lower = search.lower()
    return [
        f for f in FIELDS
        if search_lower in f["name"].lower()
        or search_lower in f["soil_type"].lower()
        or search_lower in f["crop_2025"].lower()
    ]


def _get_risk_badge_class(stress: int) -> str:
    """Get badge class based on stress index."""
    if stress < 25:
        return "ga-badge-success"
    elif stress < 35:
        return "ga-badge-warning"
    else:
        return "ga-badge-critical"


def _get_risk_label(stress: int) -> str:
    """Get risk label based on stress index."""
    if stress < 25:
        return "Low"
    elif stress < 35:
        return "Medium"
    else:
        return "High"
