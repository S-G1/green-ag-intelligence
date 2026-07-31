"""Command Palette component — Ctrl+K overlay with fuzzy search."""

from __future__ import annotations

from dash import html, dcc

from config import COMMAND_ACTIONS


def create_command_palette() -> html.Div:
    """Build the command palette overlay."""
    actions = []
    for action in COMMAND_ACTIONS:
        actions.append(
            html.Div(
                [
                    html.Div(action["icon"].upper()[:1], className="ga-command-palette-item-icon"),
                    html.Span(action["label"], className="ga-command-palette-item-label"),
                    html.Span(action["shortcut"], className="ga-command-palette-item-shortcut"),
                ],
                className="ga-command-palette-item",
                id={"type": "command-item", "index": action["id"]},
            )
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("🔍", className="ga-search-icon"),
                            dcc.Input(
                                type="text",
                                placeholder="Type a command or search…",
                                id="command-palette-input",
                                className="ga-command-palette-input",
                                autoComplete="off",
                            ),
                        ],
                        className="position-relative",
                    ),
                    html.Div(actions, className="ga-command-palette-list"),
                ],
                className="ga-command-palette",
            ),
        ],
        id="command-palette-overlay",
        className="ga-command-palette-overlay",
        style={"display": "none"},
    )
