"""Interaction callbacks — Connected field selection updates all components."""

from __future__ import annotations

from dash import Input, Output, State, html, ctx
from dash.exceptions import PreventUpdate
import dash

from components.map_component import create_map
from components.ndvi_panel import create_ndvi_panel
from components.weather_panel import create_weather_panel
from components.gauge import create_gauge
from components.field_table import create_field_table
from components.recommendations import create_recommendations


def register_interaction_callbacks(app: dash.Dash) -> None:
    """Register all connected interaction callbacks."""
    
    @app.callback(
        Output("ndvi-chart", "figure", allow_duplicate=True),
        Output("ndvi-slider", "value", allow_duplicate=True),
        Input("ndvi-slider", "value"),
        Input("ndvi-interval", "n_intervals"),
        State("ndvi-interval", "disabled"),
        State("btn-ndvi-play", "className"),
        prevent_initial_call=True,
    )
    def update_ndvi(month, n_intervals, interval_disabled, play_btn_class):
        """Update NDVI chart based on slider or animation."""
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered_id == "ndvi-interval" and not interval_disabled:
            month = (n_intervals % 12)
        elif triggered_id == "ndvi-slider":
            pass
        else:
            raise PreventUpdate
        
        ndvi_panel = create_ndvi_panel(month=month)
        for child in ndvi_panel.children:
            if hasattr(child, 'figure'):
                return child.figure, month
        
        raise PreventUpdate
    
    @app.callback(
        Output("ndvi-interval", "disabled"),
        Output("btn-ndvi-play", "className"),
        Input("btn-ndvi-play", "n_clicks"),
        State("ndvi-interval", "disabled"),
        prevent_initial_call=True,
    )
    def toggle_ndvi_play(n_clicks, currently_disabled):
        """Toggle NDVI play/pause."""
        if n_clicks is None:
            raise PreventUpdate
        
        new_state = not currently_disabled
        btn_class = "ga-ndvi-play-btn" + (" playing" if not new_state else "")
        
        return new_state, btn_class
    
    # ─────────────────────────────────────────────────────────────────────────
    # Table search → rebuild full field table with expanded search fields
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("field-table", "children", allow_duplicate=True),
        Input("table-search", "value"),
        prevent_initial_call=True,
    )
    def update_table_search(search_value):
        """Update table based on search across all visible columns."""
        from components.field_table import _filter_fields
        
        matches = _filter_fields(search_value or "")
        count_text = f"{len(matches)} result{'s' if len(matches) != 1 else ''}"
        clear_visible = bool(search_value)
        
        import sys
        print(f"DEBUG: update_table_search called with search_value={search_value!r}, clear_visible={clear_visible}", file=sys.stderr)
        
        table = create_field_table(search=search_value or "", page=0, page_size=5, clear_visible=clear_visible, result_count=count_text)
        return table.children
    
    @app.callback(
        Output("table-search", "value"),
        Input("table-search-clear", "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_table_search(n_clicks):
        if n_clicks:
            return ""
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # Global Search — filter fields and show dropdown
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("search-results", "children"),
        Output("search-results", "style"),
        Input("global-search-input", "value"),
    )
    def update_search_results(query):
        """Show search results dropdown based on global search input."""
        from data import FIELDS
        
        if not query or len(query) < 2:
            return [], {"display": "none"}
        
        query_lower = query.lower().strip()
        matches = []
        
        for f in FIELDS:
            match = (
                query_lower in f["name"].lower()
                or query_lower in f["id"].lower()
                or query_lower in f["crop_2025"].lower()
                or query_lower in f["soil_type"].lower()
                or query_lower in str(f["stress_index"]).lower()
            )
            if match:
                matches.append(
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span("📍", className="me-2"),
                                    html.Span(f["name"], className="search-result-title"),
                                ],
                                className="d-flex align-items-center",
                            ),
                            html.Div(
                                f"{f['crop_2025']} • {f['area_acres']:.1f} ac • {f['soil_type']} • Stress {f['stress_index']}",
                                className="search-result-meta",
                            ),
                        ],
                        className="search-result-item",
                        id={"type": "search-result", "index": f["id"]},
                    )
                )
        
        if not matches:
            matches.append(
                html.Div(
                    html.Span("No fields found", className="text-muted"),
                    className="search-result-item text-center py-3",
                )
            )
        
        return matches, {"display": "block"}
