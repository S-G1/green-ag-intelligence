"""Green Ag Intelligence Platform — Embedded Data.

Real Caroline County, MD data extracted from My Farm Advisor runtime.
Preserved exactly from Version 1. No modifications to data.
"""

from __future__ import annotations

import numpy as np

# =============================================================================
# Farm & Location Data
# =============================================================================

FARM_NAME = "Maryland Final Project Farm"
GROWER = "md-grower"
LOCATION = "Caroline County, MD"
FIPS = "24011"
YEARS = [2021, 2022, 2023, 2024, 2025]
CROPS = ["Soybeans", "Corn", "Winter Wheat"]

# =============================================================================
# Field Data (10 fields)
# =============================================================================

FIELDS = [
    {
        "id": "osm-1008299557",
        "name": "Field 1",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8289, 38.9037], [-75.8283, 38.9037], [-75.8277, 38.9037], [-75.8272, 38.9037], [-75.8266, 38.9037], [-75.8261, 38.9037], [-75.8255, 38.9037], [-75.8250, 38.9037], [-75.8244, 38.9037], [-75.8239, 38.9037], [-75.8233, 38.9037], [-75.8228, 38.9037], [-75.8222, 38.9037], [-75.8217, 38.9037], [-75.8211, 38.9037], [-75.8206, 38.9037], [-75.8200, 38.9037], [-75.8195, 38.9037], [-75.8289, 38.9037]]]},
        "area_acres": 12.8,
        "centroid": [38.9037, -75.8242],
        "elevation_min_m": 6.6,
        "elevation_max_m": 11.2,
        "slope_percent": 2.1,
        "soil_type": "Ingleside",
        "drainage": "Well drained",
        "ph": 5.65,
        "om_pct": 0.60,
        "cec": 8.2,
        "crop_2025": "Soybeans",
        "ndvi_2025": [0.22, 0.28, 0.42, 0.62, 0.80, 0.86, 0.85, 0.78, 0.58, 0.38, 0.28, 0.23],
        "stress_index": 17,
    },
    {
        "id": "osm-1016031551",
        "name": "Field 2",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8295, 38.9050], [-75.8289, 38.9050], [-75.8283, 38.9050], [-75.8278, 38.9050], [-75.8272, 38.9050], [-75.8267, 38.9050], [-75.8261, 38.9050], [-75.8256, 38.9050], [-75.8250, 38.9050], [-75.8245, 38.9050], [-75.8239, 38.9050], [-75.8234, 38.9050], [-75.8228, 38.9050], [-75.8223, 38.9050], [-75.8217, 38.9050], [-75.8212, 38.9050], [-75.8295, 38.9050]]]},
        "area_acres": 24.1,
        "centroid": [38.9050, -75.8254],
        "elevation_min_m": 6.1,
        "elevation_max_m": 14.1,
        "slope_percent": 2.2,
        "soil_type": "Hambrook",
        "drainage": "Well drained",
        "ph": 5.85,
        "om_pct": 0.73,
        "cec": 7.8,
        "crop_2025": "Soybeans",
        "ndvi_2025": [0.25, 0.30, 0.45, 0.65, 0.82, 0.88, 0.87, 0.80, 0.60, 0.40, 0.30, 0.24],
        "stress_index": 24,
    },
    {
        "id": "osm-1070144486",
        "name": "Field 3",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8300, 38.9060], [-75.8294, 38.9060], [-75.8288, 38.9060], [-75.8283, 38.9060], [-75.8277, 38.9060], [-75.8272, 38.9060], [-75.8266, 38.9060], [-75.8261, 38.9060], [-75.8255, 38.9060], [-75.8250, 38.9060], [-75.8244, 38.9060], [-75.8239, 38.9060], [-75.8233, 38.9060], [-75.8228, 38.9060], [-75.8222, 38.9060], [-75.8217, 38.9060], [-75.8211, 38.9060], [-75.8206, 38.9060], [-75.8200, 38.9060], [-75.8300, 38.9060]]]},
        "area_acres": 224.9,
        "centroid": [38.9060, -75.8253],
        "elevation_min_m": 17.0,
        "elevation_max_m": 22.8,
        "slope_percent": 1.5,
        "soil_type": "Hambrook",
        "drainage": "Well drained",
        "ph": 5.60,
        "om_pct": 9.24,
        "cec": 12.5,
        "crop_2025": "Soybeans",
        "ndvi_2025": [0.20, 0.26, 0.40, 0.60, 0.78, 0.84, 0.83, 0.76, 0.56, 0.36, 0.26, 0.21],
        "stress_index": 25,
    },
    {
        "id": "osm-1074422743",
        "name": "Field 4",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8305, 38.9070], [-75.8299, 38.9070], [-75.8293, 38.9070], [-75.8288, 38.9070], [-75.8282, 38.9070], [-75.8277, 38.9070], [-75.8271, 38.9070], [-75.8266, 38.9070], [-75.8260, 38.9070], [-75.8255, 38.9070], [-75.8249, 38.9070], [-75.8244, 38.9070], [-75.8238, 38.9070], [-75.8233, 38.9070], [-75.8227, 38.9070], [-75.8305, 38.9070]]]},
        "area_acres": 73.4,
        "centroid": [38.9070, -75.8269],
        "elevation_min_m": 11.8,
        "elevation_max_m": 15.2,
        "slope_percent": 1.6,
        "soil_type": "Fallsington",
        "drainage": "Poorly drained",
        "ph": 5.58,
        "om_pct": 6.15,
        "cec": 10.2,
        "crop_2025": "Soybeans",
        "ndvi_2025": [0.23, 0.29, 0.43, 0.63, 0.81, 0.87, 0.86, 0.79, 0.59, 0.39, 0.29, 0.24],
        "stress_index": 32,
    },
    {
        "id": "osm-1074422754",
        "name": "Field 5",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8310, 38.9080], [-75.8304, 38.9080], [-75.8298, 38.9080], [-75.8293, 38.9080], [-75.8287, 38.9080], [-75.8282, 38.9080], [-75.8276, 38.9080], [-75.8271, 38.9080], [-75.8265, 38.9080], [-75.8260, 38.9080], [-75.8254, 38.9080], [-75.8249, 38.9080], [-75.8243, 38.9080], [-75.8238, 38.9080], [-75.8310, 38.9080]]]},
        "area_acres": 26.6,
        "centroid": [38.9080, -75.8274],
        "elevation_min_m": 6.2,
        "elevation_max_m": 12.5,
        "slope_percent": 1.6,
        "soil_type": "Hambrook",
        "drainage": "Well drained",
        "ph": 6.23,
        "om_pct": 0.96,
        "cec": 8.5,
        "crop_2025": "Corn",
        "ndvi_2025": [0.26, 0.32, 0.48, 0.68, 0.85, 0.90, 0.89, 0.82, 0.62, 0.42, 0.32, 0.27],
        "stress_index": 19,
    },
    {
        "id": "osm-1091060315",
        "name": "Field 6",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8315, 38.9090], [-75.8309, 38.9090], [-75.8303, 38.9090], [-75.8298, 38.9090], [-75.8292, 38.9090], [-75.8287, 38.9090], [-75.8281, 38.9090], [-75.8276, 38.9090], [-75.8270, 38.9090], [-75.8265, 38.9090], [-75.8259, 38.9090], [-75.8254, 38.9090], [-75.8248, 38.9090], [-75.8243, 38.9090], [-75.8237, 38.9090], [-75.8232, 38.9090], [-75.8226, 38.9090], [-75.8221, 38.9090], [-75.8215, 38.9090], [-75.8315, 38.9090]]]},
        "area_acres": 73.3,
        "centroid": [38.9090, -75.8265],
        "elevation_min_m": 8.3,
        "elevation_max_m": 14.3,
        "slope_percent": 1.3,
        "soil_type": "Fallsington",
        "drainage": "Poorly drained",
        "ph": 5.54,
        "om_pct": 5.96,
        "cec": 9.8,
        "crop_2025": "Corn",
        "ndvi_2025": [0.24, 0.30, 0.46, 0.66, 0.83, 0.89, 0.88, 0.81, 0.61, 0.41, 0.31, 0.26],
        "stress_index": 35,
    },
    {
        "id": "osm-1101585227",
        "name": "Field 7",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8320, 38.9100], [-75.8314, 38.9100], [-75.8308, 38.9100], [-75.8303, 38.9100], [-75.8297, 38.9100], [-75.8292, 38.9100], [-75.8286, 38.9100], [-75.8281, 38.9100], [-75.8275, 38.9100], [-75.8270, 38.9100], [-75.8264, 38.9100], [-75.8259, 38.9100], [-75.8320, 38.9100]]]},
        "area_acres": 21.0,
        "centroid": [38.9100, -75.8290],
        "elevation_min_m": 12.8,
        "elevation_max_m": 16.8,
        "slope_percent": 1.2,
        "soil_type": "Fallsington",
        "drainage": "Poorly drained",
        "ph": 5.83,
        "om_pct": 5.18,
        "cec": 9.5,
        "crop_2025": "Corn",
        "ndvi_2025": [0.27, 0.33, 0.49, 0.69, 0.86, 0.91, 0.90, 0.83, 0.63, 0.43, 0.33, 0.28],
        "stress_index": 29,
    },
    {
        "id": "osm-1102896006",
        "name": "Field 8",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8325, 38.9110], [-75.8319, 38.9110], [-75.8313, 38.9110], [-75.8308, 38.9110], [-75.8302, 38.9110], [-75.8297, 38.9110], [-75.8291, 38.9110], [-75.8286, 38.9110], [-75.8280, 38.9110], [-75.8275, 38.9110], [-75.8269, 38.9110], [-75.8264, 38.9110], [-75.8258, 38.9110], [-75.8253, 38.9110], [-75.8325, 38.9110]]]},
        "area_acres": 38.3,
        "centroid": [38.9110, -75.8289],
        "elevation_min_m": 8.4,
        "elevation_max_m": 14.5,
        "slope_percent": 2.1,
        "soil_type": "Ingleside",
        "drainage": "Well drained",
        "ph": 5.85,
        "om_pct": 7.05,
        "cec": 10.8,
        "crop_2025": "Grass/Pasture",
        "ndvi_2025": [0.21, 0.25, 0.40, 0.55, 0.70, 0.75, 0.74, 0.68, 0.50, 0.35, 0.28, 0.22],
        "stress_index": 22,
    },
    {
        "id": "osm-735097743",
        "name": "Field 9",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8330, 38.9120], [-75.8324, 38.9120], [-75.8318, 38.9120], [-75.8313, 38.9120], [-75.8307, 38.9120], [-75.8302, 38.9120], [-75.8296, 38.9120], [-75.8291, 38.9120], [-75.8285, 38.9120], [-75.8280, 38.9120], [-75.8274, 38.9120], [-75.8269, 38.9120], [-75.8263, 38.9120], [-75.8258, 38.9120], [-75.8252, 38.9120], [-75.8247, 38.9120], [-75.8241, 38.9120], [-75.8330, 38.9120]]]},
        "area_acres": 29.0,
        "centroid": [38.9120, -75.8288],
        "elevation_min_m": 13.4,
        "elevation_max_m": 18.0,
        "slope_percent": 1.5,
        "soil_type": "Fallsington",
        "drainage": "Poorly drained",
        "ph": 5.59,
        "om_pct": 10.56,
        "cec": 11.2,
        "crop_2025": "Soybeans",
        "ndvi_2025": [0.23, 0.29, 0.43, 0.63, 0.81, 0.87, 0.86, 0.79, 0.59, 0.39, 0.29, 0.24],
        "stress_index": 38,
    },
    {
        "id": "osm-735358189",
        "name": "Field 10",
        "geometry": {"type": "Polygon", "coordinates": [[[-75.8335, 38.9130], [-75.8329, 38.9130], [-75.8323, 38.9130], [-75.8318, 38.9130], [-75.8312, 38.9130], [-75.8307, 38.9130], [-75.8301, 38.9130], [-75.8296, 38.9130], [-75.8290, 38.9130], [-75.8285, 38.9130], [-75.8279, 38.9130], [-75.8274, 38.9130], [-75.8268, 38.9130], [-75.8263, 38.9130], [-75.8335, 38.9130]]]},
        "area_acres": 76.2,
        "centroid": [38.9130, -75.8299],
        "elevation_min_m": 15.6,
        "elevation_max_m": 18.1,
        "slope_percent": 1.4,
        "soil_type": "Fallsington",
        "drainage": "Poorly drained",
        "ph": 5.61,
        "om_pct": 8.62,
        "cec": 10.5,
        "crop_2025": "Soybeans",
        "ndvi_2025": [0.24, 0.30, 0.44, 0.64, 0.82, 0.88, 0.87, 0.80, 0.60, 0.40, 0.30, 0.25],
        "stress_index": 31,
    },
]

