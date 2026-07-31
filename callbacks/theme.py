"""Theme callbacks — Light/dark mode toggle."""

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
