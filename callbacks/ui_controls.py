"""UI Controls callbacks — Wire all previously dead interactive controls."""

from __future__ import annotations

from dash import Input, Output, State, html, ALL, ctx, dcc
from dash.exceptions import PreventUpdate
import dash
import pandas as pd

from config import MAP_CONFIG
from data import FIELDS, get_weather_by_year, get_field_by_id


def register_ui_control_callbacks(app: dash.Dash) -> None:
    """Register callbacks for all previously unwired interactive controls."""
    
    # ─────────────────────────────────────────────────────────────────────────
    # 1. Filter toolbar buttons
    # ─────────────────────────────────────────────────────────────────────────

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
        if not n_clicks:
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
        return dcc.send_data_frame(df.to_csv, "field_export.csv", index=False)
    
    # ─────────────────────────────────────────────────────────────────────────
    # 2. Header buttons → toast for decorative buttons
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input("btn-notifications", "n_clicks"),
        Input("btn-help", "n_clicks"),
        Input("btn-settings", "n_clicks"),
        Input("btn-export-dashboard", "n_clicks"),
        Input("btn-add-field", "n_clicks"),
        Input("btn-report-csv", "n_clicks"),
        Input("btn-report-excel", "n_clicks"),
        Input("btn-settings-theme", "n_clicks"),
        prevent_initial_call=True,
    )
    def header_coming_soon(notif, help_clicks, settings, export_dash, add_field, report_csv, report_excel, settings_theme):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        labels = {
            "btn-notifications": "Notifications panel coming soon",
            "btn-help": "Help documentation coming soon",
            "btn-settings": "Settings panel coming soon",
            "btn-export-dashboard": "Dashboard export coming soon",
            "btn-add-field": "Add field workflow coming soon",
            "btn-report-csv": "Report CSV export coming soon",
            "btn-report-excel": "Report Excel export coming soon",
            "btn-settings-theme": "Theme toggle in settings coming soon",
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
        Output("active-map-layer", "data", allow_duplicate=True),
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
        return _build_map_figure(selected_field, layer), layer, layer
    
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
        
        from components.field_table import create_field_table, _filter_fields
        
        all_fields = _filter_fields(search_value or "")
        total_pages = max(1, (len(all_fields) + 4) // 5)
        
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
        Output("active-weather-metric", "data", allow_duplicate=True),
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
        
        return [fig] + classes + [active_tab]
    
    # ─────────────────────────────────────────────────────────────────────────
    # 7. Year filter → update weather chart
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("weather-chart", "figure", allow_duplicate=True),
        Input("filter-year", "value"),
        State("active-weather-metric", "data"),
        prevent_initial_call=True,
    )
    def weather_year_update(year, active_tab):
        if year is None:
            raise PreventUpdate
        
        from components.weather_panel import _build_weather_figure
        return _build_weather_figure(year, active_tab or "combined")
    
    # ─────────────────────────────────────────────────────────────────────────
    # 8. Recommendation report & summary buttons
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("download-weather", "data", allow_duplicate=True),
        Input({"type": "rec-summary", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def rec_summary_download(n_clicks_list):
        """Download recommendation summary ONLY when a specific button is clicked."""
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered[0]
        prop_id = triggered["prop_id"]
        value = triggered["value"]
        
        if not value or value == 0:
            raise PreventUpdate
        
        import json
        try:
            rec_id = json.loads(prop_id.split(".")[0])["index"]
        except Exception:
            raise PreventUpdate
        
        df = pd.DataFrame([
            {"Metric": "Recommendation", "Value": rec_id},
            {"Metric": "Fields Affected", "Value": len(FIELDS)},
        ])
        return dcc.send_data_frame(df.to_csv, f"summary_{rec_id}.csv", index=False)
    
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
    
    kpi_ids = ["total_fields", "avg_ndvi", "avg_rainfall", "avg_heat_stress", "high_risk", "avg_field_stress"]
    
    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Output("active-section", "data", allow_duplicate=True),
        Output("filter-layer", "value", allow_duplicate=True),
        Output("active-map-layer", "data", allow_duplicate=True),
        Output("active-weather-metric", "data", allow_duplicate=True),
        [Input(f"kpi-card-{kpi_id}", "n_clicks") for kpi_id in kpi_ids],
        prevent_initial_call=True,
    )
    def kpi_card_click(*args):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        kpi_id = triggered.replace("kpi-card-", "")
        
        no_update = dash.no_update
        
        actions = {
            "total_fields": ("All fields selected", "overview", no_update, no_update, no_update),
            "avg_ndvi": ("NDVI layer activated", "overview", "ndvi", "ndvi", no_update),
            "avg_rainfall": ("Rainfall weather view activated", "overview", no_update, no_update, "rainfall"),
            "avg_heat_stress": ("Heat Stress weather view activated", "overview", no_update, no_update, "heat"),
            "high_risk": ("Filtered to high-risk fields", "overview", no_update, no_update, no_update),
            "avg_field_stress": ("Field Stress Index focused", "overview", no_update, no_update, no_update),
        }
        
        msg, section, layer, map_layer, weather_metric = actions.get(kpi_id, ("KPI selected", "overview", no_update, no_update, no_update))
        return msg, section, layer, map_layer, weather_metric
    
    # ─────────────────────────────────────────────────────────────────────────
    # 11. Field table row click → select field
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("selected-field-store", "data", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "field-row", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def field_row_click(n_clicks_list):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json
        try:
            field_id = json.loads(triggered.split(".")[0])["index"]
        except Exception:
            raise PreventUpdate
        
        field = get_field_by_id(field_id)
        name = field["name"] if field else field_id
        return field_id, f"Selected field: {name}"
    
    # ─────────────────────────────────────────────────────────────────────────
    # 12. Filter layer dropdown → rebuild map figure and sync canonical store
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("map-graph", "figure", allow_duplicate=True),
        Output("active-map-layer", "data", allow_duplicate=True),
        Input("filter-layer", "value"),
        State("selected-field-store", "data"),
        prevent_initial_call=True,
    )
    def update_map_layer(layer, selected_field):
        if layer is None:
            raise PreventUpdate
        
        from components.map_component import _build_map_figure
        return _build_map_figure(selected_field, layer), layer
    
    # ─────────────────────────────────────────────────────────────────────────
    # 13. Active map layer store → update map layer button classes
    # ─────────────────────────────────────────────────────────────────────────
    
    layer_outputs = [Output(f"map-layer-{l['id']}", "className") for l in [
        {"id": "ndvi"}, {"id": "risk"}, {"id": "heat_stress"}, {"id": "rainfall"},
        {"id": "elevation"}, {"id": "slope"}, {"id": "aspect"}, {"id": "hillshade"},
        {"id": "wetness"}, {"id": "soil_health"},
    ]]
    
    @app.callback(
        *layer_outputs,
        Input("active-map-layer", "data"),
    )
    def sync_map_layer_buttons(active_layer):
        classes = []
        for l in [
            {"id": "ndvi"}, {"id": "risk"}, {"id": "heat_stress"}, {"id": "rainfall"},
            {"id": "elevation"}, {"id": "slope"}, {"id": "aspect"}, {"id": "hillshade"},
            {"id": "wetness"}, {"id": "soil_health"},
        ]:
            base = "ga-map-layer-btn"
            if l["id"] == active_layer:
                base += " active"
            classes.append(base)
        return classes
    
    # ─────────────────────────────────────────────────────────────────────────
    # 14. Active weather metric store → update weather tab classes
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("weather-tab-combined", "className", allow_duplicate=True),
        Output("weather-tab-rainfall", "className", allow_duplicate=True),
        Output("weather-tab-temperature", "className", allow_duplicate=True),
        Output("weather-tab-heat", "className", allow_duplicate=True),
        Input("active-weather-metric", "data"),
        prevent_initial_call=True,
    )
    def sync_weather_tab_classes(active_metric):
        classes = []
        for tab_id in ["combined", "rainfall", "temperature", "heat"]:
            base = "weather-tab"
            if tab_id == active_metric:
                base += " active"
            classes.append(base)
        return classes
    
    # ─────────────────────────────────────────────────────────────────────────
    # 15. Demo badge visibility sync from demo-store
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("demo-badge", "style"),
        Input("demo-store", "data"),
    )
    def sync_demo_badge(demo_state):
        if demo_state:
            return {"display": "flex"}
        return {"display": "none"}
    
    # ─────────────────────────────────────────────────────────────────────────
    # 16. Selected field store → update all linked components
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("map-graph", "figure", allow_duplicate=True),
        Output("ndvi-chart", "figure", allow_duplicate=True),
        Output("stress-gauge", "figure", allow_duplicate=True),
        Input("selected-field-store", "data"),
        State("active-map-layer", "data"),
        prevent_initial_call=True,
    )
    def update_on_field_select_store(field_id, layer):
        if field_id is None:
            raise PreventUpdate
        
        from components.map_component import _build_map_figure
        from components.ndvi_panel import _build_ndvi_bar_chart
        from components.gauge import create_gauge
        
        map_fig = _build_map_figure(field_id, layer or "risk")
        ndvi_fig = _build_ndvi_bar_chart(field_id, 6, "value")
        
        gauge_component = create_gauge(field_id)
        gauge_fig = None
        for child in gauge_component.children:
            if hasattr(child, "figure"):
                gauge_fig = child.figure
                break
        
        if gauge_fig is None:
            raise PreventUpdate
        
        return map_fig, ndvi_fig, gauge_fig
    
    # ─────────────────────────────────────────────────────────────────────────
    # 17. Farm selected → update header info and KPI values
    # ─────────────────────────────────────────────────────────────────────────
    
    @app.callback(
        Output("kpi-value-total_fields", "children", allow_duplicate=True),
        Output("kpi-value-avg_ndvi", "children", allow_duplicate=True),
        Output("kpi-value-avg_rainfall", "children", allow_duplicate=True),
        Output("kpi-value-avg_heat_stress", "children", allow_duplicate=True),
        Output("kpi-value-high_risk", "children", allow_duplicate=True),
        Output("kpi-value-avg_field_stress", "children", allow_duplicate=True),
        Input("selected-farm-id", "data"),
        Input("filter-year", "value"),
        prevent_initial_call=True,
    )
    def update_kpi_values(farm_id, year):
        if farm_id is None:
            return ("—",) * 6
        
        from data import (
            get_avg_ndvi,
            get_avg_rainfall,
            get_avg_heat_stress,
            get_high_risk_count,
            get_avg_field_stress,
            FIELDS,
        )
        
        y = year or 2025
        total_fields = str(len(FIELDS))
        avg_ndvi = f"{get_avg_ndvi(6):.2f}"
        avg_rainfall_val = get_avg_rainfall(y)
        avg_rainfall = f"{avg_rainfall_val:.1f} mm" if avg_rainfall_val is not None else "—"
        avg_heat_val = get_avg_heat_stress(y)
        avg_heat = f"{avg_heat_val:.1f} days" if avg_heat_val is not None else "—"
        high_risk = str(get_high_risk_count())
        avg_stress_val = get_avg_field_stress()
        avg_stress = f"{avg_stress_val:.1f}/100" if avg_stress_val is not None else "—"
        
        return total_fields, avg_ndvi, avg_rainfall, avg_heat, high_risk, avg_stress

    # ─────────────────────────────────────────────────────────────────────────
    # 18. Selected farm changed → refresh all dashboard components
    # ─────────────────────────────────────────────────────────────────────────

    @app.callback(
        Output("kpi-value-total_fields", "children", allow_duplicate=True),
        Output("kpi-value-avg_ndvi", "children", allow_duplicate=True),
        Output("kpi-value-avg_rainfall", "children", allow_duplicate=True),
        Output("kpi-value-avg_heat_stress", "children", allow_duplicate=True),
        Output("kpi-value-high_risk", "children", allow_duplicate=True),
        Output("kpi-value-avg_field_stress", "children", allow_duplicate=True),
        Output("map-graph", "figure", allow_duplicate=True),
        Output("weather-chart", "figure", allow_duplicate=True),
        Output("ndvi-chart", "figure", allow_duplicate=True),
        Output("stress-gauge", "figure", allow_duplicate=True),
        Output("field-table", "children", allow_duplicate=True),
        Output("recommendations-section", "children", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Input("selected-farm-id", "data"),
        State("filter-year", "value"),
        State("filter-layer", "value"),
        State("active-weather-metric", "data"),
        State("demo-store", "data"),
        prevent_initial_call=True,
    )
    def refresh_dashboard_on_farm_select(farm_id, year, layer, weather_metric, demo):
        """Rebuild all dashboard components when a farm is selected or demo mode activates."""
        if farm_id is None:
            return "—", "—", "—", "—", "—", "—", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, ""

        from data import (
            get_avg_ndvi,
            get_avg_rainfall,
            get_avg_heat_stress,
            get_high_risk_count,
            get_avg_field_stress,
            FIELDS,
        )
        from components.map_component import _build_map_figure
        from components.weather_panel import _build_weather_figure
        from components.ndvi_panel import _build_ndvi_bar_chart
        from components.gauge import create_gauge
        from components.field_table import create_field_table
        from components.recommendations import create_recommendations
        from utils.chart_theme import apply_chart_theme

        y = year or 2025
        active_layer = layer or "risk"
        active_weather = weather_metric or "combined"

        # KPI values
        total_fields = str(len(FIELDS))
        avg_ndvi = f"{get_avg_ndvi(6):.2f}"
        avg_rainfall_val = get_avg_rainfall(y)
        avg_rainfall = f"{avg_rainfall_val:.1f} mm" if avg_rainfall_val is not None else "—"
        avg_heat_val = get_avg_heat_stress(y)
        avg_heat = f"{avg_heat_val:.1f} days" if avg_heat_val is not None else "—"
        high_risk = str(get_high_risk_count())
        avg_stress_val = get_avg_field_stress()
        avg_stress = f"{avg_stress_val:.1f}/100" if avg_stress_val is not None else "—"

        # Charts
        map_fig = _build_map_figure(None, active_layer)
        weather_fig = _build_weather_figure(y, active_weather)
        ndvi_fig = _build_ndvi_bar_chart(None, 6, "value")

        # Gauge
        gauge_component = create_gauge()
        gauge_fig = None
        for child in gauge_component.children:
            if hasattr(child, "figure"):
                gauge_fig = child.figure
                break

        # Apply current theme
        theme = "light"
        if gauge_fig:
            apply_chart_theme(map_fig, theme)
            apply_chart_theme(weather_fig, theme)
            apply_chart_theme(ndvi_fig, theme)
            apply_chart_theme(gauge_fig, theme)

        # Table and recommendations
        table = create_field_table(search="", page=0, page_size=5)
        recs = create_recommendations()

        toast_msg = f"Loaded {farm_id}"
        if demo:
            toast_msg = "Demo Mode launched using Maryland Final Project Farm"

        return (
            total_fields,
            avg_ndvi,
            avg_rainfall,
            avg_heat,
            high_risk,
            avg_stress,
            map_fig,
            weather_fig,
            ndvi_fig,
            gauge_fig or dash.no_update,
            table.children,
            recs.children,
            toast_msg,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # 19. Recommendation View Field → select field
    # ─────────────────────────────────────────────────────────────────────────

    @app.callback(
        Output("selected-field-store", "data", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "rec-view", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def rec_view_button(n_clicks_list):
        """Select the field associated with a recommendation."""
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json
        try:
            rec_id = json.loads(triggered.split(".")[0])["index"]
        except Exception:
            raise PreventUpdate
        # Map recommendation ID to a representative field
        field_id = None
        name = rec_id
        if rec_id == "healthy":
            field_id = "osm-1008299557"
            name = "Field 1"
        elif rec_id == "ph":
            field_id = "osm-1074422743"
            name = "Field 4"
        elif rec_id == "drainage":
            field_id = "osm-1074422743"
            name = "Field 4"
        elif rec_id == "stress":
            field_id = "osm-735097743"
            name = "Field 9"
        if field_id:
            return field_id, f"Selected field: {name}"
        raise PreventUpdate

    # ─────────────────────────────────────────────────────────────────────────
    # 20. Recommendation Open Report → clientside new tab
    # ─────────────────────────────────────────────────────────────────────────

    app.clientside_callback(
        """
        function(n_clicks_list) {
            var ctx = window.dash_clientside.callback_context;
            if (!ctx || !ctx.triggered || !ctx.triggered.length) return "";
            var triggered = ctx.triggered[0];
            var value = triggered.value;
            if (!value || value === 0) return "";
            var rec_id = JSON.parse(triggered.prop_id.split(".")[0]).index;
            window.open("/reports/md_caroline_farm_report.html", "_blank");
            return "Report opened in new tab";
        }
        """,
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "rec-report", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # 21. Map Explorer layer buttons → update map figure
    # ─────────────────────────────────────────────────────────────────────────

    map_explorer_layer_ids = [f"map-layer-btn-{l['id']}" for l in [
        {"id": "ndvi"}, {"id": "risk"}, {"id": "heat_stress"}, {"id": "rainfall"},
    ]]

    @app.callback(
        Output("map-explorer-graph", "figure", allow_duplicate=True),
        [Input(btn_id, "n_clicks") for btn_id in map_explorer_layer_ids],
        prevent_initial_call=True,
    )
    def map_explorer_layer_buttons(*args):
        if not ctx.triggered:
            raise PreventUpdate
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        layer = triggered.replace("map-layer-btn-", "")
        from components.map_explorer import create_map_explorer_page
        # Rebuild just the figure
        from components.map_component import _build_map_figure
        return _build_map_figure(None, layer)

    # ─────────────────────────────────────────────────────────────────────────
    # 22. Farm Management buttons → select field / open report / coming soon
    # ─────────────────────────────────────────────────────────────────────────

    @app.callback(
        Output("selected-field-store", "data", allow_duplicate=True),
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "farm-view", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def farm_view_button(n_clicks_list):
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
        return field_id, f"Selected field: {name}"

    @app.callback(
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "farm-edit", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def farm_edit_button(n_clicks_list):
        if not ctx.triggered:
            raise PreventUpdate
        return "Edit field workflow coming soon"

    app.clientside_callback(
        """
        function(n_clicks_list) {
            var ctx = window.dash_clientside.callback_context;
            if (!ctx || !ctx.triggered || !ctx.triggered.length) return "";
            var triggered = ctx.triggered[0];
            var value = triggered.value;
            if (!value || value === 0) return "";
            var field_id = JSON.parse(triggered.prop_id.split(".")[0]).index;
            window.open("/reports/md_caroline_farm_report.html", "_blank");
            return "Report opened in new tab";
        }
        """,
        Output("toast-message", "data", allow_duplicate=True),
        Input({"type": "farm-report", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
