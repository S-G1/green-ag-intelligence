"""Chart theme helper — Centralized Plotly figure theming.

Provides template, colors, and layout defaults for light/dark mode.
"""

from __future__ import annotations

import plotly.io as pio


def get_chart_template(theme: str = "light") -> str:
    """Return the appropriate Plotly template for the theme."""
    return "plotly_dark" if theme == "dark" else "plotly_white"


def get_paper_bgcolor(theme: str = "light") -> str:
    """Return paper background color for charts."""
    return "rgba(45, 45, 45, 1)" if theme == "dark" else "rgba(255, 255, 255, 1)"


def get_plot_bgcolor(theme: str = "light") -> str:
    """Return plot background color for charts."""
    return "rgba(45, 45, 45, 1)" if theme == "dark" else "rgba(255, 255, 255, 1)"


def get_grid_color(theme: str = "light") -> str:
    """Return grid line color for charts."""
    return "rgba(255, 255, 255, 0.1)" if theme == "dark" else "rgba(0, 0, 0, 0.1)"


def get_text_color(theme: str = "light") -> str:
    """Return primary text color for chart labels."""
    return "#E0E0E0" if theme == "dark" else "#212121"


def get_legend_bgcolor(theme: str = "light") -> str:
    """Return legend background color."""
    return "rgba(45, 45, 45, 0.9)" if theme == "dark" else "rgba(255, 255, 255, 0.9)"


def apply_chart_theme(fig, theme: str = "light"):
    """Apply theme colors to an existing Plotly figure in-place."""
    template = get_chart_template(theme)
    paper = get_paper_bgcolor(theme)
    plot = get_plot_bgcolor(theme)
    text = get_text_color(theme)
    grid = get_grid_color(theme)
    
    fig.update_layout(
        template=template,
        paper_bgcolor=paper,
        plot_bgcolor=plot,
        font_color=text,
        legend_bgcolor=get_legend_bgcolor(theme),
    )
    
    # Update axis colors
    fig.update_xaxes(
        gridcolor=grid,
        zerolinecolor=grid,
        tickfont_color=text,
        title_font_color=text,
    )
    fig.update_yaxes(
        gridcolor=grid,
        zerolinecolor=grid,
        tickfont_color=text,
        title_font_color=text,
    )
    
    return fig