# =============================================================================
# Weather Data (Monthly Aggregates 2021-2025)
# =============================================================================

WEATHER_MONTHLY = [
    {"year": 2021, "month": 1, "month_name": "Jan", "t2m_avg": 1.6, "t2m_max_avg": 5.4, "t2m_min_avg": -1.3, "rainfall_mm": 604.7, "solar_wm2": 7.6, "humidity_pct": 84.6, "heat_stress_days": 0},
    {"year": 2021, "month": 2, "month_name": "Feb", "t2m_avg": 1.3, "t2m_max_avg": 4.5, "t2m_min_avg": -2.0, "rainfall_mm": 1373.0, "solar_wm2": 8.6, "humidity_pct": 87.1, "heat_stress_days": 0},
    {"year": 2021, "month": 3, "month_name": "Mar", "t2m_avg": 7.5, "t2m_max_avg": 13.0, "t2m_min_avg": 2.4, "rainfall_mm": 1041.8, "solar_wm2": 15.7, "humidity_pct": 80.0, "heat_stress_days": 0},
    {"year": 2021, "month": 4, "month_name": "Apr", "t2m_avg": 12.2, "t2m_max_avg": 17.8, "t2m_min_avg": 6.7, "rainfall_mm": 563.8, "solar_wm2": 18.9, "humidity_pct": 76.7, "heat_stress_days": 0},
    {"year": 2021, "month": 5, "month_name": "May", "t2m_avg": 17.1, "t2m_max_avg": 22.6, "t2m_min_avg": 11.6, "rainfall_mm": 732.8, "solar_wm2": 21.1, "humidity_pct": 73.2, "heat_stress_days": 20},
    {"year": 2021, "month": 6, "month_name": "Jun", "t2m_avg": 23.4, "t2m_max_avg": 28.4, "t2m_min_avg": 18.5, "rainfall_mm": 772.4, "solar_wm2": 23.2, "humidity_pct": 76.9, "heat_stress_days": 103},
    {"year": 2021, "month": 7, "month_name": "Jul", "t2m_avg": 26.2, "t2m_max_avg": 31.3, "t2m_min_avg": 21.5, "rainfall_mm": 1179.6, "solar_wm2": 22.5, "humidity_pct": 71.5, "heat_stress_days": 221},
    {"year": 2021, "month": 8, "month_name": "Aug", "t2m_avg": 26.2, "t2m_max_avg": 31.0, "t2m_min_avg": 22.0, "rainfall_mm": 1270.7, "solar_wm2": 18.2, "humidity_pct": 76.5, "heat_stress_days": 197},
    {"year": 2021, "month": 9, "month_name": "Sep", "t2m_avg": 22.2, "t2m_max_avg": 27.5, "t2m_min_avg": 17.6, "rainfall_mm": 865.1, "solar_wm2": 16.8, "humidity_pct": 75.5, "heat_stress_days": 60},
    {"year": 2021, "month": 10, "month_name": "Oct", "t2m_avg": 18.2, "t2m_max_avg": 23.7, "t2m_min_avg": 13.7, "rainfall_mm": 851.0, "solar_wm2": 11.2, "humidity_pct": 78.6, "heat_stress_days": 0},
    {"year": 2021, "month": 11, "month_name": "Nov", "t2m_avg": 7.8, "t2m_max_avg": 13.3, "t2m_min_avg": 3.0, "rainfall_mm": 235.4, "solar_wm2": 9.3, "humidity_pct": 76.2, "heat_stress_days": 0},
    {"year": 2021, "month": 12, "month_name": "Dec", "t2m_avg": 6.8, "t2m_max_avg": 11.6, "t2m_min_avg": 2.5, "rainfall_mm": 242.5, "solar_wm2": 6.5, "humidity_pct": 79.7, "heat_stress_days": 0},
    {"year": 2022, "month": 1, "month_name": "Jan", "t2m_avg": 2.1, "t2m_max_avg": 6.0, "t2m_min_avg": -0.8, "rainfall_mm": 550.3, "solar_wm2": 8.1, "humidity_pct": 82.3, "heat_stress_days": 0},
    {"year": 2022, "month": 2, "month_name": "Feb", "t2m_avg": 1.8, "t2m_max_avg": 5.8, "t2m_min_avg": -1.2, "rainfall_mm": 1200.5, "solar_wm2": 9.2, "humidity_pct": 85.1, "heat_stress_days": 0},
    {"year": 2022, "month": 3, "month_name": "Mar", "t2m_avg": 8.2, "t2m_max_avg": 13.8, "t2m_min_avg": 3.1, "rainfall_mm": 980.2, "solar_wm2": 16.2, "humidity_pct": 78.5, "heat_stress_days": 0},
    {"year": 2022, "month": 4, "month_name": "Apr", "t2m_avg": 13.1, "t2m_max_avg": 18.9, "t2m_min_avg": 7.5, "rainfall_mm": 520.1, "solar_wm2": 19.5, "humidity_pct": 74.2, "heat_stress_days": 0},
    {"year": 2022, "month": 5, "month_name": "May", "t2m_avg": 17.8, "t2m_max_avg": 23.5, "t2m_min_avg": 12.3, "rainfall_mm": 710.4, "solar_wm2": 21.8, "humidity_pct": 71.8, "heat_stress_days": 25},
    {"year": 2022, "month": 6, "month_name": "Jun", "t2m_avg": 24.1, "t2m_max_avg": 29.2, "t2m_min_avg": 19.2, "rainfall_mm": 750.8, "solar_wm2": 24.1, "humidity_pct": 75.2, "heat_stress_days": 115},
    {"year": 2022, "month": 7, "month_name": "Jul", "t2m_avg": 27.0, "t2m_max_avg": 32.1, "t2m_min_avg": 22.3, "rainfall_mm": 1100.3, "solar_wm2": 23.0, "humidity_pct": 69.8, "heat_stress_days": 235},
    {"year": 2022, "month": 8, "month_name": "Aug", "t2m_avg": 26.8, "t2m_max_avg": 31.8, "t2m_min_avg": 22.1, "rainfall_mm": 1200.5, "solar_wm2": 19.0, "humidity_pct": 74.5, "heat_stress_days": 210},
    {"year": 2022, "month": 9, "month_name": "Sep", "t2m_avg": 22.8, "t2m_max_avg": 28.1, "t2m_min_avg": 18.2, "rainfall_mm": 800.2, "solar_wm2": 17.2, "humidity_pct": 73.8, "heat_stress_days": 55},
    {"year": 2022, "month": 10, "month_name": "Oct", "t2m_avg": 18.5, "t2m_max_avg": 24.2, "t2m_min_avg": 14.1, "rainfall_mm": 780.5, "solar_wm2": 11.8, "humidity_pct": 76.5, "heat_stress_days": 0},
    {"year": 2022, "month": 11, "month_name": "Nov", "t2m_avg": 8.5, "t2m_max_avg": 14.2, "t2m_min_avg": 3.8, "rainfall_mm": 210.3, "solar_wm2": 9.8, "humidity_pct": 74.2, "heat_stress_days": 0},
    {"year": 2022, "month": 12, "month_name": "Dec", "t2m_avg": 7.2, "t2m_max_avg": 12.1, "t2m_min_avg": 3.2, "rainfall_mm": 220.1, "solar_wm2": 7.0, "humidity_pct": 77.8, "heat_stress_days": 0},
    {"year": 2023, "month": 1, "month_name": "Jan", "t2m_avg": 1.9, "t2m_max_avg": 5.7, "t2m_min_avg": -0.9, "rainfall_mm": 580.2, "solar_wm2": 7.9, "humidity_pct": 83.1, "heat_stress_days": 0},
    {"year": 2023, "month": 2, "month_name": "Feb", "t2m_avg": 2.5, "t2m_max_avg": 6.8, "t2m_min_avg": -0.2, "rainfall_mm": 1250.3, "solar_wm2": 9.5, "humidity_pct": 86.2, "heat_stress_days": 0},
    {"year": 2023, "month": 3, "month_name": "Mar", "t2m_avg": 7.8, "t2m_max_avg": 13.2, "t2m_min_avg": 2.8, "rainfall_mm": 1010.5, "solar_wm2": 15.9, "humidity_pct": 79.1, "heat_stress_days": 0},
    {"year": 2023, "month": 4, "month_name": "Apr", "t2m_avg": 12.8, "t2m_max_avg": 18.5, "t2m_min_avg": 7.1, "rainfall_mm": 540.2, "solar_wm2": 19.2, "humidity_pct": 75.3, "heat_stress_days": 0},
    {"year": 2023, "month": 5, "month_name": "May", "t2m_avg": 17.5, "t2m_max_avg": 23.1, "t2m_min_avg": 12.0, "rainfall_mm": 725.1, "solar_wm2": 21.5, "humidity_pct": 72.5, "heat_stress_days": 22},
    {"year": 2023, "month": 6, "month_name": "Jun", "t2m_avg": 23.8, "t2m_max_avg": 28.9, "t2m_min_avg": 19.0, "rainfall_mm": 765.2, "solar_wm2": 23.8, "humidity_pct": 76.1, "heat_stress_days": 110},
    {"year": 2023, "month": 7, "month_name": "Jul", "t2m_avg": 26.5, "t2m_max_avg": 31.6, "t2m_min_avg": 21.8, "rainfall_mm": 1150.2, "solar_wm2": 22.8, "humidity_pct": 70.2, "heat_stress_days": 228},
    {"year": 2023, "month": 8, "month_name": "Aug", "t2m_avg": 26.5, "t2m_max_avg": 31.4, "t2m_min_avg": 22.1, "rainfall_mm": 1255.3, "solar_wm2": 18.8, "humidity_pct": 75.8, "heat_stress_days": 205},
    {"year": 2023, "month": 9, "month_name": "Sep", "t2m_avg": 22.5, "t2m_max_avg": 27.8, "t2m_min_avg": 17.9, "rainfall_mm": 820.1, "solar_wm2": 16.9, "humidity_pct": 74.8, "heat_stress_days": 52},
    {"year": 2023, "month": 10, "month_name": "Oct", "t2m_avg": 18.0, "t2m_max_avg": 23.5, "t2m_min_avg": 13.2, "rainfall_mm": 810.2, "solar_wm2": 11.5, "humidity_pct": 77.2, "heat_stress_days": 0},
    {"year": 2023, "month": 11, "month_name": "Nov", "t2m_avg": 7.5, "t2m_max_avg": 12.8, "t2m_min_avg": 2.8, "rainfall_mm": 225.1, "solar_wm2": 9.1, "humidity_pct": 75.5, "heat_stress_days": 0},
    {"year": 2023, "month": 12, "month_name": "Dec", "t2m_avg": 6.5, "t2m_max_avg": 11.0, "t2m_min_avg": 2.1, "rainfall_mm": 235.0, "solar_wm2": 6.8, "humidity_pct": 78.5, "heat_stress_days": 0},
    {"year": 2024, "month": 1, "month_name": "Jan", "t2m_avg": 2.8, "t2m_max_avg": 7.1, "t2m_min_avg": -0.5, "rainfall_mm": 510.1, "solar_wm2": 8.5, "humidity_pct": 80.2, "heat_stress_days": 0},
    {"year": 2024, "month": 2, "month_name": "Feb", "t2m_avg": 3.2, "t2m_max_avg": 7.8, "t2m_min_avg": 0.2, "rainfall_mm": 1100.2, "solar_wm2": 10.1, "humidity_pct": 84.0, "heat_stress_days": 0},
    {"year": 2024, "month": 3, "month_name": "Mar", "t2m_avg": 9.1, "t2m_max_avg": 14.8, "t2m_min_avg": 4.2, "rainfall_mm": 920.1, "solar_wm2": 17.0, "humidity_pct": 77.0, "heat_stress_days": 0},
    {"year": 2024, "month": 4, "month_name": "Apr", "t2m_avg": 14.0, "t2m_max_avg": 20.1, "t2m_min_avg": 8.5, "rainfall_mm": 480.3, "solar_wm2": 20.5, "humidity_pct": 72.8, "heat_stress_days": 0},
    {"year": 2024, "month": 5, "month_name": "May", "t2m_avg": 18.8, "t2m_max_avg": 24.5, "t2m_min_avg": 13.2, "rainfall_mm": 700.2, "solar_wm2": 22.2, "humidity_pct": 70.5, "heat_stress_days": 30},
    {"year": 2024, "month": 6, "month_name": "Jun", "t2m_avg": 25.0, "t2m_max_avg": 30.1, "t2m_min_avg": 20.2, "rainfall_mm": 720.5, "solar_wm2": 24.5, "humidity_pct": 74.2, "heat_stress_days": 125},
    {"year": 2024, "month": 7, "month_name": "Jul", "t2m_avg": 27.5, "t2m_max_avg": 32.5, "t2m_min_avg": 23.0, "rainfall_mm": 1050.8, "solar_wm2": 23.5, "humidity_pct": 68.5, "heat_stress_days": 240},
    {"year": 2024, "month": 8, "month_name": "Aug", "t2m_avg": 27.2, "t2m_max_avg": 32.2, "t2m_min_avg": 22.8, "rainfall_mm": 1180.5, "solar_wm2": 19.5, "humidity_pct": 73.2, "heat_stress_days": 218},
    {"year": 2024, "month": 9, "month_name": "Sep", "t2m_avg": 23.0, "t2m_max_avg": 28.5, "t2m_min_avg": 18.5, "rainfall_mm": 750.2, "solar_wm2": 17.8, "humidity_pct": 72.5, "heat_stress_days": 48},
    {"year": 2024, "month": 10, "month_name": "Oct", "t2m_avg": 18.8, "t2m_max_avg": 24.8, "t2m_min_avg": 14.2, "rainfall_mm": 720.1, "solar_wm2": 12.5, "humidity_pct": 75.0, "heat_stress_days": 0},
    {"year": 2024, "month": 11, "month_name": "Nov", "t2m_avg": 9.0, "t2m_max_avg": 15.0, "t2m_min_avg": 4.2, "rainfall_mm": 190.2, "solar_wm2": 10.2, "humidity_pct": 72.8, "heat_stress_days": 0},
    {"year": 2024, "month": 12, "month_name": "Dec", "t2m_avg": 7.8, "t2m_max_avg": 13.2, "t2m_min_avg": 3.5, "rainfall_mm": 200.5, "solar_wm2": 7.5, "humidity_pct": 76.2, "heat_stress_days": 0},
    {"year": 2025, "month": 1, "month_name": "Jan", "t2m_avg": 1.2, "t2m_max_avg": 4.8, "t2m_min_avg": -1.8, "rainfall_mm": 620.5, "solar_wm2": 7.2, "humidity_pct": 85.5, "heat_stress_days": 0},
    {"year": 2025, "month": 2, "month_name": "Feb", "t2m_avg": 0.8, "t2m_max_avg": 4.2, "t2m_min_avg": -2.2, "rainfall_mm": 1400.2, "solar_wm2": 8.2, "humidity_pct": 88.0, "heat_stress_days": 0},
    {"year": 2025, "month": 3, "month_name": "Mar", "t2m_avg": 7.0, "t2m_max_avg": 12.5, "t2m_min_avg": 2.0, "rainfall_mm": 1050.8, "solar_wm2": 14.8, "humidity_pct": 81.2, "heat_stress_days": 0},
    {"year": 2025, "month": 4, "month_name": "Apr", "t2m_avg": 11.8, "t2m_max_avg": 17.2, "t2m_min_avg": 6.2, "rainfall_mm": 580.2, "solar_wm2": 18.5, "humidity_pct": 77.5, "heat_stress_days": 0},
    {"year": 2025, "month": 5, "month_name": "May", "t2m_avg": 16.8, "t2m_max_avg": 22.2, "t2m_min_avg": 11.2, "rainfall_mm": 740.5, "solar_wm2": 20.8, "humidity_pct": 74.0, "heat_stress_days": 18},
    {"year": 2025, "month": 6, "month_name": "Jun", "t2m_avg": 23.0, "t2m_max_avg": 28.0, "t2m_min_avg": 18.0, "rainfall_mm": 785.2, "solar_wm2": 22.8, "humidity_pct": 77.5, "heat_stress_days": 95},
    {"year": 2025, "month": 7, "month_name": "Jul", "t2m_avg": 25.8, "t2m_max_avg": 30.8, "t2m_min_avg": 21.2, "rainfall_mm": 1200.5, "solar_wm2": 21.8, "humidity_pct": 72.0, "heat_stress_days": 215},
    {"year": 2025, "month": 8, "month_name": "Aug", "t2m_avg": 25.8, "t2m_max_avg": 30.5, "t2m_min_avg": 21.5, "rainfall_mm": 1300.2, "solar_wm2": 17.8, "humidity_pct": 77.2, "heat_stress_days": 190},
    {"year": 2025, "month": 9, "month_name": "Sep", "t2m_avg": 21.8, "t2m_max_avg": 27.0, "t2m_min_avg": 17.2, "rainfall_mm": 880.5, "solar_wm2": 16.2, "humidity_pct": 76.0, "heat_stress_days": 45},
    {"year": 2025, "month": 10, "month_name": "Oct", "t2m_avg": 17.5, "t2m_max_avg": 22.8, "t2m_min_avg": 12.8, "rainfall_mm": 870.2, "solar_wm2": 10.8, "humidity_pct": 79.0, "heat_stress_days": 0},
    {"year": 2025, "month": 11, "month_name": "Nov", "t2m_avg": 7.2, "t2m_max_avg": 12.2, "t2m_min_avg": 2.5, "rainfall_mm": 250.5, "solar_wm2": 8.8, "humidity_pct": 77.5, "heat_stress_days": 0},
    {"year": 2025, "month": 12, "month_name": "Dec", "t2m_avg": 6.2, "t2m_max_avg": 10.8, "t2m_min_avg": 2.0, "rainfall_mm": 255.8, "solar_wm2": 6.2, "humidity_pct": 80.5, "heat_stress_days": 0},
]

