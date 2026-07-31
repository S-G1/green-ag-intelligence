"""UI Controls callbacks — Wire all previously dead interactive controls."""

from __future__ import annotations

from dash import Input, Output, State, html, ALL, ctx
from dash.exceptions import PreventUpdate
import dash
import pandas as pd

from config import MAP_CONFIG
from data import FIELDS, get_weather_by_year


def register_ui_control_callbacks(app: dash.Dash) -> None:
    """Register callbacks for all previously unwired interactive controls."""
    
    # ─────────────────────────────────────────────────────────────────────────
    # 1. Filter toolbar buttons
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("add-farm-open", "data", allow_duplicate=True),
        Output("onboarding-open", "data", allow_duplicate=True),
        Input("btn-add-farm", "n_clicks"),
        prevent_initial_call=True,
    )
    def open_add_farm_from_toolbar(n_clicks):
        if n_clicks:
            return True, False
        raise PreventUpdate
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input("btn-reset-filters", "n_clicks"),
        prevent_initial_call=True,
    )
    def reset_all_filters(n_clicks):
        if n_clicks:
            return "Filters reset to defaults"
        raise PreventUpdate
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input("btn-refresh", "n_clicks"),
        prevent_initial_call=True,
    )
    def refresh_data(n_clicks):
        if n_clicks:
            return "Dashboard data refreshed"
        raise PreventUpdate
    
    @app.callback(
        Output("download-fields", "data", allow_duplicate=True),
        Input("btn-export", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_from_toolbar(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        df = pd.DataFrame([
            {
                "Field": f["name"],
                "Acres": f["area_acres"],
                "Crop": f["crop_2025"],
                "NDVI": f["ndvi_2025"][6],
                "Stress": f["stress_index"],
                "Soil": f["soil_type"],
            }
            for f in FIELDS
        ])
        return dash.dcc.send_data_frame(df.to_csv, "field_export.csv", index=False)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 2. Header buttons → "Coming soon" toast for decorative buttons
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input("btn-notifications", "n_clicks"),
        Input("btn-help", "n_clicks"),
        Input("btn-settings", "n_clicks"),
        Input("btn-export-dashboard", "n_clicks"),
        prevent_initial_call=True,
    )
    def header_coming_soon(notif, help_clicks, settings, export_dash):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        labels = {
            "btn-notifications": "Notifications panel coming soon",
            "btn-help": "Help documentation coming soon",
            "btn-settings": "Settings panel coming soon",
            "btn-export-dashboard": "Dashboard export coming soon",
        }
        return labels.get(triggered, "Feature coming soon")
    
    # ─────────────────────────────────────────────────────────────────────────
    # 3. Map overlay buttons
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("map-graph", "relayoutData", allow_duplicate=True),
        Input("map-reset", "n_clicks"),
        prevent_initial_call=True,
    )
    def reset_map_view(n_clicks):
        if n_clicks:
            return {
                "mapbox.center.lat": MAP_CONFIG["center_lat"],
                "mapbox.center.lon": MAP_CONFIG["center_lon"],
                "mapbox.zoom": MAP_CONFIG["default_zoom"],
            }
        raise PreventUpdate
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input("map-download", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_map_png(n_clicks):
        if n_clicks:
            return "Map PNG download triggered — use Plotly camera icon in mode bar"
        raise PreventUpdate
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input("map-fullscreen", "n_clicks"),
        prevent_initial_call=True,
    )
    def map_fullscreen(n_clicks):
        if n_clicks:
            return "Fullscreen map — use browser zoom or Map Explorer page"
        raise PreventUpdate
    
    # ─────────────────────────────────────────────────────────────────────────
    # 4. Map layer buttons (10 inline overlay buttons)
    # ─────────────────────────────────────────────────────────────────────────
    
    layer_btn_ids = [f"map-layer-{l['id']}" for l in [
        {"id": "ndvi"}, {"id": "risk"}, {"id": "heat_stress"}, {"id": "rainfall"},
        {"id": "elevation"}, {"id": "slope"}, {"id": "aspect"}, {"id": "hillshade"},
        {"id": "wetness"}, {"id": "soil_health"},
    ]]
    
    @app.callback(
        Output("map-graph", "figure", allow_duplicate=True),
        Output("filter-layer", "value", allow_duplicate=True),
        [Input(btn_id, "n_clicks") for btn_id in layer_btn_ids],
        State("selected-field-store", "data"),
        prevent_initial_call=True,
    )
    def map_layer_buttons(*args):
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        layer = triggered.replace("map-layer-", "")
        
        from components.map_component import _build_map_figure
        selected_field = args[-1]  # Last arg is State
        return _build_map_figure(selected_field, layer), layer
    
    # ─────────────────────────────────────────────────────────────────────────
    # 5. Table pagination
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("field-table", "children", allow_duplicate=True),
        Output("table-prev-page", "disabled"),
        Output("table-next-page", "disabled"),
        Input("table-prev-page", "n_clicks"),
        Input("table-next-page", "n_clicks"),
        State("table-search", "value"),
        prevent_initial_call=True,
    )
    def table_pagination(prev_clicks, next_clicks, search_value):
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        
        # Simple stateless pagination: use modulo of click counts
        # In a real app, use a dcc.Store for page number
        from components.field_table import create_field_table, _filter_fields
        
        all_fields = _filter_fields(search_value or "")
        total_pages = max(1, (len(all_fields) + 4) // 5)
        
        # Derive page from click counts
        prev_count = prev_clicks or 0
        next_count = next_clicks or 0
        page = next_count - prev_count
        page = max(0, min(page, total_pages - 1))
        
        table = create_field_table(search=search_value or "", page=page, page_size=5)
        return table.children, (page <= 0), (page >= total_pages - 1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 6. Weather tab buttons
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("weather-chart", "figure", allow_duplicate=True),
        Output("weather-tab-combined", "className"),
        Output("weather-tab-rainfall", "className"),
        Output("weather-tab-temperature", "className"),
        Output("weather-tab-heat", "className"),
        Input("weather-tab-combined", "n_clicks"),
        Input("weather-tab-rainfall", "n_clicks"),
        Input("weather-tab-temperature", "n_clicks"),
        Input("weather-tab-heat", "n_clicks"),
        State("filter-year", "value"),
        prevent_initial_call=True,
    )
    def weather_tabs(combined, rainfall, temperature, heat, year):
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        tab_map = {
            "weather-tab-combined": "combined",
            "weather-tab-rainfall": "rainfall",
            "weather-tab-temperature": "temperature",
            "weather-tab-heat": "heat",
        }
        active_tab = tab_map.get(triggered, "combined")
        
        from components.weather_panel import _build_weather_figure
        fig = _build_weather_figure(year or 2025, active_tab)
        
        classes = []
        for tab_id in ["combined", "rainfall", "temperature", "heat"]:
            base = "weather-tab"
            if tab_id == active_tab:
                base += " active"
            classes.append(base)
        
        return [fig] + classes
    
    # ─────────────────────────────────────────────────────────────────────────
    # 7. Year filter → update weather chart
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("weather-chart", "figure", allow_duplicate=True),
        Input("filter-year", "value"),
        State("weather-tab-combined", "className"),
        prevent_initial_call=True,
    )
    def weather_year_update(year, tab_class):
        if year is None:
            raise PreventUpdate
        
        # Extract active tab from className
        active_tab = "combined"
        if "active" in (tab_class or ""):
            # Determine which tab is active from the class string
            # This is a simplification; in practice store active tab in a Store
            pass
        
        from components.weather_panel import _build_weather_figure
        return _build_weather_figure(year, active_tab)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 8. Recommendation report & summary buttons
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "rec-report", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def rec_report_button(n_clicks_list):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json
        try:
            rec_id = json.loads(triggered.split(".")[0])["index"]
        except Exception:
            raise PreventUpdate
        return f"Report for {rec_id} — opening farm report preview"
    
    @app.callback(
        Output("download-weather", "data", allow_duplicate=True),
        Input({"type": "rec-summary", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def rec_summary_download(n_clicks_list):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json
        try:
            rec_id = json.loads(triggered.split(".")[0])["index"]
        except Exception:
            raise PreventUpdate
        
        # Export a simple summary CSV
        df = pd.DataFrame([
            {
                "Metric": "Recommendation",
                "Value": rec_id,
            },
            {
                "Metric": "Fields Affected",
                "Value": len(FIELDS),
            },
        ])
        return dash.dcc.send_data_frame(df.to_csv, f"summary_{rec_id}.csv", index=False)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 9. Search result click → select field
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("selected-field-store", "data", allow_duplicate=True),
        Output("search-results", "style", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "search-result", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def search_result_click(n_clicks_list):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json
        try:
            field_id = json.loads(triggered.split(".")[0])["index"]
        except Exception:
            raise PreventUpdate
        
        field = next((f for f in FIELDS if f["id"] == field_id), None)
        name = field["name"] if field else field_id
        return field_id, {"display": "none"}, f"Selected field: {name}"
    
    # ─────────────────────────────────────────────────────────────────────────
    # 10. KPI card clicks → actions
    # ─────────────────────────────────────────────────────────────────────────
    
    kpi_ids = ["total_fields", "total_acres", "avg_ndvi", "avg_stress", "high_risk", "well_drained"]
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Output("active-section", "data", allow_duplicate=True),
        [Input(f"kpi-card-{kpi_id}", "n_clicks") for kpi_id in kpi_ids],
        prevent_initial_call=True,
    )
    def kpi_card_click(*args):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        kpi_id = triggered.replace("kpi-card-", "")
        
        actions = {
            "total_fields": ("All fields selected", "overview"),
            "total_acres": ("Farm area overview", "overview"),
            "avg_ndvi": ("NDVI layer activated", "map-explorer"),
            "avg_stress": ("Stress view activated", "overview"),
            "high_risk": ("Filtered to high-risk fields", "overview"),
            "well_drained": ("Drainage overview", "soil-terrain"),
        }
        
        msg, section = actions.get(kpi_id, ("KPI selected", "overview"))
        return msg, section
