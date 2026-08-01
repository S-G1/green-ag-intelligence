"""Export callbacks — CSV, Excel, and PDF export functionality."""

from __future__ import annotations

from dash import Input, Output, dcc
from dash.exceptions import PreventUpdate
import pandas as pd

from data import WEATHER_MONTHLY, FIELDS


def register_export_callbacks(app) -> None:
    """Register export callbacks."""
    
    @app.callback(
        Output("download-weather", "data", allow_duplicate=True),
        Input("btn-export-weather", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_weather(n_clicks):
        """Export weather data as CSV."""
        if not n_clicks:
            raise PreventUpdate
        
        df = pd.DataFrame(WEATHER_MONTHLY)
        return dcc.send_data_frame(df.to_csv, "weather_data.csv", index=False)
    
    @app.callback(
        Output("download-fields", "data", allow_duplicate=True),
        Input("btn-export-table", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_fields(n_clicks):
        """Export field data as CSV."""
        if not n_clicks:
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
        
        return dcc.send_data_frame(df.to_csv, "field_data.csv", index=False)
    
    @app.callback(
        Output("download-excel", "data", allow_duplicate=True),
        Input("btn-export-excel", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_excel(n_clicks):
        """Export field data as Excel file with multiple sheets."""
        if not n_clicks:
            raise PreventUpdate
        
        output = "/tmp/green_ag_data.xlsx"
        
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            fields_df = pd.DataFrame([
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
                    "CEC": f["cec"],
                }
                for f in FIELDS
            ])
            fields_df.to_excel(writer, sheet_name="Fields", index=False)
            
            weather_df = pd.DataFrame(WEATHER_MONTHLY)
            weather_df.to_excel(writer, sheet_name="Weather", index=False)
            
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            ndvi_df = pd.DataFrame([
                {
                    "Field": f["name"],
                    **{month: ndvi for month, ndvi in zip(months, f["ndvi_2025"])},
                }
                for f in FIELDS
            ])
            ndvi_df.to_excel(writer, sheet_name="NDVI", index=False)
        
        return dcc.send_file(output, filename="green_ag_data.xlsx")