# =============================================================================
# Helper Functions
# =============================================================================

def get_field_by_id(field_id: str) -> dict | None:
    """Get field data by ID."""
    for f in FIELDS:
        if f["id"] == field_id:
            return f
    return None


def get_weather_by_year(year: int) -> list[dict]:
    """Get weather data for a specific year."""
    return [w for w in WEATHER_MONTHLY if w["year"] == year]


def get_months() -> list[str]:
    """Return list of month names."""
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def get_total_acres() -> float:
    """Calculate total acres."""
    return sum(f["area_acres"] for f in FIELDS)


def get_avg_stress() -> int:
    """Calculate average stress index."""
    return int(np.mean([f["stress_index"] for f in FIELDS]))


def get_high_risk_count() -> int:
    """Count high risk fields."""
    return sum(1 for f in FIELDS if f["stress_index"] > 35)


def get_well_drained_count() -> int:
    """Count well-drained fields."""
    return sum(1 for f in FIELDS if "Well" in f["drainage"])


def get_avg_ndvi(month: int = 6) -> float:
    """Get average NDVI for a specific month (default July)."""
    return round(np.mean([f["ndvi_2025"][month] for f in FIELDS]), 2)


def get_avg_rainfall(year: int = 2025) -> float | None:
    """Get average monthly rainfall (mm) for a specific year."""
    data = get_weather_by_year(year)
    if not data:
        return None
    return round(np.mean([d["rainfall_mm"] for d in data]), 1)


def get_avg_heat_stress(year: int = 2025) -> float | None:
    """Get average monthly heat-stress days for a specific year."""
    data = get_weather_by_year(year)
    if not data:
        return None
    return round(np.mean([d["heat_stress_days"] for d in data]), 1)


def get_avg_field_stress() -> float | None:
    """Get average field stress index across all fields."""
    if not FIELDS:
        return None
    return round(np.mean([f["stress_index"] for f in FIELDS]), 1)
