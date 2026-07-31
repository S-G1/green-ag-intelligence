"""Export callbacks — CSV and PDF export functionality."""

from __future__ import annotations

from dash import Input, Output
from dash.exceptions import PreventUpdate
import dash
import pandas as pd

from data import WEATHER_MONTHLY, FIELDS


def register_export_callbacks(app: dash.Dash) -> None:
    """Register export callbacks."""
    
    @app.callback(
        Output("download-weather", "data"),
        Input("btn-export-weather", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_weather(n_clicks):
        """Export weather data as CSV."""
        if n_clicks is None:
            raise PreventUpdate
        
        df = pd.DataFrame(WEATHER_MONTHLY)
        return dash.dcc.send_data_frame(df.to_csv, "weather_data.csv", index=False)
    
    @app.callback(
        Output("download-fields", "data"),
        Input("btn-export-table", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_fields(n_clicks):
        """Export field data as CSV."""
        if n_clicks is None:
            raise PreventUpdate
        
        df = pd.DataFrame([
            {
                "Field": f["name"],
                "Acres": f["area_acres"],
                "Crop": f["crop_2025"],
                "NDVI_July": f["ndvi_2025"][6],
                "Soil_Type": f["soil_type"],
                "Elevation_m": f["elevation_min_m"],
                "Slope_pct": f["slope_percent"],
                "Stress_Index": f["stress_index"],
                "Drainage": f["drainage"],
                "pH": f["ph"],
                "OM_pct": f["om_pct"],
            }
            for f in FIELDS
        ])
        
        return dash.dcc.send_data_frame(df.to_csv, "field_data.csv", index=False)
    
    @app.callback(
        Output("download-ndvi", "data"),
        Input("btn-export-ndvi", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_ndvi(n_clicks):
        """Export NDVI data as CSV."""
        if n_clicks is None:
            raise PreventUpdate
        
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        df = pd.DataFrame([
            {
                "Field": f["name"],
                **{month: ndvi for month, ndvi in zip(months, f["ndvi_2025"])},
            }
            for f in FIELDS
        ])
        
        return dash.dcc.send_data_frame(df.to_csv, "ndvi_data.csv", index=False)
