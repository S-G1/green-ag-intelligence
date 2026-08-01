"""Green Ag Intelligence Platform — Configuration & Design Tokens.

All design constants, color tokens, spacing, typography, and breakpoints.
"""

from __future__ import annotations

# =============================================================================
# Application Info
# =============================================================================

APP_NAME = "Green Ag Intelligence Platform"
APP_SUBTITLE = "Environmental Risk Monitoring & Decision Support"
APP_TAGLINE = "Precision Agriculture Decision Support System"
APP_VERSION = "2.0.0"

# =============================================================================
# Brand Colors
# =============================================================================

COLORS = {
    # Primary
    "forest_green": "#1B5E20",
    "leaf_green": "#4CAF50",
    "primary_light": "#81C784",
    "primary_dark": "#0D3B10",
    
    # Secondary
    "deep_blue": "#1565C0",
    "ocean_blue": "#42A5F5",
    "sky_blue": "#90CAF9",
    
    # Semantic
    "success": "#2E7D32",
    "success_light": "#E8F5E9",
    "warning": "#F57F17",
    "warning_light": "#FFF3E0",
    "critical": "#C62828",
    "critical_light": "#FFEBEE",
    "info": "#0288D1",
    "info_light": "#E1F5FE",
    
    # Neutral
    "white": "#FFFFFF",
    "gray_50": "#FAFAFA",
    "gray_100": "#F5F5F5",
    "gray_200": "#EEEEEE",
    "gray_300": "#E0E0E0",
    "gray_400": "#BDBDBD",
    "gray_500": "#9E9E9E",
    "gray_600": "#757575",
    "gray_700": "#616161",
    "gray_800": "#424242",
    "gray_900": "#212121",
    "black": "#000000",
    
    # Dark Mode
    "slate": "#263238",
    "slate_light": "#37474F",
    "slate_lighter": "#455A64",
    "dark_bg": "#1C1C1C",
    "dark_card": "#2D2D2D",
    "dark_border": "#404040",
    "dark_text": "#E0E0E0",
    "dark_text_secondary": "#A0A0A0",
}

# =============================================================================
# Light Theme Tokens
# =============================================================================

LIGHT_THEME = {
    "bg_primary": COLORS["gray_50"],
    "bg_secondary": COLORS["gray_100"],
    "bg_card": COLORS["white"],
    "bg_hover": COLORS["gray_50"],
    "text_primary": COLORS["gray_900"],
    "text_secondary": COLORS["gray_600"],
    "text_muted": COLORS["gray_500"],
    "border": COLORS["gray_300"],
    "border_light": COLORS["gray_200"],
    "shadow": "rgba(0, 0, 0, 0.08)",
    "shadow_strong": "rgba(0, 0, 0, 0.12)",
    "accent": COLORS["forest_green"],
    "accent_light": COLORS["leaf_green"],
}

# =============================================================================
# Dark Theme Tokens
# =============================================================================

DARK_THEME = {
    "bg_primary": COLORS["dark_bg"],
    "bg_secondary": COLORS["slate"],
    "bg_card": COLORS["dark_card"],
    "bg_hover": COLORS["slate_light"],
    "text_primary": COLORS["dark_text"],
    "text_secondary": COLORS["dark_text_secondary"],
    "text_muted": COLORS["gray_500"],
    "border": COLORS["dark_border"],
    "border_light": COLORS["slate_lighter"],
    "shadow": "rgba(0, 0, 0, 0.3)",
    "shadow_strong": "rgba(0, 0, 0, 0.5)",
    "accent": COLORS["leaf_green"],
    "accent_light": COLORS["primary_light"],
}

# =============================================================================
# Typography Scale
# =============================================================================

TYPOGRAPHY = {
    "display": {"size": "1.75rem", "weight": "700", "line_height": "1.2"},
    "h1": {"size": "1.5rem", "weight": "600", "line_height": "1.3"},
    "h2": {"size": "1.25rem", "weight": "600", "line_height": "1.35"},
    "h3": {"size": "1.125rem", "weight": "600", "line_height": "1.4"},
    "body": {"size": "0.875rem", "weight": "400", "line_height": "1.5"},
    "body_sm": {"size": "0.8125rem", "weight": "400", "line_height": "1.5"},
    "caption": {"size": "0.75rem", "weight": "400", "line_height": "1.4"},
    "overline": {"size": "0.6875rem", "weight": "600", "line_height": "1.4", "letter_spacing": "0.05em", "text_transform": "uppercase"},
    "metric": {"size": "2rem", "weight": "700", "line_height": "1.1"},
    "metric_sm": {"size": "1.5rem", "weight": "600", "line_height": "1.2"},
}

# =============================================================================
# Spacing Scale (4px base)
# =============================================================================

SPACING = {
    "xs": "0.25rem",    # 4px
    "sm": "0.5rem",     # 8px
    "md": "1rem",       # 16px
    "lg": "1.5rem",     # 24px
    "xl": "2rem",       # 32px
    "2xl": "3rem",      # 48px
    "3xl": "4rem",      # 64px
}

# =============================================================================
# Border Radius
# =============================================================================

RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "2xl": "24px",
    "full": "9999px",
}

# =============================================================================
# Shadows
# =============================================================================

SHADOWS = {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
}

# =============================================================================
# Breakpoints
# =============================================================================

BREAKPOINTS = {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px",
}

# =============================================================================
# Z-Index Scale
# =============================================================================

