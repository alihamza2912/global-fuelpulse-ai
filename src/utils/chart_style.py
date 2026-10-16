"""
Shared Plotly Chart Styling Utility for Global FuelPulse AI.
Guarantees consistent, high-contrast, editorial styling with clean margins,
untruncated legends, standoff axis titles, and readable typography across all charts.
"""

from typing import Any, Dict, List, Optional
import plotly.graph_objects as go
import numpy as np
import pandas as pd

COLOR_INK = "#F9FAFB"
COLOR_WHITE = "rgba(0,0,0,0)"
COLOR_CREAM = "#070A12"
COLOR_AMBER = "#F5B942"
COLOR_BORDER = "rgba(255, 255, 255, 0.12)"
COLOR_GRID = "rgba(255, 255, 255, 0.08)"
COLOR_TEXT_MUTED = "#94A3B8"

# Product name mapping dictionary for clean human-readable presentation
PRODUCT_NAME_MAP = {
    "petrol_regular": "Petrol (Regular)",
    "diesel": "Diesel",
    "motor_gasoline": "Petrol (Regular)",
    "crude_oil": "Crude Petroleum (HS 2709)",
    "refined_petroleum": "Refined Products (HS 2710)",
}

WATERFALL_NAME_MAP = {
    "Base Crude (FOB & Freight)": "Base Price",
    "Bas": "Base Price",
    "Refinery Margin & Freight": "Refinery Margin",
    "Refi": "Refinery Margin",
    "OMC Depot Cost": "OMC Margin",
    "OMC": "OMC Margin",
    "Central Excise Duty": "Central Excise Duty",
    "Cen": "Central Excise Duty",
    "Dealer Commission": "Dealer Commission",
    "Dea": "Dealer Commission",
    "State VAT (Delhi)": "State VAT",
    "Sta": "State VAT",
    "Retail Pump Price": "Retail Price",
    "Ret": "Retail Price",
}


def clean_product_label(label: str) -> str:
    """Returns human-readable product label, e.g., 'petrol_regular' -> 'Petrol (Regular)'."""
    if not isinstance(label, str):
        return label
    return PRODUCT_NAME_MAP.get(label, label)


