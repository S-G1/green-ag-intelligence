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
    
    @app.callback(
        Output("map-graph", "figure"),
        Output("ndvi-chart", "figure"),
        Output("stress-gauge", "figure"),
        Output("field-table", "children"),
        Output("recommendations-section", "children"),
        Input("field-table", "n_clicks"),
        State("field-table", "children"),
        prevent_initial_call=True,
    )
    def update_on_field_select(n_clicks, table_children):
        """Update all components when a field is selected."""
        if n_clicks is None:
            raise PreventUpdate
        
        # Extract selected field ID from click context
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        # For now, return no update - actual field selection needs more complex logic
        raise PreventUpdate
    
    @app.callback(
        Output("map-graph", "figure", allow_duplicate=True),
        Input("filter-layer", "value"),
        prevent_initial_call=True,
    )
    def update_map_layer(layer):
        """Update map when layer changes."""
        if layer is None:
            raise PreventUpdate
        
        map_component = create_map(layer=layer)
        # Extract figure from the component
        for child in map_component.children:
            if hasattr(child, 'figure'):
                return child.figure
        
        raise PreventUpdate
    
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
    
    @app.callback(
        Output("field-table", "children", allow_duplicate=True),
        Input("table-search", "value"),
        prevent_initial_call=True,
    )
    def update_table_search(search_value):
        """Update table based on search."""
        table = create_field_table(search=search_value or "")
        # Return the table content (excluding the header)
        for child in table.children:
            if isinstance(child, html.Div) and child.className == "ga-table-container":
                return child
        
        raise PreventUpdate
    
    @app.callback(
        Output("stress-gauge", "figure", allow_duplicate=True),
        Input("filter-field", "value"),
        prevent_initial_call=True,
    )
    def update_gauge_field(field_id):
        """Update gauge when field selection changes."""
        if field_id is None:
            raise PreventUpdate
        
        gauge = create_gauge(field_id=field_id)
        for child in gauge.children:
            if hasattr(child, 'figure'):
                return child.figure
        
        raise PreventUpdate
