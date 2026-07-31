"""Global Search component — Centered search bar with keyboard shortcut."""

from __future__ import annotations

from dash import html, dcc


def create_global_search() -> html.Div:
    """Build the global search bar with results dropdown."""
    return html.Div(
        [
            html.Div(
                [
                    html.Span("🔍", className="ga-search-icon"),
                    dcc.Input(
                        type="text",
                        placeholder="Search farms, fields, reports, documentation…",
                        id="global-search-input",
                        className="ga-search-input",
                        autoComplete="off",
                    ),
                    html.Span("Ctrl K", className="ga-search-shortcut d-none d-md-inline"),
                ],
                id="global-search",
                className="ga-search",
                style={"cursor": "pointer"},
            ),
            html.Div(
                id="search-results",
                className="search-results-dropdown",
                style={"display": "none"},
            ),
        ],
        className="ga-search-container position-relative",
    )
