"""Navigation callbacks — Page routing, onboarding, demo mode, command palette."""

from __future__ import annotations

from dash import Input, Output, State, html, ALL, ctx
from dash.exceptions import PreventUpdate
import dash

from config import DEMO_CONFIG, COMMAND_ACTIONS
from components.nav_rail import NAV_ITEMS


def register_navigation_callbacks(app: dash.Dash) -> None:
    """Register navigation, routing, demo, and command palette callbacks."""
    
    # ─────────────────────────────────────────────────────────────────────────
    # 1. Nav rail click → update active-section store
    # ─────────────────────────────────────────────────────────────────────────
    nav_ids = [f"nav-{item['id']}" for item in NAV_ITEMS]
    
    @app.callback(
        Output("active-section", "data"),
        [Input(nav_id, "n_clicks") for nav_id in nav_ids],
        prevent_initial_call=True,
    )
    def on_nav_click(*_):
        """Update active section when nav item clicked."""
        if not ctx.triggered:
            raise PreventUpdate
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        section = triggered_id.replace("nav-", "")
        return section
    
    # ─────────────────────────────────────────────────────────────────────────
    # 2. Active-section store → update page content + nav active classes
    # ─────────────────────────────────────────────────────────────────────────
    outputs = [Output("page-content", "children")]
    outputs += [Output(f"nav-{item['id']}", "className") for item in NAV_ITEMS]
    
    @app.callback(
        *outputs,
        Input("active-section", "data"),
    )
    def update_page(section):
        """Switch page content and highlight active nav item."""
        from app import create_page
        
        page = create_page(section)
        
        classes = []
        for item in NAV_ITEMS:
            base = "nav-rail-item"
            if item["id"] == section:
                base += " active"
            classes.append(base)
        
        return [page] + classes
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3. Back to overview button
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("active-section", "data", allow_duplicate=True),
        Input("btn-back-overview", "n_clicks"),
        prevent_initial_call=True,
    )
    def back_to_overview(n_clicks):
        if n_clicks:
            return "overview"
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 4. Onboarding visibility
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("onboarding-overlay", "style"),
        Output("active-section", "data", allow_duplicate=True),
        Input("onboarding-overlay", "style"),
        Input("onboarding-open-farm", "n_clicks"),
        Input("onboarding-add-farm", "n_clicks"),
        Input("onboarding-demo", "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_onboarding(style, open_clicks, add_clicks, demo_clicks):
        """Handle onboarding dialog interactions."""
        if not ctx.triggered:
            return style, dash.no_update
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered in ["onboarding-open-farm", "onboarding-add-farm"]:
            return {"display": "none"}, "overview"
        elif triggered == "onboarding-demo":
            return {"display": "none"}, "overview"
        
        return style, dash.no_update
    
    # ─────────────────────────────────────────────────────────────────────────
    # 5. Demo mode toggle
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("demo-badge", "style"),
        Output("demo-store", "data"),
        Output("ndvi-interval", "disabled", allow_duplicate=True),
        Output("btn-ndvi-play", "className", allow_duplicate=True),
        Input("btn-demo-mode", "n_clicks"),
        Input("onboarding-demo", "n_clicks"),
        Input("btn-exit-demo", "n_clicks"),
        State("demo-store", "data"),
        prevent_initial_call=True,
    )
    def toggle_demo_mode(btn_clicks, onboarding_clicks, exit_clicks, demo_state):
        """Toggle demo mode — starts NDVI animation automatically."""
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered in ["btn-demo-mode", "onboarding-demo"]:
            # Show badge, enable demo, start NDVI animation
            return {"display": "flex"}, True, False, "ga-ndvi-play-btn playing"
        elif triggered == "btn-exit-demo":
            # Hide badge, disable demo, stop animation
            return {"display": "none"}, False, True, "ga-ndvi-play-btn"
        
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 6. Command palette toggle
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("command-palette-overlay", "style"),
        Input("global-search", "n_clicks"),
        Input("command-palette-input", "n_submit"),
        Input("command-palette-overlay", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_command_palette(search_clicks, input_submit, overlay_click):
        """Toggle command palette visibility."""
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered == "global-search":
            return {"display": "flex"}
        elif triggered in ["command-palette-input", "command-palette-overlay"]:
            return {"display": "none"}
        
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 6b. Command palette filtering
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("command-palette-list", "children"),
        Input("command-palette-input", "value"),
    )
    def filter_command_palette(query):
        """Filter command palette items based on input."""
        query = (query or "").lower()
        
        filtered = []
        for action in COMMAND_ACTIONS:
            label = action["label"].lower()
            if not query or query in label:
                filtered.append(
                    html.Div(
                        [
                            html.Div(action["icon"].upper()[:1], className="ga-command-palette-item-icon"),
                            html.Span(action["label"], className="ga-command-palette-item-label"),
                            html.Span(action["shortcut"], className="ga-command-palette-item-shortcut"),
                        ],
                        className="ga-command-palette-item",
                        id={"type": "command-item", "index": action["id"]},
                    )
                )
        
        if not filtered:
            filtered.append(
                html.Div(
                    html.Span("No commands found", className="text-muted"),
                    className="ga-command-palette-item text-center py-3",
                )
            )
        
        return filtered
    
    # ─────────────────────────────────────────────────────────────────────────
    # 7. Command palette actions — execute commands
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("command-palette-overlay", "style", allow_duplicate=True),
        Output("active-section", "data", allow_duplicate=True),
        Output("theme-store", "data", allow_duplicate=True),
        Output("demo-store", "data", allow_duplicate=True),
        Output("ndvi-interval", "disabled", allow_duplicate=True),
        Output("btn-ndvi-play", "className", allow_duplicate=True),
        Output("download-weather", "data", allow_duplicate=True),
        Input({"type": "command-item", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_command_select(n_clicks_list):
        """Handle command palette item selection — execute actual commands."""
        if not ctx.triggered:
            raise PreventUpdate
        
        # Find which item was clicked
        triggered = ctx.triggered[0]["prop_id"]
        # Parse pattern-matching ID
        import json
        # triggered looks like '{"index":"map","type":"command-item"}.n_clicks'
        try:
            id_json = triggered.split(".")[0]
            item_id = json.loads(id_json)["index"]
        except Exception:
            raise PreventUpdate
        
        # Default no-change for most outputs
        no_update = dash.no_update
        
        # Navigation commands
        nav_map = {
            "map": "map-explorer",
            "weather": "weather",
            "table": "overview",  # field table is on overview
            "recommendations": "overview",
            "search": "overview",
        }
        
        if item_id in nav_map:
            return {"display": "none"}, nav_map[item_id], no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "theme":
            # Toggle theme — we need to read current theme, but we can't in this callback
            # Just return light/dark toggle instruction via clientside if needed
            # For now, we'll just close palette and let user use theme button
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "demo":
            # Launch demo mode
            return {"display": "none"}, "overview", no_update, True, False, "ga-ndvi-play-btn playing", no_update
        
        elif item_id == "export":
            # Trigger weather export as example
            import pandas as pd
            from data import WEATHER_MONTHLY
            df = pd.DataFrame(WEATHER_MONTHLY)
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, dash.dcc.send_data_frame(df.to_csv, "weather_export.csv", index=False)
        
        elif item_id == "refresh":
            # Just close palette — refresh is a page reload
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "reset":
            # Close palette, go to overview
            return {"display": "none"}, "overview", no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "help":
            # Go to settings or show help — for now just close
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
        
        # Default: close palette
        return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
    
    # ─────────────────────────────────────────────────────────────────────────
    # 8. Nav rail collapse toggle
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("nav-rail", "className"),
        Output("nav-rail", "style"),
        Output("nav-collapsed", "data"),
        Input("nav-rail-toggle", "n_clicks"),
        State("nav-collapsed", "data"),
        prevent_initial_call=True,
    )
    def toggle_nav_rail(n_clicks, collapsed):
        if n_clicks is None:
            raise PreventUpdate
        
        new_collapsed = not collapsed
        class_name = f"nav-rail {'collapsed' if new_collapsed else ''}"
        width = "72px" if new_collapsed else "240px"
        
        return class_name, {"width": width}, new_collapsed
    
