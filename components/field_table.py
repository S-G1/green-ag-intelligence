"""Field Table component — Enhanced with pagination, search, clear, count, no-results."""

from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc

from data import FIELDS


def create_field_table(search: str = "", page: int = 0, page_size: int = 5, clear_visible: bool = False, result_count: str = "") -> html.Div:
    """Build the enhanced field comparison table."""
    all_fields = _filter_fields(search)
    total_pages = max(1, (len(all_fields) + page_size - 1) // page_size)
    page = min(page, total_pages - 1)
    
    start = page * page_size
    end = start + page_size
    fields_page = all_fields[start:end]
    
    rows = []
    for f in fields_page:
        risk_class = _get_risk_badge_class(f["stress_index"])
        risk_label = _get_risk_label(f["stress_index"])
        priority = _get_priority(f["stress_index"])
        
        rows.append(
            html.Tr(
                [
                    html.Td(f["name"]),
                    html.Td(f["crop_2025"]),
                    html.Td(f"{f['area_acres']:.1f}"),
                    html.Td(f"{f['ndvi_2025'][6]:.2f}"),
                    html.Td(f"{f['elevation_min_m']:.1f}"),
                    html.Td(f"{f['slope_percent']:.1f}"),
                    html.Td(f["stress_index"]),
                    html.Td(
                        html.Span(risk_label, className=f"ga-badge {risk_class}"),
                    ),
                    html.Td(priority),
                    html.Td(_get_recommendation_text(f)),
                ],
                id={"type": "field-row", "index": f["id"]},
                className="field-row",
            )
        )
    
    # No-results state
    if not rows:
        rows.append(
            html.Tr(
                [
                    html.Td(
                        html.Div(
                            [
                                html.Div("🔍", className="fs-4 mb-2 text-muted"),
                                html.Div("No fields match your search", className="text-muted"),
                            ],
                            className="text-center py-4",
                        ),
                        colSpan=10,
                    ),
                ]
            )
        )
    
    # Pagination controls
    pagination = html.Div(
        [
            html.Button(
                "← Prev",
                id="table-prev-page",
                className="ga-card-btn me-2",
                disabled=(page <= 0),
            ),
            html.Span(
                f"Page {page + 1} of {total_pages} ({len(all_fields)} fields)",
                className="text-muted mx-2",
                style={"fontSize": "0.75rem"},
            ),
            html.Button(
                "Next →",
                id="table-next-page",
                className="ga-card-btn ms-2",
                disabled=(page >= total_pages - 1),
            ),
        ],
        className="d-flex align-items-center justify-content-between mt-3",
    )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Field Comparison", className="ga-card-title"),
                    html.Div(
                        [
                            html.Button(
                                "📊 Excel",
                                id="btn-export-excel",
                                className="ga-card-btn",
                            ),
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
            
            html.Div(
                [
                    dbc.Input(
                        id="table-search",
                        placeholder="Search fields...",
                        className="mb-2",
                        value=search,
                    ),
                    html.Div(
                        [
                            html.Span(result_count or f"{len(all_fields)} fields", className="text-muted small me-2", id="table-result-count"),
                            html.Button(
                                "Clear",
                                id="table-search-clear",
                                className="ga-card-btn",
                                style={"display": "inline-block" if clear_visible else "none"},
                            ),
                        ],
                        className="d-flex align-items-center mb-2",
                    ),
                ]
            ),
            
            html.Div(
                html.Table(
                    [
                        html.Thead(
                            html.Tr([
                                html.Th("Field"),
                                html.Th("Crop"),
                                html.Th("Acres"),
                                html.Th("NDVI"),
                                html.Th("Elev (m)"),
                                html.Th("Slope (%)"),
                                html.Th("Stress"),
                                html.Th("Risk"),
                                html.Th("Priority"),
                                html.Th("Recommendation"),
                            ])
                        ),
                        html.Tbody(rows),
                    ],
                    className="ga-table",
                ),
                className="ga-table-container",
            ),
            
            pagination,
        ],
        className="ga-card",
        id="field-table",
    )


def _filter_fields(search: str) -> list[dict]:
    """Filter fields by search term across all relevant columns."""
    if not search:
        return FIELDS
    
    search_lower = search.lower().strip()
    results = []
    
    for f in FIELDS:
        rec = _get_recommendation_text(f).lower()
        risk = _get_risk_label(f["stress_index"]).lower()
        priority = _get_priority(f["stress_index"]).lower()
        
        match = (
            search_lower in f["name"].lower()
            or search_lower in f["id"].lower()
            or search_lower in f["soil_type"].lower()
            or search_lower in f["crop_2025"].lower()
            or search_lower in rec
            or search_lower in risk
            or search_lower in priority
            or search_lower in str(f["stress_index"]).lower()
            or search_lower in str(f["area_acres"]).lower()
        )
        if match:
            results.append(f)
    
    return results


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


def _get_priority(stress: int) -> str:
    """Get priority level based on stress."""
    if stress < 25:
        return "Low"
    elif stress < 35:
        return "Medium"
    else:
        return "High"


def _get_recommendation_text(f: dict) -> str:
    """Get recommendation text for a field."""
    if f["stress_index"] > 35:
        return "Scout immediately"
    elif f["stress_index"] > 25:
        return "Monitor weekly"
    elif "Poor" in f["drainage"]:
        return "Check drainage"
    elif f["ph"] < 5.5:
        return "Test soil pH"
    else:
        return "Continue current"
