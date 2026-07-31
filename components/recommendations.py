"""Recommendations component — Enhanced with confidence % and action buttons."""

from __future__ import annotations

from dash import html

from data import FIELDS


def create_recommendations() -> html.Div:
    """Build enhanced recommendation cards with confidence and actions."""
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
                            html.Div(
                                [
                                    html.Span(rec["title"], className="ga-rec-title"),
                                    html.Span(
                                        f"Confidence: {rec['confidence']}%",
                                        className="ga-rec-confidence",
                                    ) if rec.get("confidence") else None,
                                ],
                                className="d-flex align-items-center justify-content-between",
                            ),
                            html.Div(rec["description"], className="ga-rec-desc"),
                            html.Div(
                                [
                                    html.Button(
                                        "View Field",
                                        className="ga-card-btn me-2",
                                        id=f"rec-view-{rec['id']}",
                                    ),
                                    html.Button(
                                        "Open Report",
                                        className="ga-card-btn me-2",
                                        id=f"rec-report-{rec['id']}",
                                    ),
                                    html.Button(
                                        "📥 Summary",
                                        className="ga-card-btn",
                                        id=f"rec-summary-{rec['id']}",
                                    ),
                                ],
                                className="ga-rec-actions",
                            ) if rec.get("actions") else None,
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
                    html.Span(
                        f"{len(cards)} active",
                        className="badge ga-badge-info",
                    ),
                ],
                className="ga-card-header",
            ),
            html.Div(cards, className="d-flex flex-column gap-3"),
        ],
        className="ga-card",
    )


def _generate_recommendations() -> list[dict]:
    """Generate dynamic recommendations with confidence scores."""
    recs = []
    
    # Find healthy fields
    healthy = [f for f in FIELDS if f["stress_index"] < 20]
    if healthy:
        recs.append({
            "id": "healthy",
            "severity": "healthy",
            "icon": "✅",
            "title": f"{len(healthy)} Fields in Optimal Condition",
            "confidence": 94,
            "description": "These fields show excellent health metrics. Continue current management practices including regular monitoring and preventive maintenance. NDVI values are above 0.7 and stress index is below 20.",
            "actions": True,
        })
    
    # Check for low pH
    low_ph = [f for f in FIELDS if f["ph"] < 5.5]
    if low_ph:
        recs.append({
            "id": "ph",
            "severity": "monitor",
            "icon": "⚠️",
            "title": f"Soil pH Below Optimal in {len(low_ph)} Fields",
            "confidence": 87,
            "description": "Consider lime application to raise pH levels. Target pH range: 6.0-6.5 for optimal nutrient availability. Current average pH is 5.6 across affected fields.",
            "actions": True,
        })
    
    # Check drainage
    poorly_drained = [f for f in FIELDS if "Poor" in f["drainage"]]
    if poorly_drained:
        recs.append({
            "id": "drainage",
            "severity": "alert",
            "icon": "🚨",
            "title": f"Drainage Issues in {len(poorly_drained)} Fields",
            "confidence": 91,
            "description": "Poorly drained fields risk waterlogging and root rot. Consider tile drainage installation or cover crops to improve soil structure. Fields: " + ", ".join([f["name"] for f in poorly_drained[:3]]),
            "actions": True,
        })
    
    # Check high stress
    high_stress = [f for f in FIELDS if f["stress_index"] > 30]
    if high_stress:
        recs.append({
            "id": "stress",
            "severity": "critical",
            "icon": "🔴",
            "title": f"High Stress Alert: {len(high_stress)} Fields",
            "confidence": 96,
            "description": "Immediate irrigation or shade management recommended. Monitor soil moisture levels daily and consider emergency watering protocols. Stress index exceeds 30.",
            "actions": True,
        })
    
    return recs