Z_INDEX = {
    "base": 0,
    "dropdown": 100,
    "sticky": 200,
    "fixed": 300,
    "modal": 400,
    "popover": 500,
    "tooltip": 600,
    "command_palette": 700,
}

# =============================================================================
# Animation Tokens
# =============================================================================

ANIMATIONS = {
    "duration_fast": "150ms",
    "duration_normal": "200ms",
    "duration_slow": "300ms",
    "duration_slower": "500ms",
    "ease_default": "cubic-bezier(0.4, 0, 0.2, 1)",
    "ease_in": "cubic-bezier(0.4, 0, 1, 1)",
    "ease_out": "cubic-bezier(0, 0, 0.2, 1)",
    "ease_spring": "cubic-bezier(0.34, 1.56, 0.64, 1)",
}

# =============================================================================
# Layout Dimensions
# =============================================================================

LAYOUT = {
    "header_height": "64px",
    "sidebar_width": "280px",
    "max_content_width": "1440px",
    "search_height": "48px",
    "filter_height": "56px",
    "kpi_height": "120px",
}

# =============================================================================
# KPI Configuration
# =============================================================================

KPI_CONFIG = [
    {"id": "total_fields", "label": "Total Fields", "icon": "map", "format": "integer"},
    {"id": "avg_ndvi", "label": "Average NDVI", "icon": "chart", "format": "decimal", "range": [0, 1]},
    {"id": "avg_rainfall", "label": "Average Rainfall", "icon": "water", "format": "decimal", "unit": "mm"},
    {"id": "avg_heat_stress", "label": "Average Heat Stress", "icon": "fire", "format": "decimal", "unit": "days"},
    {"id": "high_risk", "label": "High-Risk Fields", "icon": "warning", "format": "integer"},
    {"id": "avg_field_stress", "label": "Avg Field Stress Index", "icon": "alert", "format": "decimal", "unit": "/100"},
]

# =============================================================================
# Map Configuration
# =============================================================================

MAP_CONFIG = {
    "default_zoom": 12,
    "center_lat": 38.91,
    "center_lon": -75.83,
    "style": "open-street-map",
    "layers": [
        {"id": "ndvi", "label": "NDVI", "color_scale": "RdYlGn"},
        {"id": "risk", "label": "Risk", "color_scale": "RdYlGn_r"},
        {"id": "heat_stress", "label": "Heat Stress", "color_scale": "YlOrRd"},
        {"id": "rainfall", "label": "Rainfall", "color_scale": "Blues"},
    ],
}

# =============================================================================
# Onboarding Configuration
# =============================================================================

ONBOARDING_OPTIONS = [
    {"id": "open-farm", "label": "Open Existing Farm", "icon": "folder", "color": "primary"},
    {"id": "add-farm", "label": "Add New Farm", "icon": "plus", "color": "secondary"},
    {"id": "demo", "label": "Launch Demo Mode", "icon": "play", "color": "success"},
]

# =============================================================================
# Command Palette Actions
# =============================================================================

COMMAND_ACTIONS = [
    {"id": "search", "label": "Search farms, fields...", "shortcut": "Ctrl+K", "icon": "search"},
    {"id": "theme", "label": "Toggle Theme", "shortcut": "Ctrl+Shift+L", "icon": "moon"},
    {"id": "demo", "label": "Launch Demo Mode", "shortcut": "Ctrl+Shift+D", "icon": "play"},
    {"id": "export", "label": "Export Dashboard", "shortcut": "Ctrl+Shift+E", "icon": "download"},
    {"id": "refresh", "label": "Refresh Data", "shortcut": "Ctrl+R", "icon": "refresh"},
    {"id": "reset", "label": "Reset Filters", "shortcut": "Ctrl+Shift+R", "icon": "reset"},
    {"id": "map", "label": "Go to Map", "shortcut": "Ctrl+1", "icon": "map"},
    {"id": "weather", "label": "Go to Weather", "shortcut": "Ctrl+2", "icon": "cloud"},
    {"id": "table", "label": "Go to Field Table", "shortcut": "Ctrl+3", "icon": "table"},
    {"id": "recommendations", "label": "Go to Recommendations", "shortcut": "Ctrl+4", "icon": "lightbulb"},
    {"id": "help", "label": "Help & Documentation", "shortcut": "Ctrl+?", "icon": "help"},
]

# =============================================================================
# Export Configuration
# =============================================================================

EXPORT_CONFIG = {
    "csv": {"enabled": True, "formats": ["weather", "fields", "ndvi", "heat_stress"]},
    "pdf": {"enabled": True, "filename": "green_ag_report_{{date}}.pdf"},
}

# =============================================================================
# Demo Mode Configuration
# =============================================================================

DEMO_CONFIG = {
    "auto_play_ndvi": True,
    "ndvi_play_duration": 3000,  # ms per month
    "highlight_field": "osm-1070144486",  # Largest field
    "show_badge": True,
    "badge_text": "Demo Mode",
    "auto_select_year": 2025,
    "auto_select_crop": "Soybeans",
}

# =============================================================================
# Accessibility
# =============================================================================

A11Y = {
    "focus_ring": "0 0 0 3px rgba(27, 94, 32, 0.4)",
    "focus_ring_dark": "0 0 0 3px rgba(129, 199, 132, 0.4)",
    "min_touch": "44px",
    "target_contrast": 4.5,
    "reduced_motion": "@media (prefers-reduced-motion: reduce)",
}
