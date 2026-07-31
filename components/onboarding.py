"""Onboarding component — First-time welcome dialog with accessible buttons."""

from __future__ import annotations

from dash import html

from config import APP_NAME, APP_SUBTITLE, ONBOARDING_OPTIONS


def create_onboarding() -> html.Div:
    """Build the onboarding dialog with accessible button options."""
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
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("🌱", className="ga-onboarding-logo", **{"aria-hidden": "true"}),
                    html.H1(APP_NAME, className="ga-onboarding-title"),
                    html.P(APP_SUBTITLE, className="ga-onboarding-subtitle"),
                    html.Div(options, className="ga-onboarding-options"),
                ],
                className="ga-onboarding",
                **{"role": "dialog", "aria-modal": "true", "aria-labelledby": "onboarding-title"},
            ),
        ],
        id="onboarding-overlay",
        className="ga-onboarding-overlay",
        style={"display": "flex"},
    )
