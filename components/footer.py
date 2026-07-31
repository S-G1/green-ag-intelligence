"""Footer component — Professional footer with data sources and links."""

from __future__ import annotations

from dash import html

from config import APP_NAME, APP_VERSION


def create_footer() -> html.Footer:
    """Build the professional footer."""
    return html.Footer(
        [
            html.Div(
                [
                    html.Span(f"{APP_NAME} v{APP_VERSION}"),
                    html.Span("•", className="mx-2"),
                    html.Span("Caroline County, MD"),
                    html.Span("•", className="mx-2"),
                    html.Span("Real data: NASA POWER, USGS 3DEP, SSURGO, CDL"),
                ],
                className="ga-footer-left",
            ),
            html.Div(
                [
                    html.A("Documentation", href="#", className="ga-footer-link"),
                    html.A("API", href="#", className="ga-footer-link"),
                    html.A("Privacy", href="#", className="ga-footer-link"),
                    html.A("Terms", href="#", className="ga-footer-link"),
                ],
                className="ga-footer-right",
            ),
        ],
        className="ga-footer",
    )
