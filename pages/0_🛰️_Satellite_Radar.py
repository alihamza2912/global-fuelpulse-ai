"""
Page 0: Satellite Earth Observation Radar & Energy Flow Intelligence.
Grounded in low-Earth orbit (LEO) reconnaissance: sub-meter optical, day/night X-band SAR radar,
and radiometric thermal infrared surveillance tracking crude oil storage, refineries, and maritime chokepoints.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from src.ui_components import (
    render_page_header,
    render_instrument_card,
    apply_theme,
    render_html,
    COLOR_INK,
    COLOR_AMBER,
    COLOR_WHITE,
    COLOR_CREAM
)

apply_theme()

render_page_header(
    title="SATELLITE EARTH OBSERVATION & ENERGY RADAR",
    subtitle="Low-Earth Orbit (LEO) Optical, X-Band SAR Radar, and Thermal Infrared Surveillance of Global Petroleum Assets",
    source_tag="PULSE Constellation Telemetry • Sentinel-2 • Landsat-9 • AIS Hybrid",
    observation_date="Continuous 15-Minute Revisit Stream"
)

# 1. Headline Orbital Telemetry Metrics
k1, k2, k3, k4 = st.columns(4)

with k1:
    render_instrument_card(
        label="Orbital Constellation",
        value="18 Active Satellites",
        accent="amber",
        subtext="510–530 km Sun-Synchronous LEO",
        code_badge="LEO"
    )

with k2:
    render_instrument_card(
        label="Optical Resolution",
        value="0.30m GSD",
        accent="teal",
        subtext="16 Spectral Bands (VNIR + RedEdge)",
        code_badge="30CM"
    )

with k3:
    render_instrument_card(
        label="SAR Radar Capability",
        value="100% Cloud Penetration",
        accent="copper",
        subtext="X-Band Polarimetric Day & Night",
        code_badge="SAR"
    )

with k4:
    render_instrument_card(
        label="Storage Auditing",
        value="Floating Roof Liquid Depth",
        accent="red",
        subtext="±1.2% Commercial Volume Precision",
        code_badge="STORAGE"
    )

st.write("")

# 2. Interactive Drag-to-Compare Sensor Slider
st.subheader("⚡ Drag to Compare: Optical vs. Synthetic Aperture Radar (SAR)")
st.markdown(
    """
    **Sensor Fusion Engine:** Drag the interactive slider below to inspect how cloud cover vanishes under X-band radar, 
    revealing crude oil storage tank fill levels and hidden ship wakes in critical corridors like Ras Tanura and the Strait of Hormuz.
    """
)

slider_html = """
<div style="width: 100%; border: 2px solid #111111; border-radius: 12px; overflow: hidden; background: #070b14; box-shadow: 4px 4px 0px #111111; margin-bottom: 24px;">
  <div style="padding: 10px 16px; background: #111111; color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; display: flex; justify-content: space-between; align-items: center;">
    <span>📡 ORBITAL SENSOR FUSION: RAS TANURA CRUDE TERMINAL & BATTERY</span>
    <span style="color: #F5B942;">ACQUISITION: 2026-10-16 08:30 UTC</span>
  </div>

  <div id="stDragContainer" style="position: relative; width: 100%; height: 380px; overflow: hidden; user-select: none; cursor: ew-resize; background: #081524;">
    <!-- SAR Radar Layer (Right / Background) -->
    <div style="position: absolute; inset: 0; background: #081524; display: flex; flex-direction: column; justify-content: space-between; padding: 20px;">
      <svg style="position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0.75;" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="stRadarGrid" width="35" height="35" patternUnits="userSpaceOnUse">
            <path d="M 35 0 L 0 0 0 35" fill="none" stroke="rgba(56, 189, 248, 0.15)" stroke-width="1" />
          </pattern>
          <radialGradient id="stThermalGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#ef4444" stop-opacity="0.9" />
            <stop offset="60%" stop-color="#f59e0b" stop-opacity="0.65" />
            <stop offset="100%" stop-color="#082f49" stop-opacity="0.1" />
          </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#stRadarGrid)" />
        <!-- Floating Roof Tanks with Liquid Depth Radiance -->
        <circle cx="28%" cy="40%" r="48" fill="url(#stThermalGlow)" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3 3" />
        <circle cx="48%" cy="38%" r="46" fill="url(#stThermalGlow)" stroke="#38bdf8" stroke-width="2" />
        <circle cx="68%" cy="42%" r="50" fill="url(#stThermalGlow)" stroke="#38bdf8" stroke-width="2" stroke-dasharray="3 3" />
        <circle cx="36%" cy="68%" r="46" fill="url(#stThermalGlow)" stroke="#38bdf8" stroke-width="2" />
        <circle cx="58%" cy="70%" r="48" fill="url(#stThermalGlow)" stroke="#38bdf8" stroke-width="2" />
        <!-- Ship Wake -->
        <path d="M 120 320 Q 240 280, 420 250" stroke="#38bdf8" stroke-width="3" fill="none" opacity="0.85" />
        <circle cx="420" cy="250" r="7" fill="#38bdf8" />
      </svg>
      <div style="position: relative; z-index: 10; display: flex; justify-content: space-between; font-family: monospace; font-size: 11px;">
        <span style="background: rgba(8,47,73,0.9); border: 1px solid rgba(56,189,248,0.5); color: #7dd3fc; padding: 4px 10px; rounded: 9999px; font-weight: bold;">
          📡 X-BAND SAR + LWIR THERMAL
        </span>
        <span style="background: rgba(15,23,42,0.9); color: #38bdf8; padding: 4px 10px; font-weight: bold;">
          ALL-WEATHER 100% VISIBILITY
        </span>
      </div>
      <div style="position: relative; z-index: 10; background: rgba(15,23,42,0.92); border: 1px solid rgba(56,189,248,0.3); padding: 10px; border-radius: 8px; max-width: 380px; font-family: monospace; font-size: 11px; line-height: 1.4;">
        <div style="color: #38bdf8; font-weight: bold;">RADAR LIQUID VOLUME AUDIT:</div>
        <div style="color: #e2e8f0;">• Tank Cluster 04: <span style="color: #34d399; font-weight: bold;">78.2% Full</span> (942,000 bbl)</div>
        <div style="color: #e2e8f0;">• Tank Cluster 05: <span style="color: #F5B942; font-weight: bold;">42.1% Full</span> (-18% Net Outflow)</div>
      </div>
    </div>

    <!-- Optical Layer (Foreground Clipped) -->
    <div id="stDragClipped" style="position: absolute; inset: 0; width: 50%; overflow: hidden;">
      <div style="position: absolute; inset: 0; width: 1000px; height: 100%; background: #1c2734; display: flex; flex-direction: column; justify-content: space-between; padding: 20px;">
        <svg style="position: absolute; inset: 0; width: 100%; height: 100%;" xmlns="http://www.w3.org/2000/svg">
          <rect width="100%" height="100%" fill="#16222d" />
          <path d="M 0 0 L 750 0 L 640 400 L 0 400 Z" fill="#243444" />
          <circle cx="28%" cy="40%" r="48" fill="#e2e8f0" stroke="#0f172a" stroke-width="2" />
          <circle cx="48%" cy="38%" r="46" fill="#cbd5e1" stroke="#0f172a" stroke-width="2" />
          <circle cx="68%" cy="42%" r="50" fill="#f8fafc" stroke="#0f172a" stroke-width="2" />
          <circle cx="36%" cy="68%" r="46" fill="#cbd5e1" stroke="#0f172a" stroke-width="2" />
          <circle cx="58%" cy="70%" r="48" fill="#e2e8f0" stroke="#0f172a" stroke-width="2" />
          <!-- Heavy Cloud Obstruction -->
          <ellipse cx="38%" cy="42%" rx="200" ry="100" fill="rgba(255,255,255,0.76)" filter="blur(24px)" />
          <ellipse cx="62%" cy="50%" rx="180" ry="120" fill="rgba(255,255,255,0.85)" filter="blur(28px)" />
        </svg>
        <div style="position: relative; z-index: 10; display: flex; justify-content: space-between; font-family: monospace; font-size: 11px;">
          <span style="background: rgba(69,26,3,0.9); border: 1px solid rgba(245,185,66,0.5); color: #fde68a; padding: 4px 10px; font-weight: bold;">
            ☀️ 0.30M OPTICAL RGB
          </span>
          <span style="background: rgba(15,23,42,0.9); color: #F5B942; padding: 4px 10px; font-weight: bold;">
            ⚠️ 74% CLOUD COVER
          </span>
        </div>
        <div style="position: relative; z-index: 10; background: rgba(15,23,42,0.92); border: 1px solid rgba(245,185,66,0.3); padding: 10px; border-radius: 8px; max-width: 380px; font-family: monospace; font-size: 11px; line-height: 1.4;">
          <div style="color: #F5B942; font-weight: bold;">OPTICAL VISIBILITY NOTICE:</div>
          <div style="color: #cbd5e1;">Dense atmospheric cloud cover obstructing optical sensors. Surface features occluded.</div>
        </div>
      </div>
    </div>

    <!-- Draggable Divider Line & Knob -->
    <div id="stDragDivider" style="position: absolute; top: 0; bottom: 0; left: 50%; width: 3px; background: #FFFFFF; box-shadow: 0 0 14px rgba(255,255,255,0.9); z-index: 30;">
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 34px; height: 34px; border-radius: 9999px; background: #F5B942; border: 2px solid #FFFFFF; color: #111111; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
        ⟷
      </div>
    </div>
  </div>

  <div style="padding: 8px 14px; background: #FFF9E8; border-top: 1.5px solid #111111; font-family: monospace; font-size: 11.5px; color: #111111; display: flex; justify-content: space-between;">
    <span><b>INTERACTION:</b> Drag slider left/right</span>
    <span><b>ORBITAL REVISIT:</b> 01h 14m (PULSE-SAR X)</span>
  </div>
