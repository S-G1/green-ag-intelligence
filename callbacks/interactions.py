"""Interaction callbacks — Connected field selection updates all components."""

from __future__ import annotations

from dash import Input, Output, State, html
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
    
    # ─────────────────────────────────────────────────────────────────────────
    # Canonical selected field store → update all linked components
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("map-graph", "figure", allow_duplicate=True),
        Output("ndvi-chart", "figure", allow_duplicate=True),
        Output("stress-gauge", "figure", allow_duplicate=True),
        Output("selected-field-store", "data"),
        Input({"type": "search-result", "index": dash.ALL}, "n_clicks"),
        Input({"type": "rec-view", "index": dash.ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def update_on_field_select(search_clicks, rec_clicks):
        """Update all components when a field is selected from search or recommendations."""
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"]
        
        # Extract field ID from pattern-matching ID
        import json
        try:
            id_json = triggered.split(".")[0]
            field_id = json.loads(id_json)["index"]
        except Exception:
            raise PreventUpdate
        
        # Build updated figures
        from components.map_component import _build_map_figure
        from components.ndvi_panel import _build_ndvi_bar_chart
        from components.gauge import create_gauge
        
        map_fig = _build_map_figure(field_id, "ndvi")
        ndvi_fig = _build_ndvi_bar_chart(field_id, 6, "value")
        gauge_component = create_gauge(field_id)
        
        # Extract gauge figure
        gauge_fig = None
        for child in gauge_component.children:
            if hasattr(child, "figure"):
                gauge_fig = child.figure
                break
        
        if gauge_fig is None:
            raise PreventUpdate
        
        return map_fig, ndvi_fig, gauge_fig, field_id
    
    # ─────────────────────────────────────────────────────────────────────────
    # Filter layer dropdown → rebuild map figure directly
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("map-graph", "figure", allow_duplicate=True),
        Input("filter-layer", "value"),
        State("selected-field-store", "data"),
        prevent_initial_call=True,
    )
    def update_map_layer(layer, selected_field):
        """Update map when layer changes."""
        if layer is None:
            raise PreventUpdate
        
        from components.map_component import _build_map_figure
        return _build_map_figure(selected_field, layer)
    
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
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered_id == "ndvi-interval" and not interval_disabled:
            month = (n_intervals % 12)
        elif triggered_id == "ndvi-slider":
            pass  # Use the slider value
        else:
            raise PreventUpdate
        
        ndvi_panel = create_ndvi_panel(month=month)
        # Extract figure
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
        table = create_field_table(search=search_value or "")
        # Return the full table component (it has id="field-table" on outer div)
        # but we only need to update children since Output targets children
        return table.children
    

    
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
        
        query_lower = query.lower()
        matches = []
        
        for f in FIELDS:
            match = (
                query_lower in f["name"].lower()
                or query_lower in f["crop_2025"].lower()
                or query_lower in f["soil_type"].lower()
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
                                f"{f['crop_2025']} • {f['area_acres']:.1f} ac • {f['soil_type']}",
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
