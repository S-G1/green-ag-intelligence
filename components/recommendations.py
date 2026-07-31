"""Recommendations component — Severity cards with icons and actions."""

from __future__ import annotations

from dash import html

from data import FIELDS


def create_recommendations() -> html.Div:
    """Build the recommendations section."""
    recs = _generate_recommendations()
    
    cards = []
    for rec in recs:
        cards.append(
            html.Div(
                [
                    html.Div(
                        rec["icon"],
                        className="ga-rec-icon",
                    ),
                    html.Div(
                        [
                            html.Div(rec["title"], className="ga-rec-title"),
                            html.Div(rec["description"], className="ga-rec-desc"),
                            html.Div(
                                html.Button(
                                    rec["action"],
                                    className="ga-card-btn ga-rec-action",
                                ),
                                className="ga-rec-action",
                            ) if rec.get("action") else None,
                        ],
                        className="ga-rec-content",
                    ),
                ],
                className=f"ga-rec-card {rec['severity']}",
            )
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Recommendations", className="ga-card-title"),
                ],
                className="ga-card-header",
            ),
            html.Div(cards, className="d-flex flex-column gap-3"),
        ],
        className="ga-card",
    )


def _generate_recommendations() -> list[dict]:
    """Generate dynamic recommendations based on field data."""
    recs = []
    
    # Find healthy fields
    healthy = [f for f in FIELDS if f["stress_index"] < 20]
    if healthy:
        recs.append({
            "severity": "healthy",
            "icon": "✅",
            "title": f"{len(healthy)} Fields in Optimal Condition",
            "description": "These fields show excellent health metrics. Continue current management practices including regular monitoring and preventive maintenance.",
            "action": "View Details",
        })
    
    # Check for low pH
    low_ph = [f for f in FIELDS if f["ph"] < 5.5]
    if low_ph:
        recs.append({
            "severity": "monitor",
            "icon": "⚠️",
            "title": f"Soil pH Below Optimal in {len(low_ph)} Fields",
            "description": "Consider lime application to raise pH levels. Target pH range: 6.0-6.5 for optimal nutrient availability.",
            "action": "Schedule Test",
        })
    
    # Check drainage
    poorly_drained = [f for f in FIELDS if "Poor" in f["drainage"]]
    if poorly_drained:
        recs.append({
            "severity": "alert",
            "icon": "🚨",
            "title": f"Drainage Issues in {len(poorly_drained)} Fields",
            "description": "Poorly drained fields risk waterlogging and root rot. Consider tile drainage installation or cover crops to improve soil structure.",
            "action": "View Plan",
        })
    
    # Check high stress
    high_stress = [f for f in FIELDS if f["stress_index"] > 30]
    if high_stress:
        recs.append({
            "severity": "critical",
            "icon": "🔴",
            "title": f"High Stress Alert: {len(high_stress)} Fields",
            "description": "Immediate irrigation or shade management recommended. Monitor soil moisture levels daily and consider emergency watering protocols.",
            "action": "Take Action",
        })
    
    return recs
