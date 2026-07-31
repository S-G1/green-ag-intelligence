"""Navigation callbacks — Onboarding, demo mode, command palette."""

from __future__ import annotations

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
import dash

from config import DEMO_CONFIG


def register_navigation_callbacks(app: dash.Dash) -> None:
    """Register navigation and demo callbacks."""
    
    # Onboarding visibility
    @app.callback(
        Output("onboarding-overlay", "style"),
        Input("onboarding-overlay", "style"),
        Input("onboarding-open-farm", "n_clicks"),
        Input("onboarding-add-farm", "n_clicks"),
        Input("onboarding-demo", "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_onboarding(style, open_clicks, add_clicks, demo_clicks):
        """Handle onboarding dialog interactions."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return style
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered in ["onboarding-open-farm", "onboarding-add-farm", "onboarding-demo"]:
            return {"display": "none"}
        
        return style
    
    # Demo mode toggle
    @app.callback(
        Output("demo-badge", "style"),
        Output("demo-store", "data"),
        Input("btn-demo-mode", "n_clicks"),
        Input("onboarding-demo", "n_clicks"),
        Input("btn-exit-demo", "n_clicks"),
        State("demo-store", "data"),
        prevent_initial_call=True,
    )
    def toggle_demo_mode(btn_clicks, onboarding_clicks, exit_clicks, demo_state):
        """Toggle demo mode."""
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered in ["btn-demo-mode", "onboarding-demo"]:
            return {"display": "flex"}, True
        elif triggered == "btn-exit-demo":
            return {"display": "none"}, False
        
        raise PreventUpdate
    
    # Command palette toggle
    @app.callback(
        Output("command-palette-overlay", "style"),
        Input("command-palette-overlay", "style"),
        Input("global-search", "n_clicks"),
        Input("command-palette-input", "n_submit"),
        Input("command-palette-overlay", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_command_palette(style, search_clicks, input_submit, overlay_click):
        """Toggle command palette visibility."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return style
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered == "global-search":
            return {"display": "flex"}
        elif triggered in ["command-palette-input", "command-palette-overlay"]:
            return {"display": "none"}
        
        return style
    
    # Command palette actions
    @app.callback(
        Output("command-palette-overlay", "style", allow_duplicate=True),
        Input({"type": "command-item", "index": dash.ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_command_select(n_clicks):
        """Handle command palette item selection."""
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        # Close palette after selection
        return {"display": "none"}