</div>

<script>
(function() {
  const container = document.getElementById('stDragContainer');
  const clipped = document.getElementById('stDragClipped');
  const divider = document.getElementById('stDragDivider');
  let isDragging = false;

  function updateSlider(clientX) {
    if (!isDragging || !container) return;
    const rect = container.getBoundingClientRect();
    const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
    const pct = (x / rect.width) * 100;
    clipped.style.width = pct + '%';
    divider.style.left = pct + '%';
  }

  if (container) {
    container.addEventListener('mousedown', () => { isDragging = true; });
    window.addEventListener('mouseup', () => { isDragging = false; });
    container.addEventListener('mousemove', (e) => updateSlider(e.clientX));

    container.addEventListener('touchstart', () => { isDragging = true; });
    window.addEventListener('touchend', () => { isDragging = false; });
    container.addEventListener('touchmove', (e) => updateSlider(e.touches[0].clientX));
  }
})();
</script>
"""

render_html(slider_html)

st.write("")

# 3. Spacecraft Fleet & Payload Dossier
st.subheader("🛰️ Spacecraft Fleet & Payload Constellation")
f1, f2 = st.columns(2)

with f1:
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 2px solid #111111; border-radius: 8px; padding: 18px; box-shadow: 3px 3px 0px #111111; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 17px; font-weight: 800; color: #111111;">PULSE-OPTIC 1 & 2</span>
                <span style="font-family: monospace; font-size: 11px; background: #D9F4D8; color: #111111; padding: 2px 8px; border-radius: 9999px; font-weight: 700; border: 1px solid #111111;">ACTIVE LEO</span>
            </div>
            <div style="font-family: monospace; font-size: 12px; color: #555555; margin-bottom: 10px;">
                0.30m GSD • 16 Multispectral Bands • 510 km Sun-Synchronous Orbit
            </div>
            <p style="font-size: 13.5px; color: #111111; line-height: 1.5; margin: 0;">
                Sub-meter optical intelligence tracking floating-roof oil storage tanks, terminal manifold valve yards, and VLCC deck activity under daylight conditions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="background: #FFFFFF; border: 2px solid #111111; border-radius: 8px; padding: 18px; box-shadow: 3px 3px 0px #111111;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 17px; font-weight: 800; color: #111111;">PULSE-SAR X</span>
                <span style="font-family: monospace; font-size: 11px; background: #FFE58A; color: #111111; padding: 2px 8px; border-radius: 9999px; font-weight: 700; border: 1px solid #111111;">X-BAND RADAR</span>
            </div>
            <div style="font-family: monospace; font-size: 12px; color: #555555; margin-bottom: 10px;">
                0.50m Spotlight • X-Band (9.65 GHz) • 100% Cloud-Penetrating
            </div>
            <p style="font-size: 13.5px; color: #111111; line-height: 1.5; margin: 0;">
                Penetrates heavy monsoons, sandstorms, and night to compute oil tanker displacement and seaborne flotilla trajectories through critical choke corridors.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with f2:
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 2px solid #111111; border-radius: 8px; padding: 18px; box-shadow: 3px 3px 0px #111111; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 17px; font-weight: 800; color: #111111;">PULSE-THERMAL 3</span>
                <span style="font-family: monospace; font-size: 11px; background: #F7E1E6; color: #C53030; padding: 2px 8px; border-radius: 9999px; font-weight: 700; border: 1px solid #111111;">RADIOMETRIC</span>
            </div>
            <div style="font-family: monospace; font-size: 12px; color: #555555; margin-bottom: 10px;">
                2.5m Radiometric • Dual LWIR (8.5–12.0 µm) • 8-Hour Revisit
            </div>
            <p style="font-size: 13.5px; color: #111111; line-height: 1.5; margin: 0;">
                Monitors refinery cracking units, catalytic reformer furnace temperatures, and flaring volumes to estimate refining runs and crack spread economics before official disclosures.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="background: #FFFFFF; border: 2px solid #111111; border-radius: 8px; padding: 18px; box-shadow: 3px 3px 0px #111111;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 17px; font-weight: 800; color: #111111;">PULSE-AIS HYBRID</span>
                <span style="font-family: monospace; font-size: 11px; background: #DFEBFA; color: #2B6CB0; padding: 2px 8px; border-radius: 9999px; font-weight: 700; border: 1px solid #111111;">RF SURVEILLANCE</span>
            </div>
            <div style="font-family: monospace; font-size: 12px; color: #555555; margin-bottom: 10px;">
                Space-Based AIS Interception • RF Spectrum Analyzer • 1,200 km Reception
            </div>
            <p style="font-size: 13.5px; color: #111111; line-height: 1.5; margin: 0;">
                Correlates space-based AIS maritime transponders with satellite radar wakes to expose dark-fleet tankers operating with disabled or spoofed location beacons.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# 4. Interactive Satellite Tasking Request Simulator
st.subheader("🎯 On-Demand Satellite Tasking Simulator")
st.markdown("Submit simulated priority tasking requests over any strategic energy facility or chokepoint.")

with st.form("satellite_tasking_form"):
    t_c1, t_c2, t_c3 = st.columns([4, 4, 3])
    with t_c1:
        target_aoi = st.selectbox(
            "Target Area of Interest (AOI)",
            [
                "Strait of Hormuz (26.56° N, 56.25° E) — 18.5 mbpd Transit",
                "Jamnagar Refining Complex (22.47° N, 70.06° E) — World's Largest Refinery",
                "Ras Tanura Terminal, Saudi Arabia (26.64° N, 50.16° E) — Offshore Berths",
                "Fujairah Commercial Anchorage (25.13° N, 56.33° E) — Bunkering Hub",
                "Cushing Crude Storage Battery, USA (35.98° N, -96.76° E) — WTI Benchmark",
                "Malacca Strait Corridor (1.29° N, 103.85° E) — 16.2 mbpd Asia Conduit"
            ]
        )
    with t_c2:
        sensor_mode = st.selectbox(
            "Imaging Sensor Mode",
            [
                "PULSE-OPTIC (0.30m Multispectral Visual)",
                "PULSE-SAR-X (0.50m Cloud-Penetrating Radar)",
                "PULSE-THERMAL (Radiometric Flare & Flue Analysis)"
            ]
        )
    with t_c3:
        priority_window = st.selectbox(
            "Tasking Priority",
            ["Emergency Rush (< 3h)", "Next Orbit Pass (< 12h)", "Standard Monitoring (24h)"]
        )

    submit_tasking = st.form_submit_button("⚡ DISPATCH SATELLITE TASKING REQUEST", use_container_width=True)

if submit_tasking:
    st.success(
        f"✅ **TASKING ORDER CONFIRMED (NORAD ID: 58214):** Satellite `{sensor_mode.split('(')[0].strip()}` "
        f"assigned to target `{target_aoi.split('—')[0].strip()}` under `{priority_window}` priority. "
        f"Downlink imagery stream expected in **01h 14m** via Svalbard ground station."
    )
