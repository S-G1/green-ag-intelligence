"""Toast notification component — Display transient success/info messages."""

from __future__ import annotations

from dash import html


def create_toast() -> html.Div:
    """Build the toast notification overlay."""
    return html.Div(
        [
            html.Div(
                [
                    html.Span("✓", className="toast-icon me-2"),
                    html.Span(id="toast-text", className="toast-text"),
                    html.Button(
                        "✕",
                        className="toast-close ms-2",
                        id="btn-dismiss-toast",
                        type="button",
                        **{"aria-label": "Dismiss notification"},
                    ),
                ],
                className="toast-inner",
                id="toast-inner",
            ),
        ],
        id="toast-overlay",
        className="toast-overlay",
        style={"display": "none"},
    )
