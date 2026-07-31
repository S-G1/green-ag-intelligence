"""Onboarding component — First-time welcome dialog."""

from __future__ import annotations

from dash import html

from config import APP_NAME, APP_SUBTITLE, ONBOARDING_OPTIONS


def create_onboarding() -> html.Div:
    """Build the onboarding dialog."""
    options = []
    for opt in ONBOARDING_OPTIONS:
        options.append(
            html.Div(
                [
                    html.Div(
                        opt["icon"].upper()[:1],
                        className=f"ga-onboarding-option-icon {opt['color']}",
                    ),
                    html.Div(
                        [
                            html.Div(opt["label"], className="ga-onboarding-option-title"),
                            html.Div(
                                "Open existing farm data from your account",
                                className="ga-onboarding-option-desc",
                            ) if opt["id"] == "open_farm" else
                            html.Div(
                                "Create a new farm with field boundaries",
                                className="ga-onboarding-option-desc",
                            ) if opt["id"] == "add_farm" else
                            html.Div(
                                "See the platform in action with demo data",
                                className="ga-onboarding-option-desc",
                            ),
                        ],
                        className="ga-onboarding-option-content",
                    ),
                ],
                className="ga-onboarding-option",
                id=f"onboarding-{opt['id']}",
            )
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("🌱", className="ga-onboarding-logo"),
                    html.H1(APP_NAME, className="ga-onboarding-title"),
                    html.P(APP_SUBTITLE, className="ga-onboarding-subtitle"),
                    html.Div(options, className="ga-onboarding-options"),
                ],
                className="ga-onboarding",
            ),
        ],
        id="onboarding-overlay",
        className="ga-onboarding-overlay",
        style={"display": "none"},
    )
