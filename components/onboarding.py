"""Onboarding component — First-time welcome dialog using dbc.Modal."""

from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from config import APP_NAME, APP_SUBTITLE, ONBOARDING_OPTIONS


def create_onboarding() -> dbc.Modal:
    """Build the onboarding dialog using Bootstrap Modal for proper backdrop management."""
    
    options = []
    for opt in ONBOARDING_OPTIONS:
        desc = (
            "Open existing farm data from your account"
            if opt["id"] == "open-farm" else
            "Create a new farm with field boundaries"
            if opt["id"] == "add-farm" else
            "See the platform in action with demo data"
        )
        options.append(
            html.Button(
                [
                    html.Div(
                        opt["icon"].upper()[:1],
                        className=f"ga-onboarding-option-icon {opt['color']}",
                        **{"aria-hidden": "true"},
                    ),
                    html.Div(
                        [
                            html.Div(opt["label"], className="ga-onboarding-option-title"),
                            html.Div(desc, className="ga-onboarding-option-desc"),
                        ],
                        className="ga-onboarding-option-content",
                    ),
                ],
                className="ga-onboarding-option",
                id=f"onboarding-{opt['id']}",
                type="button",
                **{"aria-label": opt["label"]},
            )
        )
    
    return dbc.Modal(
        [
            dbc.ModalHeader(
                [
                    html.Div("🌱", className="ga-onboarding-logo", **{"aria-hidden": "true"}),
                    html.H1(APP_NAME, className="ga-onboarding-title"),
                    html.P(APP_SUBTITLE, className="ga-onboarding-subtitle"),
                ],
                close_button=False,
                className="border-0 text-center pb-0",
            ),
            dbc.ModalBody(
                html.Div(options, className="ga-onboarding-options"),
                className="pt-0",
            ),
        ],
        id="onboarding-overlay",
        is_open=True,  # Initially open
        backdrop="static",  # Don't close on backdrop click
        keyboard=False,  # Don't close on Escape
        centered=True,
        className="ga-onboarding-modal",
    )
