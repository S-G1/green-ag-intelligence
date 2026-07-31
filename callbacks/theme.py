"""Theme callbacks — Light/dark mode toggle with chart updates."""

from __future__ import annotations

from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import dash


def register_theme_callbacks(app: dash.Dash) -> None:
    """Register theme toggle callbacks."""
    
    @app.callback(
        Output("theme-store", "data"),
        Input("btn-theme-toggle", "n_clicks"),
        State("theme-store", "data"),
        prevent_initial_call=True,
    )
    def toggle_theme(n_clicks, current_theme):
        """Toggle between light and dark mode."""
        if n_clicks is None:
            raise PreventUpdate
        
        return "dark" if current_theme == "light" else "light"
    
    @app.callback(
        Output("ga-root", "data-theme"),
        Input("theme-store", "data"),
    )
    def apply_theme(theme):
        """Apply theme to root element."""
        return theme
    
    # ─────────────────────────────────────────────────────────────────────────
    # Theme change → update all chart figures
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("map-graph", "figure", allow_duplicate=True),
        Output("ndvi-chart", "figure", allow_duplicate=True),
        Output("weather-chart", "figure", allow_duplicate=True),
        Output("stress-gauge", "figure", allow_duplicate=True),
        Input("theme-store", "data"),
        State("selected-field-store", "data"),
        State("filter-layer", "value"),
        State("filter-year", "value"),
        prevent_initial_call=True,
    )
    def update_charts_for_theme(theme, selected_field, layer, year):
        """Rebuild all chart figures with the correct theme template."""
        if theme is None:
            raise PreventUpdate
        
        from components.map_component import _build_map_figure
        from components.ndvi_panel import _build_ndvi_bar_chart
        from components.weather_panel import _build_weather_figure
        from components.gauge import create_gauge
        from utils.chart_theme import apply_chart_theme
        
        # Build figures
        map_fig = _build_map_figure(selected_field, layer or "ndvi")
        ndvi_fig = _build_ndvi_bar_chart(selected_field, 6, "value")
        weather_fig = _build_weather_figure(year or 2025, "combined")
        
        # Gauge
        gauge_component = create_gauge(selected_field)
        gauge_fig = None
        for child in gauge_component.children:
            if hasattr(child, "figure"):
                gauge_fig = child.figure
                break
        
        # Apply theme
        apply_chart_theme(map_fig, theme)
        apply_chart_theme(ndvi_fig, theme)
        apply_chart_theme(weather_fig, theme)
        if gauge_fig:
            apply_chart_theme(gauge_fig, theme)
        
        return map_fig, ndvi_fig, weather_fig, gauge_fig or dash.no_update
