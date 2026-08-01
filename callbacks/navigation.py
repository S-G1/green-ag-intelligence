"""Navigation callbacks — Page routing, farm selector, add farm, demo mode, command palette, toast."""

from __future__ import annotations

from dash import Input, Output, State, html, ALL, ctx, dcc
from dash.exceptions import PreventUpdate
import dash

from config import DEMO_CONFIG, COMMAND_ACTIONS
from components.nav_rail import NAV_ITEMS


# =============================================================================
# In-memory farm registry (session-scoped, not persisted to disk)
# =============================================================================

_user_farms: dict[str, dict] = {}


def register_navigation_callbacks(app: dash.Dash) -> None:
    """Register all navigation, modal, and workflow callbacks."""
    
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
    # 3. Empty-state banner visibility
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("empty-state-banner", "style"),
        Input("selected-farm-id", "data"),
    )
    def sync_empty_state_banner(farm_id):
        if farm_id:
            return {"display": "none"}
        return {"display": "flex"}
    
    # ─────────────────────────────────────────────────────────────────────────
    # 5. Farm selector backdrop visibility
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("farm-selector-backdrop", "style"),
        Input("farm-selector-open", "data"),
    )
    def sync_farm_selector_backdrop(is_open):
        if is_open:
            return {"display": "block"}
        return {"display": "none"}
    
    # ─────────────────────────────────────────────────────────────────────────
    # 6. Add farm backdrop visibility
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("add-farm-backdrop", "style"),
        Input("add-farm-open", "data"),
    )
    def sync_add_farm_backdrop(is_open):
        if is_open:
            return {"display": "block"}
        return {"display": "none"}
    
    # ─────────────────────────────────────────────────────────────────────────
    # 7. Dashboard primary action buttons
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("farm-selector-open", "data", allow_duplicate=True),
        Output("add-farm-open", "data", allow_duplicate=True),
        Output("demo-store", "data", allow_duplicate=True),
        Output("ndvi-interval", "disabled", allow_duplicate=True),
        Output("btn-ndvi-play", "className", allow_duplicate=True),
        Output("demo-badge", "style", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Output("active-section", "data", allow_duplicate=True),
        Output("selected-farm-id", "data", allow_duplicate=True),
        Output("selected-grower", "data", allow_duplicate=True),
        Output("filter-crop", "value", allow_duplicate=True),
        Output("filter-year", "value", allow_duplicate=True),
        Output("filter-layer", "value", allow_duplicate=True),
        Output("active-map-layer", "data", allow_duplicate=True),
        Input("btn-open-existing-farm", "n_clicks"),
        Input("btn-add-new-farm", "n_clicks"),
        Input("btn-launch-demo-mode", "n_clicks"),
        prevent_initial_call=True,
    )
    def handle_dashboard_actions(open_clicks, add_clicks, demo_clicks):
        triggered = ctx.triggered_id
        no_update = dash.no_update
        
        if triggered == "btn-open-existing-farm" and open_clicks:
            return (True, False, no_update, no_update, no_update, no_update,
                    no_update, no_update, no_update, no_update, no_update,
                    no_update, no_update, no_update)
        
        elif triggered == "btn-add-new-farm" and add_clicks:
            return (False, True, no_update, no_update, no_update, no_update,
                    no_update, no_update, no_update, no_update, no_update,
                    no_update, no_update, no_update)
        
        elif triggered == "btn-launch-demo-mode" and demo_clicks:
            return (False, False, True, False, "ga-ndvi-play-btn playing",
                    {"display": "flex"},
                    "Demo Mode launched using Maryland Final Project Farm",
                    "overview", "md-caroline-farm", "md-grower",
                    "Soybeans", 2025, "risk", "risk")
        
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 8. Farm Selector visibility sync
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("farm-selector-wrapper", "style"),
        Input("farm-selector-open", "data"),
    )
    def sync_farm_selector_visibility(is_open):
        if is_open:
            return {"display": "block"}
        return {"display": "none"}
    
    # ─────────────────────────────────────────────────────────────────────────
    # 9. Farm selection — click a farm item
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("selected-farm-id", "data", allow_duplicate=True),
        Output("selected-grower", "data", allow_duplicate=True),
        Output("btn-open-selected-farm", "disabled"),
        Output("farm-check-md-caroline-farm", "style"),
        Input("farm-item-md-caroline-farm", "n_clicks"),
        prevent_initial_call=True,
    )
    def select_farm(n_clicks):
        if n_clicks:
            return "md-caroline-farm", "md-grower", False, {"display": "block"}
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 10. Open selected farm from farm selector
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("farm-selector-open", "data", allow_duplicate=True),
        Output("selected-grower", "data", allow_duplicate=True),
        Output("selected-farm-id", "data", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Output("active-section", "data", allow_duplicate=True),
        Input("btn-open-selected-farm", "n_clicks"),
        State("selected-farm-id", "data"),
        prevent_initial_call=True,
    )
    def open_selected_farm(n_clicks, farm_id):
        if n_clicks and farm_id:
            return (False, "md-grower", farm_id,
                    f"Opened {farm_id}", "overview")
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 11. Cancel / close farm selector
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("farm-selector-open", "data", allow_duplicate=True),
        Input("btn-cancel-farm-selector", "n_clicks"),
        Input("btn-close-farm-selector", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_farm_selector(cancel_clicks, close_clicks):
        if ctx.triggered:
            return False
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 12. Add New Farm from farm selector
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("farm-selector-open", "data", allow_duplicate=True),
        Output("add-farm-open", "data", allow_duplicate=True),
        Input("btn-add-farm-from-selector", "n_clicks"),
        prevent_initial_call=True,
    )
    def add_farm_from_selector(n_clicks):
        if n_clicks:
            return False, True
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 13. Add Farm modal visibility sync
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("add-farm-wrapper", "style"),
        Input("add-farm-open", "data"),
    )
    def sync_add_farm_visibility(is_open):
        if is_open:
            return {"display": "block"}
        return {"display": "none"}
    
    # ─────────────────────────────────────────────────────────────────────────
    # 14. Add farm form validation
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("add-farm-name-error", "style"),
        Output("add-farm-grower-error", "style"),
        Output("add-farm-state-error", "style"),
        Output("add-farm-county-error", "style"),
        Output("btn-save-farm", "disabled"),
        Output("btn-save-open-farm", "disabled"),
        Input("add-farm-name", "value"),
        Input("add-farm-grower", "value"),
        Input("add-farm-state", "value"),
        Input("add-farm-county", "value"),
    )
    def validate_add_farm(name, grower, state, county):
        errors = {
            "name": not name or len(name.strip()) == 0,
            "grower": not grower or len(grower.strip()) == 0,
            "state": not state or len(state.strip()) == 0,
            "county": not county or len(county.strip()) == 0,
        }
        
        any_error = any(errors.values())
        
        return (
            {"display": "block"} if errors["name"] else {"display": "none"},
            {"display": "block"} if errors["grower"] else {"display": "none"},
            {"display": "block"} if errors["state"] else {"display": "none"},
            {"display": "block"} if errors["county"] else {"display": "none"},
            any_error,
            any_error,
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # 15. Save farm (in-memory)
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("add-farm-open", "data", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Input("btn-save-farm", "n_clicks"),
        State("add-farm-name", "value"),
        State("add-farm-grower", "value"),
        State("add-farm-state", "value"),
        State("add-farm-county", "value"),
        State("add-farm-crop", "value"),
        State("add-farm-year", "value"),
        State("add-farm-notes", "value"),
        prevent_initial_call=True,
    )
    def save_farm(n_clicks, name, grower, state, county, crop, year, notes):
        if not n_clicks:
            raise PreventUpdate
        
        farm_id = f"user-{name.lower().replace(' ', '-')[:20]}"
        _user_farms[farm_id] = {
            "id": farm_id,
            "name": name,
            "grower": grower,
            "state": state,
            "county": county,
            "crop": crop,
            "year": year,
            "notes": notes or "",
        }
        
        return False, f"Farm '{name}' saved successfully"
    
    # ─────────────────────────────────────────────────────────────────────────
    # 16. Save and open farm
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("add-farm-open", "data", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Output("selected-farm-id", "data", allow_duplicate=True),
        Output("selected-grower", "data", allow_duplicate=True),
        Output("active-section", "data", allow_duplicate=True),
        Input("btn-save-open-farm", "n_clicks"),
        State("add-farm-name", "value"),
        State("add-farm-grower", "value"),
        State("add-farm-state", "value"),
        State("add-farm-county", "value"),
        State("add-farm-crop", "value"),
        State("add-farm-year", "value"),
        State("add-farm-notes", "value"),
        prevent_initial_call=True,
    )
    def save_and_open_farm(n_clicks, name, grower, state, county, crop, year, notes):
        if not n_clicks:
            raise PreventUpdate
        
        farm_id = f"user-{name.lower().replace(' ', '-')[:20]}"
        _user_farms[farm_id] = {
            "id": farm_id,
            "name": name,
            "grower": grower,
            "state": state,
            "county": county,
            "crop": crop,
            "year": year,
            "notes": notes or "",
        }
        
        return (False, f"Farm '{name}' saved and opened",
                farm_id, grower, "overview")
    
    # ─────────────────────────────────────────────────────────────────────────
    # 17. Cancel / close add farm
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("add-farm-open", "data", allow_duplicate=True),
        Input("btn-cancel-add-farm", "n_clicks"),
        Input("btn-close-add-farm", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_add_farm(cancel_clicks, close_clicks):
        if ctx.triggered:
            return False
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 18. Add farm file upload validation
    # ─────────────────────────────────────────────────────────────────────────

    @app.callback(
        Output("add-farm-geojson-status", "children"),
        Output("add-farm-file-error", "children"),
        Output("add-farm-file-error", "style"),
        Input("add-farm-upload-geojson", "contents"),
        State("add-farm-upload-geojson", "filename"),
        prevent_initial_call=True,
    )
    def validate_geojson_upload(contents, filename):
        if not contents:
            raise PreventUpdate
        import base64, json, io
        try:
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            data = json.loads(decoded)
            geom_type = data.get("type", "")
            if geom_type not in ("FeatureCollection", "Feature"):
                return (
                    f"❌ {filename}: must be FeatureCollection or Feature",
                    "Invalid GeoJSON type",
                    {"display": "block"},
                )
            features = data.get("features", [data]) if geom_type == "FeatureCollection" else [data]
            if not features:
                return (
                    f"❌ {filename}: no features found",
                    "Empty geometry",
                    {"display": "block"},
                )
            for f in features:
                g = f.get("geometry", {})
                if g.get("type") not in ("Polygon", "MultiPolygon"):
                    return (
                        f"❌ {filename}: features must be Polygon or MultiPolygon",
                        "Invalid geometry type",
                        {"display": "block"},
                    )
            file_size = len(decoded)
            if file_size > 5 * 1024 * 1024:
                return (
                    f"❌ {filename}: exceeds 5 MB limit",
                    "File too large",
                    {"display": "block"},
                )
            return (
                f"✓ {filename} — {len(features)} feature(s), {file_size/1024:.1f} KB",
                "",
                {"display": "none"},
            )
        except Exception as e:
            return (
                f"❌ {filename}: parse error",
                str(e),
                {"display": "block"},
            )

    @app.callback(
        Output("add-farm-shapefile-status", "children"),
        Output("add-farm-file-error", "children", allow_duplicate=True),
        Output("add-farm-file-error", "style", allow_duplicate=True),
        Input("add-farm-upload-shapefile", "contents"),
        State("add-farm-upload-shapefile", "filename"),
        prevent_initial_call=True,
    )
    def validate_shapefile_upload(contents, filename):
        if not contents:
            raise PreventUpdate
        import base64, zipfile, io
        try:
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            file_size = len(decoded)
            if file_size > 10 * 1024 * 1024:
                return (
                    f"❌ {filename}: exceeds 10 MB limit",
                    "File too large",
                    {"display": "block"},
                )
            if not filename.lower().endswith(".zip"):
                return (
                    f"❌ {filename}: must be a .zip archive",
                    "Invalid file type",
                    {"display": "block"},
                )
            with zipfile.ZipFile(io.BytesIO(decoded)) as z:
                names = z.namelist()
                if not any(n.lower().endswith(".shp") for n in names):
                    return (
                        f"❌ {filename}: no .shp file inside archive",
                        "Missing shapefile",
                        {"display": "block"},
                    )
            return (
                f"✓ {filename} — archive valid, {file_size/1024:.1f} KB",
                "",
                {"display": "none"},
            )
        except Exception as e:
            return (
                f"❌ {filename}: parse error",
                str(e),
                {"display": "block"},
            )

    # ─────────────────────────────────────────────────────────────────────────
    # 19. Demo mode exit button
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("demo-badge", "style"),
        Output("demo-store", "data", allow_duplicate=True),
        Output("ndvi-interval", "disabled", allow_duplicate=True),
        Output("btn-ndvi-play", "className", allow_duplicate=True),
        Input("btn-exit-demo", "n_clicks"),
        prevent_initial_call=True,
    )
    def exit_demo_mode(n_clicks):
        if n_clicks:
            return {"display": "none"}, False, True, "ga-ndvi-play-btn"
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 19. Toast notification display
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("toast-overlay", "style"),
        Output("toast-text", "children"),
        Input("toast-message", "data"),
    )
    def display_toast(message):
        if message:
            return {"display": "flex"}, message
        return {"display": "none"}, ""
    
    # ─────────────────────────────────────────────────────────────────────────
    # 20. Dismiss toast
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input("btn-dismiss-toast", "n_clicks"),
        Input("toast-overlay", "n_clicks"),
        prevent_initial_call=True,
    )
    def dismiss_toast(dismiss_clicks, overlay_clicks):
        if ctx.triggered:
            return ""
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 21. Command palette toggle
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("command-palette-overlay", "style"),
        Input("global-search", "n_clicks"),
        Input("command-palette-input", "n_submit"),
        Input("command-palette-overlay", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_command_palette(search_clicks, input_submit, overlay_click):
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered == "global-search" and search_clicks:
            return {"display": "flex"}
        elif triggered in ["command-palette-input", "command-palette-overlay"]:
            return {"display": "none"}
        
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 22. Command palette filtering
    # ─────────────────────────────────────────────────────────────────────────
    @app.callback(
        Output("command-palette-list", "children"),
        Input("command-palette-input", "value"),
    )
    def filter_command_palette(query):
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
    # 23. Command palette actions
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
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"]
        import json
        try:
            id_json = triggered.split(".")[0]
            item_id = json.loads(id_json)["index"]
        except Exception:
            raise PreventUpdate
        
        no_update = dash.no_update
        
        nav_map = {
            "map": "map-explorer",
            "weather": "weather",
            "table": "overview",
            "recommendations": "overview",
            "search": "overview",
        }
        
        if item_id in nav_map:
            return {"display": "none"}, nav_map[item_id], no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "theme":
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "demo":
            return {"display": "none"}, "overview", no_update, True, False, "ga-ndvi-play-btn playing", no_update
        
        elif item_id == "export":
            import pandas as pd
            from data import WEATHER_MONTHLY
            df = pd.DataFrame(WEATHER_MONTHLY)
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, dcc.send_data_frame(df.to_csv, "weather_export.csv", index=False)
        
        elif item_id == "refresh":
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "reset":
            return {"display": "none"}, "overview", no_update, no_update, no_update, no_update, no_update
        
        elif item_id == "help":
            return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
        
        return {"display": "none"}, no_update, no_update, no_update, no_update, no_update, no_update
    
    # ─────────────────────────────────────────────────────────────────────────
    # 24. Nav rail collapse toggle
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