def apply_clean_layout(
    fig: go.Figure,
    height: int = 460,
    title: Optional[str] = None,
    xaxis_title: Optional[str] = None,
    yaxis_title: Optional[str] = None,
    showlegend: Optional[bool] = None,
    legend_below: bool = True,
    rotate_x: Optional[int] = None,
    margin_l: Optional[int] = None,
    margin_b: Optional[int] = None,
    is_waterfall: bool = False,
    is_pie: bool = False,
    **kwargs
) -> go.Figure:
    """
    Applies comprehensive, publication-grade styling to any Plotly figure:
    - Legend placed below chart horizontally with multi-row wrapping (never on the right).
    - Generous margins (l=80+, r=30, t=60, b=140+) so nothing is clipped.
    - automargin=True and title_standoff=20+ on both axes to eliminate overlaps.
    - X-axis labels rotated or wrapped with full names (never truncated).
    - Waterfall charts mapped to full 7 steps with rotated tick angles.
    - Donut/pie charts positioned with outside labels for small slices (<6%).
    - Product names mapped from raw codes (petrol_regular -> Petrol (Regular)).
    - High-contrast typography in black (#000000) or carbon ink (#111111) at 12px minimum.
    """
    if fig is None:
        return fig

    # 1. Inspect and sanitize traces
    has_geo = False
    has_pie = is_pie
    has_waterfall = is_waterfall
    is_horizontal_bar = False

    for trace in fig.data:
        t_type = getattr(trace, "type", "")
        if t_type in ("scattergeo", "choropleth", "geo"):
            has_geo = True
        elif t_type in ("pie", "donut"):
            has_pie = True
        elif t_type == "waterfall":
            has_waterfall = True
        elif t_type == "bar" and getattr(trace, "orientation", "") == "h":
            is_horizontal_bar = True

        # Clean product names in trace attributes
        if hasattr(trace, "name") and trace.name:
            trace.name = clean_product_label(trace.name)
            if trace.name == "petrol_regular":
                trace.name = "Petrol (Regular)"
            elif trace.name == "diesel":
                trace.name = "Diesel"
            elif trace.name == "Crude Refining Throughput (MMT":
                trace.name = "Crude Refining Throughput (MMT)"

        if hasattr(trace, "legendgroup") and trace.legendgroup:
            trace.legendgroup = clean_product_label(trace.legendgroup)

        # Clean hovertemplates
        if hasattr(trace, "hovertemplate") and trace.hovertemplate:
            trace.hovertemplate = (
                trace.hovertemplate
                .replace("petrol_regular", "Petrol (Regular)")
                .replace("diesel", "Diesel")
            )

        # Clean Pie / Donut slices
        if t_type == "pie":
            if hasattr(trace, "labels") and trace.labels is not None:
                new_labels = [clean_product_label(str(l)) for l in trace.labels]
                trace.labels = new_labels

            # Smart slice label positioning: inside for >= 6%, outside for < 6%
            if hasattr(trace, "values") and trace.values is not None:
                try:
                    vals = np.array(trace.values, dtype=float)
                    total_val = np.nansum(vals)
                    if total_val > 0:
                        pcts = vals / total_val
                        positions = ["outside" if p < 0.06 else "inside" for p in pcts]
                        trace.textposition = positions
                except Exception:
                    trace.textposition = "auto"
            else:
                trace.textposition = "auto"

            trace.insidetextfont = dict(family="'Space Grotesk', sans-serif", size=12, color="#FFFFFF")
            trace.outsidetextfont = dict(family="'Space Grotesk', sans-serif", size=12, color=COLOR_INK)

        # Clean Waterfall steps
        if t_type == "waterfall" or has_waterfall:
            if hasattr(trace, "x") and trace.x is not None:
                new_x = []
                for val in trace.x:
                    s_val = str(val).strip()
                    cleaned = WATERFALL_NAME_MAP.get(s_val, s_val)
                    new_x.append(cleaned)
                trace.x = new_x
            has_waterfall = True

    # 2. Compute dynamic margins based on chart characteristics
    calc_l = margin_l if margin_l is not None else (120 if is_horizontal_bar else 85)
    calc_r = 35
    calc_t = 60 if title else 40

    if has_waterfall:
        calc_b = margin_b if margin_b is not None else 150
        if rotate_x is None:
            rotate_x = -30
    elif has_pie:
        calc_b = margin_b if margin_b is not None else (130 if legend_below else 60)
        calc_l = 40
        calc_r = 40
    elif has_geo:
        calc_b = margin_b if margin_b is not None else 30
        calc_l = 15
        calc_r = 15
        calc_t = 30
    else:
        calc_b = margin_b if margin_b is not None else (140 if legend_below else 80)

    # 3. Base layout configuration
    layout_updates: Dict[str, Any] = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "height": max(height, 450),
        "font": dict(
            family="'Space Grotesk', 'Inter', -apple-system, sans-serif",
            color=COLOR_INK,
            size=13
        ),
        "margin": dict(l=calc_l, r=calc_r, t=calc_t, b=calc_b),
        "hoverlabel": dict(
            bgcolor="#0E1526",
            bordercolor="rgba(255, 255, 255, 0.2)",
            font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=13)
        )
    }

    if title:
        layout_updates["title"] = dict(
            text=f"<b>{title}</b>",
            font=dict(family="'Space Grotesk', sans-serif", size=17, color=COLOR_INK),
            x=0.02,
            xanchor="left",
            y=0.96
        )

    # 4. Legend styling (always below chart horizontally, never on the right)
    determine_showlegend = showlegend
    if determine_showlegend is None:
        # Determine from existing fig layout
        existing_show = getattr(fig.layout, "showlegend", None)
        determine_showlegend = existing_show if existing_show is not None else True

    if determine_showlegend and not has_geo:
        layout_updates["showlegend"] = True
        if legend_below:
            # Place below x-axis with ample clearance
            leg_y = -0.28 if (rotate_x or has_waterfall) else -0.22
            layout_updates["legend"] = dict(
                orientation="h",
                yanchor="top",
                y=leg_y,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(14, 21, 38, 0.8)",
                bordercolor="rgba(255, 255, 255, 0.12)",
                borderwidth=1,
                font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=13),
                itemwidth=40,
                traceorder="normal"
            )
        else:
            layout_updates["legend"] = dict(
                bgcolor="rgba(14, 21, 38, 0.8)",
                bordercolor="rgba(255, 255, 255, 0.12)",
                borderwidth=1,
                font=dict(color="#F9FAFB", family="'Space Grotesk', sans-serif", size=13)
            )
    elif determine_showlegend is False:
        layout_updates["showlegend"] = False

    fig.update_layout(**layout_updates)

    # 5. Cartesian Axes Configuration (automargin + standoff)
    if not has_geo:
        xaxis_kwargs: Dict[str, Any] = {
            "automargin": True,
            "title_standoff": 22,
            "gridcolor": COLOR_GRID,
            "zerolinecolor": "rgba(255, 255, 255, 0.12)",
            "tickfont": dict(color=COLOR_TEXT_MUTED, family="'Space Grotesk', sans-serif", size=12),
            "title_font": dict(color=COLOR_INK, family="'Space Grotesk', sans-serif", size=14, weight="bold")
        }
        if rotate_x is not None:
            xaxis_kwargs["tickangle"] = rotate_x
        if xaxis_title:
            xaxis_kwargs["title_text"] = xaxis_title

        yaxis_kwargs: Dict[str, Any] = {
            "automargin": True,
            "title_standoff": 24,
            "gridcolor": COLOR_GRID,
            "zerolinecolor": "rgba(255, 255, 255, 0.12)",
            "tickfont": dict(color=COLOR_TEXT_MUTED, family="'Space Grotesk', sans-serif", size=12),
            "title_font": dict(color=COLOR_INK, family="'Space Grotesk', sans-serif", size=14, weight="bold")
        }
        if yaxis_title:
            yaxis_kwargs["title_text"] = yaxis_title

        fig.update_xaxes(**xaxis_kwargs)
        fig.update_yaxes(**yaxis_kwargs)

    # 6. Apply any caller-specific overrides
    if kwargs:
        fig.update_layout(**kwargs)

    return fig
