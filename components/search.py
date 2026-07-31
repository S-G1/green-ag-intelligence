"""Global Search component — Centered search bar with keyboard shortcut."""

from __future__ import annotations

from dash import html, dcc


def create_global_search() -> html.Div:
    """Build the global search bar."""
    return html.Div(
        [
            html.Div(
                [
                    html.Span("🔍", className="ga-search-icon"),
                    dcc.Input(
                        type="text",
                        placeholder="Search farms, fields, reports, documentation…",
                        id="global-search",
                        className="ga-search-input",
                    ),
                    html.Span("Ctrl K", className="ga-search-shortcut d-none d-md-inline"),
                ],
                className="ga-search",
            ),
        ],
        className="ga-search-container",
    )
