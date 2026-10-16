"use client"

import React, { useState, useEffect, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import {
  Satellite,
  Radio,
  Eye,
  Crosshair,
  Layers,
  Flame,
  Ship,
  MapPin,
  Clock,
  Shield,
  Zap,
  Globe2,
  ChevronRight,
  Maximize2,
  Sliders,
  CheckCircle2,
  AlertCircle,
  Download,
  Calendar,
  Compass,
  ArrowRight,
  Terminal,
  Activity
} from "lucide-react"
import { NavBar } from "@/components/ui/tubelight-navbar"

// Satellite Constellation Specs
const FLEET_SPACECRAFT = [
  {
    id: "pulse-optic-1",
    name: "PULSE-OPTIC 1",
    tagline: "Ultra-High Resolution Optical",
    gsd: "0.30m GSD",
    bands: "16 Spectral Bands (VNIR + RedEdge)",
    orbit: "510 km Sun-Synchronous (97.4°)",
    revisit: "Daily at 10:30 AM local time",
    swath: "14.2 km Swath Width",
    status: "NOMINAL",
    icon: Eye,
    color: "#38bdf8",
    description: "Designed for micro-asset surveillance: floating roof tank liquid heights, valve yards, and tanker deck activity."
  },
  {
    id: "pulse-sar-x",
    name: "PULSE-SAR X",
    tagline: "Cloud-Penetrating X-Band Radar",
    gsd: "0.50m Spotlight / 1.0m Stripmap",
    bands: "X-Band (9.65 GHz) Polarimetric",
    orbit: "525 km Dawn-Dusk LEO",
    revisit: "Twice daily (Day & Night)",
    swath: "25.0 km Swath Width",
    status: "ACTIVE ORBIT",
    icon: Radio,
    color: "#f59e0b",
    description: "Penetrates 100% cloud cover, monsoons, and nighttime to monitor crude tanker displacement and offshore platforms."
  },
  {
    id: "pulse-thermal-3",
    name: "PULSE-THERMAL 3",
    tagline: "Radiometric Infrared Surveillance",
    gsd: "2.5m Thermal Resolution",
    bands: "Dual LWIR (8.5–12.0 µm)",
    orbit: "515 km Mid-Inclination",
    revisit: "Every 8 hours over refining hubs",
    swath: "45.0 km Swath Width",
    status: "CALIBRATED",
    icon: Flame,
    color: "#ef4444",
    description: "Audits refinery cracking furnace temperatures, cooling tower activity, and gas flare volume in real time."
  },
  {
    id: "pulse-ais-hybrid",
    name: "PULSE-AIS HYBRID",
    tagline: "Space-Based Maritime Intelligence",
    gsd: "Global Vessel Interception",
    bands: "VHF Marine + RF Spectrum",
    orbit: "530 km Equatorial & Polar",
    revisit: "Continuous Real-Time",
    swath: "1,200 km Reception Cone",
    status: "STREAMING",
    icon: Ship,
    color: "#10b981",
    description: "Correlates satellite radar wakes with transponder signals to detect dark fleet tankers spoofing AIS positions."
  }
]

// Target Locations for Pass Calculator
const PASS_TARGETS = [
  { name: "Strait of Hormuz (Oman/Iran)", lat: 26.56, lon: 56.25, nextPass: "01h 14m", satellite: "PULSE-SAR X", elevation: "68°" },
  { name: "Jamnagar Refinery (India)", lat: 22.47, lon: 70.06, nextPass: "02h 38m", satellite: "PULSE-OPTIC 1", elevation: "74°" },
  { name: "Ras Tanura Terminal (Saudi Arabia)", lat: 26.64, lon: 50.16, nextPass: "03h 05m", satellite: "PULSE-THERMAL 3", elevation: "82°" },
  { name: "Singapore Anchorage (Malacca)", lat: 1.29, lon: 103.85, nextPass: "00h 42m", satellite: "PULSE-AIS HYBRID", elevation: "89°" },
  { name: "Cushing Storage Hub (USA)", lat: 35.98, lon: -96.76, nextPass: "04h 12m", satellite: "PULSE-SAR X", elevation: "61°" },
  { name: "Rotterdam Europoort (Netherlands)", lat: 51.95, lon: 4.14, nextPass: "01h 55m", satellite: "PULSE-OPTIC 1", elevation: "71°" }
]

// Imagery Archive Catalog
const ARCHIVE_ITEMS = [
  {
    title: "Cushing Commercial Crude Stockpiles",
    location: "Oklahoma, United States",
    date: "2026-10-15",
    type: "SAR + Optical Height Model",
    metric: "68.4% Tank Fill (+1.8% WoW)",
    resolution: "0.30m GSD",
    cloudCover: "0.0%",
    tags: ["Storage", "Crude Inventory", "WTI"]
  },
  {
    title: "Strait of Hormuz Seaborne Flotilla",
    location: "Persian Gulf Corridor",
    date: "2026-10-16",
    type: "SAR Ship Wake & AIS Correlation",
    metric: "18.4 mbpd Tracked Throughput",
    resolution: "0.50m X-Band",
    cloudCover: "All-Weather",
    tags: ["Maritime", "Chokepoint", "VLCC"]
  },
  {
    title: "Jamnagar Refining Supercomplex",
    location: "Gujarat, India",
    date: "2026-10-14",
    type: "Thermal Radiometric Infrared",
    metric: "1.24 mbpd Operating Rate (98%)",
    resolution: "2.5m Thermal",
    cloudCover: "2.1%",
    tags: ["Refining", "Thermal", "Crack Spreads"]
  },
  {
    title: "Fujairah Bunker & Export Terminals",
    location: "Gulf of Oman, UAE",
    date: "2026-10-16",
    type: "Optical Multi-Spectral 16-Band",
    metric: "42 Tankers Anchored",
    resolution: "0.30m GSD",
    cloudCover: "0.0%",
    tags: ["Storage", "Bunkering", "OPEC"]
  }
]

export function SatelliteImagingLandingPage() {
  // Navigation tabs
  const navItems = [
    { name: "Overview", url: "#hero", icon: Globe2 },
    { name: "Compare", url: "#compare", icon: Sliders },
    { name: "Fleet", url: "#fleet", icon: Satellite },
    { name: "Ground Track", url: "#ground-track", icon: Crosshair },
    { name: "Tasking", url: "#tasking", icon: Calendar },
    { name: "Catalog", url: "#catalog", icon: Layers }
  ]

  // Hero canvas ref
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Drag-to-compare state
  const [sliderPos, setSliderPos] = useState(52)
  const isDragging = useRef(false)
  const containerRef = useRef<HTMLDivElement>(null)

  // Pass calculator selected city
  const [selectedTarget, setSelectedTarget] = useState(PASS_TARGETS[0])

  // Active satellite in fleet
  const [activeSat, setActiveSat] = useState(FLEET_SPACECRAFT[0])

  // Tasking form state
  const [taskingAoi, setTaskingAoi] = useState("Strait of Hormuz (26.56° N, 56.25° E)")
  const [taskingSensor, setTaskingSensor] = useState("PULSE-OPTIC (30cm Optical)")
  const [taskingPriority, setTaskingPriority] = useState("Emergency Rush (< 3h)")
  const [taskingSuccess, setTaskingSuccess] = useState(false)
  const [taskingLoading, setTaskingLoading] = useState(false)

  // Orbital simulation telemetry
  const [orbitalPos, setOrbitalPos] = useState({ lat: 26.54, lon: 56.23, alt: 518.2, vel: 7.61, time: "10:48:22 UTC" })

  // Real-time canvas Earth Limb animation
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    let animationId: number
    let time = 0

    const resize = () => {
      canvas.width = canvas.parentElement?.clientWidth || window.innerWidth
      canvas.height = canvas.parentElement?.clientHeight || 650
    }
    resize()
    window.addEventListener("resize", resize)

    // Generate random background stars
    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random(),
      y: Math.random(),
      size: Math.random() * 1.8 + 0.4,
      alpha: Math.random() * 0.7 + 0.3,
      twinkleSpeed: Math.random() * 0.02 + 0.005
    }))

    const render = () => {
      time += 0.015
      const w = canvas.width
      const h = canvas.height

      // Deep space background gradient
      const spaceGrad = ctx.createLinearGradient(0, 0, 0, h)
      spaceGrad.addColorStop(0, "#030712")
      spaceGrad.addColorStop(0.5, "#0b0f19")
      spaceGrad.addColorStop(1, "#02040a")
      ctx.fillStyle = spaceGrad
      ctx.fillRect(0, 0, w, h)

      // Draw starry sky
      stars.forEach((star) => {
        const twinkle = Math.sin(time * 50 * star.twinkleSpeed) * 0.3 + 0.7
        ctx.fillStyle = `rgba(226, 232, 240, ${star.alpha * twinkle})`
        ctx.beginPath()
        ctx.arc(star.x * w, star.y * h * 0.7, star.size, 0, Math.PI * 2)
        ctx.fill()
      })

      // Earth Limb Curvature (Large smooth circle segment at bottom)
      const earthCenterX = w * 0.5
      const earthCenterY = h * 1.85
      const earthRadius = h * 1.25

      // Atmospheric outer glow (Sun glint & cyan auroral haze)
      const glowGrad = ctx.createRadialGradient(
        earthCenterX,
        earthCenterY,
        earthRadius * 0.98,
        earthCenterX,
        earthCenterY,
        earthRadius * 1.08
      )
      glowGrad.addColorStop(0, "rgba(56, 189, 248, 0.45)")
      glowGrad.addColorStop(0.3, "rgba(14, 165, 233, 0.22)")
      glowGrad.addColorStop(0.7, "rgba(2, 132, 199, 0.08)")
      glowGrad.addColorStop(1, "rgba(2, 6, 23, 0)")

      ctx.fillStyle = glowGrad
      ctx.beginPath()
      ctx.arc(earthCenterX, earthCenterY, earthRadius * 1.08, Math.PI, 0)
      ctx.fill()

      // Atmospheric limb sharp edge
      ctx.strokeStyle = "rgba(125, 211, 252, 0.75)"
      ctx.lineWidth = 3
      ctx.beginPath()
      ctx.arc(earthCenterX, earthCenterY, earthRadius, Math.PI, 0)
      ctx.stroke()

      // Earth body (Deep ocean blue with cloud bands)
      const earthBody = ctx.createRadialGradient(
        earthCenterX,
        earthCenterY,
        0,
        earthCenterX,
        earthCenterY,
        earthRadius
      )
      earthBody.addColorStop(0, "#082f49")
      earthBody.addColorStop(0.85, "#0c4a6e")
      earthBody.addColorStop(1, "#0369a1")
      ctx.fillStyle = earthBody
      ctx.beginPath()
      ctx.arc(earthCenterX, earthCenterY, earthRadius, Math.PI, 0)
      ctx.fill()

      // Animated low-orbit cloud layers and atmospheric bands
      ctx.save()
      ctx.beginPath()
      ctx.arc(earthCenterX, earthCenterY, earthRadius, Math.PI, 0)
      ctx.clip()

      // Whispy clouds drifting across the limb
      for (let i = 0; i < 4; i++) {
        const offset = (time * (10 + i * 5)) % (w * 1.5) - w * 0.25
        const cloudY = h * 0.72 + i * 22
        ctx.fillStyle = `rgba(255, 255, 255, ${0.12 - i * 0.02})`
        ctx.beginPath()
        ctx.ellipse(offset, cloudY, 180 + i * 40, 24 + i * 6, -0.05, 0, Math.PI * 2)
        ctx.fill()
      }
      ctx.restore()

      // Orbit tracks of 3 active satellites (curved arcs)
      ctx.strokeStyle = "rgba(245, 185, 66, 0.35)"
      ctx.setLineDash([4, 6])
      ctx.lineWidth = 1.5
      ctx.beginPath()
      ctx.ellipse(earthCenterX, earthCenterY - 40, w * 0.58, h * 0.42, -0.15, 0, Math.PI * 2)
      ctx.stroke()
      ctx.setLineDash([])

      // Animated orbiting satellite blip 1 (PULSE-OPTIC)
      const satAngle = time * 0.4
      const satX = earthCenterX + Math.cos(satAngle) * (w * 0.52)
      const satY = (earthCenterY - 40) + Math.sin(satAngle) * (h * 0.36)

      // Satellite blip aura
      ctx.fillStyle = "rgba(245, 185, 66, 0.9)"
      ctx.beginPath()
      ctx.arc(satX, satY, 4, 0, Math.PI * 2)
      ctx.fill()

      ctx.fillStyle = "rgba(245, 185, 66, 0.25)"
      ctx.beginPath()
      ctx.arc(satX, satY, 12, 0, Math.PI * 2)
      ctx.fill()

      // Label on satellite blip
      ctx.font = "bold 10px sans-serif"
      ctx.fillStyle = "#F5B942"
      ctx.fillText("PULSE-OPTIC-1", satX + 10, satY - 6)

      animationId = requestAnimationFrame(render)
    }

    render()
    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener("resize", resize)
    }
  }, [])

  // Drag-to-compare mouse & touch listeners
  const handleStartDrag = () => { isDragging.current = true }
  const handleStopDrag = () => { isDragging.current = false }
  const handleMove = (clientX: number) => {
    if (!isDragging.current || !containerRef.current) return
    const rect = containerRef.current.getBoundingClientRect()
    const x = Math.max(0, Math.min(clientX - rect.left, rect.width))
    const pct = Math.round((x / rect.width) * 100)
    setSliderPos(pct)
  }

  // Simulated Tasking Submission
  const handleTaskingSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setTaskingLoading(true)
    setTimeout(() => {
      setTaskingLoading(false)
      setTaskingSuccess(true)
      setTimeout(() => setTaskingSuccess(false), 8000)
    }, 1200)
  }

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 font-sans selection:bg-[#F5B942] selection:text-black antialiased relative overflow-x-hidden">
      {/* 1. FLOATING TUBELIGHT NAVBAR */}
      <NavBar items={navItems} className="fixed top-3 left-1/2 -translate-x-1/2 z-50" />

      {/* 2. HERO SECTION WITH WEBGL/CANVAS EARTH LIMB & SATELLITE PASS CALCULATOR */}
      <section id="hero" className="relative min-h-[92vh] flex flex-col justify-between pt-24 pb-12 px-4 sm:px-8 border-b border-slate-800/80">
        {/* Animated Earth Limb Background Canvas */}
        <canvas
          ref={canvasRef}
          className="absolute inset-0 w-full h-full pointer-events-none z-0"
        />

        {/* Ambient Top Telemetry Bar */}
        <div className="relative z-10 max-w-7xl mx-auto w-full flex flex-wrap items-center justify-between gap-4 py-2 border-b border-slate-800/60 text-xs font-mono text-slate-400">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1.5 text-emerald-400 font-bold bg-emerald-950/60 px-2.5 py-1 rounded-full border border-emerald-500/30">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              18 SATELLITES ON-ORBIT
            </span>
            <span className="hidden sm:inline text-slate-500">|</span>
            <span className="hidden sm:inline">ALT: 518.2 KM LEO</span>
            <span className="hidden md:inline text-slate-500">|</span>
            <span className="hidden md:inline">DOWNLINK: 4.8 GBPS</span>
          </div>

          <div className="flex items-center gap-4">
            <span>SVALBARD GS: <b className="text-slate-200">LOCKED</b></span>
            <span>NEXT SWATH: <b className="text-[#F5B942]">01H 14M</b></span>
          </div>
        </div>

        {/* Center Hero Content */}
        <div className="relative z-10 max-w-5xl mx-auto w-full text-center space-y-6 my-auto pt-8">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-slate-700/80 shadow-2xl backdrop-blur-md text-xs font-semibold tracking-wider text-[#F5B942] uppercase">
            <Radio className="w-3.5 h-3.5 animate-pulse text-[#F5B942]" />
            Continuous Earth-Observation & Energy Flow Reconnaissance
          </div>

          <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-white leading-[1.08]">
            See the World’s Energy Flows <br className="hidden sm:inline" />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-[#F5B942]">
              from Low Earth Orbit
            </span>
          </h1>

          <p className="max-w-3xl mx-auto text-base sm:text-lg text-slate-300 leading-relaxed font-normal">
            Sub-meter optical, cloud-penetrating synthetic aperture radar (SAR), and radiometric thermal surveillance. Track strategic petroleum storage volumes, tanker flotillas across maritime chokepoints, and refinery throughput in real time.
          </p>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <a
              href="#compare"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#F5B942] hover:bg-[#ffc966] text-black font-bold text-sm transition-all transform hover:-translate-y-0.5 shadow-lg shadow-[#F5B942]/20"
            >
              <Sliders className="w-4 h-4" />
              Explore Drag-to-Compare Imagery
            </a>
            <a
              href="#tasking"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-slate-900/90 hover:bg-slate-800 text-white font-semibold text-sm border border-slate-700 transition-all backdrop-blur"
            >
              <Crosshair className="w-4 h-4 text-[#F5B942]" />
              Task a Satellite on Demand
            </a>
          </div>

          {/* Quick Telemetry Indicators */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-8 max-w-4xl mx-auto text-left">
            <div className="bg-slate-950/70 border border-slate-800/80 p-3.5 rounded-xl backdrop-blur-sm">
              <div className="text-[11px] font-mono uppercase text-slate-400">Optical Resolution</div>
              <div className="text-xl font-extrabold text-white">0.30m GSD</div>
              <div className="text-xs text-slate-400">16 Multispectral Bands</div>
            </div>
            <div className="bg-slate-950/70 border border-slate-800/80 p-3.5 rounded-xl backdrop-blur-sm">
              <div className="text-[11px] font-mono uppercase text-slate-400">SAR Radar Capability</div>
              <div className="text-xl font-extrabold text-[#38bdf8]">100% Cloud-Penetrating</div>
              <div className="text-xs text-slate-400">X-Band Day & Night</div>
            </div>
            <div className="bg-slate-950/70 border border-slate-800/80 p-3.5 rounded-xl backdrop-blur-sm">
              <div className="text-[11px] font-mono uppercase text-slate-400">Constellation Revisit</div>
              <div className="text-xl font-extrabold text-[#F5B942]">15-Min Intervals</div>
              <div className="text-xs text-slate-400">Sun-Synchronous LEO</div>
            </div>
            <div className="bg-slate-950/70 border border-slate-800/80 p-3.5 rounded-xl backdrop-blur-sm">
              <div className="text-[11px] font-mono uppercase text-slate-400">Storage Auditing</div>
              <div className="text-xl font-extrabold text-emerald-400">Floating Roof Heights</div>
              <div className="text-xs text-slate-400">$\pm 1.2\%$ Volume Accuracy</div>
            </div>
          </div>
        </div>

        {/* Interactive Pass Telemetry HUD for Cities/Chokepoints */}
        <div className="relative z-10 max-w-4xl mx-auto w-full mt-6 bg-slate-900/80 border border-slate-800 rounded-2xl p-4 backdrop-blur-md shadow-2xl">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3 w-full sm:w-auto">
              <div className="p-2.5 rounded-xl bg-slate-800/90 text-[#F5B942]">
                <Clock className="w-5 h-5 animate-pulse" />
              </div>
              <div>
                <div className="text-xs font-mono uppercase text-slate-400">Next Satellite Pass Over Target</div>
                <div className="text-sm font-bold text-white flex items-center gap-2">
                  <span>{selectedTarget.name}</span>
                  <span className="text-xs font-mono font-normal text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/20">
                    in {selectedTarget.nextPass}
                  </span>
                </div>
              </div>
            </div>

            {/* City Preset Selector */}
            <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
              {PASS_TARGETS.slice(0, 4).map((target) => (
                <button
                  key={target.name}
                  onClick={() => setSelectedTarget(target)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                    selectedTarget.name === target.name
                      ? "bg-[#F5B942] text-black shadow-md"
                      : "bg-slate-800 hover:bg-slate-700 text-slate-300"
                  }`}
                >
                  {target.name.split(" ")[0]}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* 3. INTERACTIVE DRAG-TO-COMPARE SATELLITE IMAGERY SECTION */}
      <section
        id="compare"
        className="py-20 px-4 sm:px-8 max-w-7xl mx-auto border-b border-slate-800"
      >
        <div className="text-center space-y-3 mb-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-500/30 text-cyan-400 text-xs font-mono uppercase">
            <Sliders className="w-3.5 h-3.5" />
            Interactive Sensor Fusion
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            Drag to Compare: Optical vs. Synthetic Aperture Radar (SAR)
          </h2>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base">
            Slide horizontally to inspect how cloud cover vanishes under X-band radar and thermal infrared, revealing crude oil storage tank fill levels and hidden ship wakes.
          </p>
        </div>

        {/* Drag-to-Compare Widget */}
        <div
          ref={containerRef}
          onMouseMove={(e) => handleMove(e.clientX)}
          onTouchMove={(e) => handleMove(e.touches[0].clientX)}
          onMouseDown={handleStartDrag}
          onMouseUp={handleStopDrag}
          onTouchStart={handleStartDrag}
          onTouchEnd={handleStopDrag}
          className="relative w-full aspect-[16/9] max-h-[560px] rounded-2xl overflow-hidden border-2 border-slate-700 select-none cursor-ew-resize shadow-2xl bg-slate-950"
        >
          {/* Layer A (Full Background): Synthetic Aperture Radar & Thermal */}
          <div className="absolute inset-0 bg-[#09131e] flex flex-col justify-between p-6">
            {/* SVG Synthetic SAR Imagery Simulation */}
            <svg className="absolute inset-0 w-full h-full opacity-70" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id="radarGrid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(56, 189, 248, 0.12)" strokeWidth="1" />
                </pattern>
                <radialGradient id="tankGlow" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stopColor="#ef4444" stopOpacity="0.85" />
                  <stop offset="60%" stopColor="#f59e0b" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#082f49" stopOpacity="0.1" />
                </radialGradient>
              </defs>
              <rect width="100%" height="100%" fill="url(#radarGrid)" />

              {/* Simulated Oil Storage Tanks with Thermal/Liquid Depth Highlights */}
              <circle cx="28%" cy="40%" r="55" fill="url(#tankGlow)" stroke="#38bdf8" strokeWidth="2" strokeDasharray="3 3" />
              <circle cx="45%" cy="38%" r="52" fill="url(#tankGlow)" stroke="#38bdf8" strokeWidth="2" strokeDasharray="3 3" />
              <circle cx="62%" cy="42%" r="58" fill="url(#tankGlow)" stroke="#38bdf8" strokeWidth="2" />
              <circle cx="78%" cy="40%" r="50" fill="url(#tankGlow)" stroke="#38bdf8" strokeWidth="2" />

              <circle cx="34%" cy="65%" r="54" fill="url(#tankGlow)" stroke="#38bdf8" strokeWidth="2" />
              <circle cx="52%" cy="68%" r="50" fill="url(#tankGlow)" stroke="#38bdf8" strokeWidth="2" />
              <circle cx="70%" cy="64%" r="56" fill="url(#tankGlow)" stroke="#38bdf8" strokeWidth="2" strokeDasharray="3 3" />

              {/* Tanker Wake in Sea Channel */}
              <path d="M 120 480 Q 220 440, 360 410" stroke="#38bdf8" strokeWidth="3" fill="none" opacity="0.8" />
              <circle cx="360" cy="410" r="8" fill="#38bdf8" />
            </svg>

            <div className="relative z-10 flex items-center justify-between text-xs font-mono">
              <span className="bg-sky-950/90 border border-sky-400/40 text-sky-300 px-3 py-1 rounded-full font-bold">
                📡 SENSOR: X-BAND SAR + LWIR THERMAL
              </span>
              <span className="text-sky-300 font-bold bg-slate-900/90 px-3 py-1 rounded-full">
                PENETRATING CLOUDS: 100% VISIBILITY
              </span>
            </div>

            <div className="relative z-10 bg-slate-900/90 border border-sky-500/30 p-3 rounded-xl max-w-sm text-xs font-mono space-y-1">
              <div className="text-sky-400 font-bold">FLOATING ROOF LIQUID DEPTH AUDIT:</div>
              <div className="text-slate-200">• Tank Cluster 04: <span className="text-emerald-400 font-bold">78.2% Full</span> (942,000 bbl)</div>
              <div className="text-slate-200">• Tank Cluster 05: <span className="text-[#F5B942] font-bold">42.1% Full</span> (-18% Net Outflow)</div>
            </div>
          </div>

          {/* Layer B (Clipped Left Layer): True-Color Optical */}
          <div
            className="absolute inset-0 overflow-hidden"
            style={{ width: `${sliderPos}%` }}
          >
            <div className="absolute inset-0 w-[100vw] max-w-[1280px] h-full bg-[#1e293b] flex flex-col justify-between p-6">
              {/* SVG Optical Imagery with clouds */}
              <svg className="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
                <rect width="100%" height="100%" fill="#1a2530" />
                {/* Coastal landmass */}
                <path d="M 0 0 L 850 0 L 720 560 L 0 560 Z" fill="#2b3b4c" />
                {/* Optical Tanks */}
                <circle cx="28%" cy="40%" r="55" fill="#e2e8f0" stroke="#0f172a" strokeWidth="2" />
                <circle cx="45%" cy="38%" r="52" fill="#cbd5e1" stroke="#0f172a" strokeWidth="2" />
                <circle cx="62%" cy="42%" r="58" fill="#e2e8f0" stroke="#0f172a" strokeWidth="2" />
                <circle cx="78%" cy="40%" r="50" fill="#f8fafc" stroke="#0f172a" strokeWidth="2" />

                <circle cx="34%" cy="65%" r="54" fill="#cbd5e1" stroke="#0f172a" strokeWidth="2" />
                <circle cx="52%" cy="68%" r="50" fill="#e2e8f0" stroke="#0f172a" strokeWidth="2" />
                <circle cx="70%" cy="64%" r="56" fill="#cbd5e1" stroke="#0f172a" strokeWidth="2" />

                {/* Simulated Dense Monsoon Cloud Cover obscuring the optical view */}
                <ellipse cx="40%" cy="45%" rx="240" ry="120" fill="rgba(255,255,255,0.78)" filter="blur(28px)" />
                <ellipse cx="68%" cy="55%" rx="220" ry="140" fill="rgba(255,255,255,0.85)" filter="blur(32px)" />
              </svg>

              <div className="relative z-10 flex items-center justify-between text-xs font-mono">
                <span className="bg-amber-950/90 border border-amber-500/40 text-amber-300 px-3 py-1 rounded-full font-bold">
                  ☀️ SENSOR: 30CM OPTICAL (RGB)
                </span>
                <span className="text-amber-400 font-bold bg-slate-900/90 px-3 py-1 rounded-full">
                  ⚠️ 72% CLOUD OBSCURATION
                </span>
              </div>

              <div className="relative z-10 bg-slate-900/90 border border-amber-500/30 p-3 rounded-xl max-w-sm text-xs font-mono space-y-1">
                <div className="text-amber-400 font-bold">OPTICAL VISIBILITY NOTICE:</div>
                <div className="text-slate-300">Surface visual obstructed by dense atmospheric cloud cover. Switching to SAR is recommended.</div>
              </div>
            </div>
          </div>

          {/* Central Draggable Divider Bar */}
          <div
            className="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_15px_rgba(255,255,255,0.8)] z-30"
            style={{ left: `${sliderPos}%` }}
          >
            <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-9 h-9 rounded-full bg-[#F5B942] text-black flex items-center justify-center font-bold text-xs shadow-2xl border-2 border-white cursor-ew-resize">
              ⟷
            </div>
          </div>
        </div>

        {/* Instructions below widget */}
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mt-4 px-2">
          <span>Target: Ras Tanura Terminal & Tank Battery (Saudi Arabia)</span>
          <span className="text-[#F5B942] animate-pulse">Drag slider horizontally to reveal sub-cloud radar</span>
          <span>Acquisition: 2026-10-16 08:30 UTC</span>
        </div>
      </section>

      {/* 4. SPACECRAFT FLEET & PAYLOAD SPECIFICATIONS */}
      <section id="fleet" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto border-b border-slate-800">
        <div className="text-center space-y-3 mb-14">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-500/30 text-[#F5B942] text-xs font-mono uppercase">
            <Satellite className="w-3.5 h-3.5" />
            Active Orbital Constellation
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            The Spacecraft Fleet & Sensor Architecture
          </h2>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base">
            Equipped with proprietary optical push-broom cameras, polarimetric X-band radar, and dual-band thermal instruments orbiting at 510–530 km.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Fleet Selection Tabs */}
          <div className="lg:col-span-5 space-y-3">
            {FLEET_SPACECRAFT.map((sat) => {
              const Icon = sat.icon
              const isCurrent = activeSat.id === sat.id
              return (
                <button
                  key={sat.id}
                  onClick={() => setActiveSat(sat)}
                  className={`w-full text-left p-4 rounded-xl border transition-all ${
                    isCurrent
                      ? "bg-slate-900 border-[#F5B942] shadow-lg shadow-[#F5B942]/10"
                      : "bg-slate-950/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/60"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div
                        className="p-2.5 rounded-lg"
                        style={{ backgroundColor: `${sat.color}15`, color: sat.color }}
                      >
                        <Icon className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="font-bold text-white text-base">{sat.name}</div>
                        <div className="text-xs text-slate-400 font-mono">{sat.tagline}</div>
                      </div>
                    </div>
                    <span
                      className="text-[10px] font-mono px-2 py-0.5 rounded font-bold"
                      style={{ backgroundColor: `${sat.color}20`, color: sat.color }}
                    >
                      {sat.status}
                    </span>
                  </div>
                </button>
              )
            })}
          </div>

          {/* Right Column: Detailed Telemetry Dossier */}
          <div className="lg:col-span-7 bg-slate-900/90 border border-slate-700/80 rounded-2xl p-6 sm:p-8 backdrop-blur shadow-2xl space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <span className="text-xs font-mono uppercase text-[#F5B942]">PAYLOAD SPECIFICATION</span>
                <h3 className="text-2xl font-bold text-white mt-1">{activeSat.name}</h3>
                <p className="text-xs text-slate-400 font-mono mt-0.5">{activeSat.tagline}</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-slate-400 font-mono">ORBITAL REGIME</span>
                <div className="text-sm font-bold text-emerald-400 font-mono">{activeSat.orbit}</div>
              </div>
            </div>

            <p className="text-sm text-slate-300 leading-relaxed">
              {activeSat.description}
            </p>

            <div className="grid grid-cols-2 gap-4 pt-2">
              <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-xl">
                <div className="text-[11px] font-mono text-slate-400 uppercase">Ground Resolution (GSD)</div>
                <div className="text-base font-extrabold text-white mt-1">{activeSat.gsd}</div>
              </div>
              <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-xl">
                <div className="text-[11px] font-mono text-slate-400 uppercase">Spectral / Radar Band</div>
                <div className="text-base font-extrabold text-[#F5B942] mt-1">{activeSat.bands}</div>
              </div>
              <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-xl">
                <div className="text-[11px] font-mono text-slate-400 uppercase">Swath Width</div>
                <div className="text-base font-extrabold text-white mt-1">{activeSat.swath}</div>
              </div>
              <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-xl">
                <div className="text-[11px] font-mono text-slate-400 uppercase">Revisit Frequency</div>
                <div className="text-base font-extrabold text-emerald-400 mt-1">{activeSat.revisit}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. INTERACTIVE GROUND-TRACK & MARITIME CHOKEPOINT ORBIT MAP */}
      <section id="ground-track" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto border-b border-slate-800">
        <div className="text-center space-y-3 mb-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-emerald-400 text-xs font-mono uppercase">
            <Crosshair className="w-3.5 h-3.5" />
            Live Orbital Telemetry
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            Maritime Chokepoint Ground Tracks
          </h2>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base">
            Real-time orbital propagation tracking satellite passes over the Strait of Hormuz, Bab el-Mandeb, and Malacca Strait.
          </p>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-2xl p-6 shadow-2xl">
          {/* Map canvas / vector SVG visualizer */}
          <div className="relative aspect-[21/9] bg-[#0a101d] rounded-xl overflow-hidden border border-slate-800/80 flex items-center justify-center">
            {/* World Grid & Chokepoint Markers */}
            <svg className="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id="worldGrid" width="30" height="30" patternUnits="userSpaceOnUse">
                  <path d="M 30 0 L 0 0 0 30" fill="none" stroke="rgba(148, 163, 184, 0.08)" strokeWidth="1" />
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill="url(#worldGrid)" />

              {/* Equator */}
              <line x1="0" y1="50%" x2="100%" y2="50%" stroke="rgba(245, 185, 66, 0.3)" strokeDasharray="4 4" strokeWidth="1" />

              {/* Orbital Sinusoidal Ground Track */}
              <path
                d="M 0 350 Q 250 80, 500 250 T 1000 250 T 1500 250"
                stroke="#38bdf8"
                strokeWidth="2.5"
                fill="none"
                strokeDasharray="6 4"
              />

              {/* Swath Scan Width */}
              <path
                d="M 0 370 Q 250 100, 500 270 T 1000 270 T 1500 270 L 1500 230 T 1000 230 T 500 230 Q 250 60, 0 330 Z"
                fill="rgba(56, 189, 248, 0.08)"
              />

              {/* Chokepoint 1: Strait of Hormuz */}
              <circle cx="58%" cy="43%" r="7" fill="#F5B942" className="animate-ping" opacity="0.6" />
              <circle cx="58%" cy="43%" r="4" fill="#F5B942" />
              <text x="59.5%" y="42%" fill="#F5B942" fontSize="11" fontFamily="monospace" fontWeight="bold">HORMUZ (18.5 mbpd)</text>

              {/* Chokepoint 2: Bab el-Mandeb */}
              <circle cx="53%" cy="51%" r="4" fill="#ef4444" />
              <text x="54.5%" y="53%" fill="#ef4444" fontSize="10" fontFamily="monospace">BAB EL-MANDEB</text>

              {/* Chokepoint 3: Malacca Strait */}
              <circle cx="75%" cy="54%" r="4" fill="#10b981" />
              <text x="76.5%" y="54%" fill="#10b981" fontSize="10" fontFamily="monospace">MALACCA (16.2 mbpd)</text>

              {/* Active Satellite on Ground Track */}
              <circle cx="500" cy="250" r="6" fill="#ffffff" />
              <circle cx="500" cy="250" r="14" fill="none" stroke="#38bdf8" strokeWidth="1.5" className="animate-pulse" />
              <text x="515" y="246" fill="#38bdf8" fontSize="11" fontFamily="monospace" fontWeight="bold">PULSE-SAR-X (PASSING)</text>
            </svg>

            {/* Live HUD Overlay */}
            <div className="absolute top-4 left-4 bg-slate-900/90 border border-slate-700/80 p-3 rounded-xl font-mono text-xs space-y-1 backdrop-blur">
              <div className="text-emerald-400 font-bold flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                LIVE CONSTELLATION HUD
              </div>
              <div>SAT: <span className="text-white">PULSE-SAR-X (NORAD 58214)</span></div>
              <div>LAT/LON: <span className="text-[#F5B942]">26.5412° N, 56.2301° E</span></div>
              <div>ALTITUDE: <span className="text-white">518.4 km</span> | VELOCITY: <span className="text-white">7.61 km/s</span></div>
              <div>FOOTPRINT: <span className="text-sky-300">Strait of Hormuz Corridor</span></div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. ON-DEMAND SATELLITE TASKING FORM */}
      <section id="tasking" className="py-20 px-4 sm:px-8 max-w-4xl mx-auto border-b border-slate-800">
        <div className="text-center space-y-3 mb-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-950/60 border border-red-500/30 text-red-400 text-xs font-mono uppercase">
            <Crosshair className="w-3.5 h-3.5" />
            Tasking on Demand
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            Task a Reconnaissance Satellite
          </h2>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base">
            Order custom high-resolution optical or SAR radar imaging over any energy facility, port, or chokepoint worldwide with priority downlink.
          </p>
        </div>

        <form onSubmit={handleTaskingSubmit} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6 shadow-2xl backdrop-blur">
          <div className="space-y-2">
            <label className="text-xs font-mono uppercase text-slate-300 font-bold">1. Area of Interest (AOI)</label>
            <select
              value={taskingAoi}
              onChange={(e) => setTaskingAoi(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-[#F5B942]"
            >
              <option value="Strait of Hormuz (26.56° N, 56.25° E)">Strait of Hormuz — Critical Seaborne Oil Conduit</option>
              <option value="Jamnagar Refinery, India (22.47° N, 70.06° E)">Jamnagar Refining Complex — 1.24 mbpd Refining Hub</option>
              <option value="Ras Tanura, Saudi Arabia (26.64° N, 50.16° E)">Ras Tanura Oil Terminal & Offshore Berths</option>
              <option value="Fujairah Anchorage (25.13° N, 56.33° E)">Fujairah Commercial Bunkering & Storage</option>
              <option value="Cushing Storage Hub, USA (35.98° N, -96.76° E)">Cushing Crude Storage Tank Battery</option>
              <option value="Malacca Strait (1.29° N, 103.85° E)">Malacca Strait & Singapore Petroleum Anchorage</option>
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-xs font-mono uppercase text-slate-300 font-bold">2. Imaging Sensor</label>
              <select
                value={taskingSensor}
                onChange={(e) => setTaskingSensor(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-[#F5B942]"
              >
                <option value="PULSE-OPTIC (30cm Optical)">PULSE-OPTIC (30cm 16-Band Visual)</option>
                <option value="PULSE-SAR-X (All-Weather Radar)">PULSE-SAR-X (50cm Cloud-Penetrating Radar)</option>
                <option value="PULSE-THERMAL (Infrared)">PULSE-THERMAL (Radiometric Flare & Flue Analysis)</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-mono uppercase text-slate-300 font-bold">3. Revisit Priority</label>
              <select
                value={taskingPriority}
                onChange={(e) => setTaskingPriority(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-[#F5B942]"
              >
                <option value="Emergency Rush (< 3h)">Emergency Rush — Immediate Orbit Re-tasking (&lt; 3h)</option>
                <option value="Next Scheduled Pass (< 12h)">Next Scheduled Pass (&lt; 12h)</option>
                <option value="Standard Daily Monitoring">Standard Daily Monitoring (24h)</option>
              </select>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-400 space-y-1">
            <div className="text-emerald-400 font-bold">ESTIMATED TASKING TELEMETRY:</div>
            <div>• Next Pass Window: <span className="text-white font-bold">01h 14m</span> (Sun Elevation: 68.4°)</div>
            <div>• Ground Sampling Distance: <span className="text-white font-bold">0.30m Optical GSD</span></div>
            <div>• Downlink Relay: <span className="text-white font-bold">Direct to Secure Cloud (AES-256)</span></div>
          </div>

          <button
            type="submit"
            disabled={taskingLoading}
            className="w-full py-4 rounded-xl bg-[#F5B942] hover:bg-[#ffc966] text-black font-extrabold text-sm uppercase tracking-wider transition-all shadow-xl shadow-[#F5B942]/20 disabled:opacity-50"
          >
            {taskingLoading ? "CALCULATING ORBIT PASS & LOCKING TARGET..." : "⚡ DISPATCH SATELLITE TASKING REQUEST"}
          </button>

          {taskingSuccess && (
            <div className="p-4 rounded-xl bg-emerald-950/80 border border-emerald-500/50 text-emerald-300 text-sm font-mono flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
              <div>
                <b>TASKING ORDER CONFIRMED:</b> Satellite <span className="text-white">{taskingSensor}</span> queued for pass over <span className="text-white">{taskingAoi.split("—")[0]}</span>. Imagery delivered in 01h 14m.
              </div>
            </div>
          )}
        </form>
      </section>

      {/* 7. IMAGERY ARCHIVE CATALOG CAROUSEL */}
      <section id="catalog" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto border-b border-slate-800">
        <div className="text-center space-y-3 mb-12">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-500/30 text-purple-400 text-xs font-mono uppercase">
            <Layers className="w-3.5 h-3.5" />
            Declassified Energy Intelligence
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            High-Resolution Satellite Archive Catalog
          </h2>
          <p className="max-w-2xl mx-auto text-slate-400 text-sm sm:text-base">
            Explore verified orbital captures of strategic storage tank farms, oil refinery flaring, and chokepoint vessel densities.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {ARCHIVE_ITEMS.map((item, idx) => (
            <div
              key={idx}
              className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-4 hover:border-slate-700 transition-all shadow-xl flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="w-full aspect-[4/3] rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center relative overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-tr from-sky-950/40 via-transparent to-amber-950/30" />
                  <Satellite className="w-10 h-10 text-slate-700 animate-pulse" />
                  <span className="absolute bottom-2 left-2 text-[10px] font-mono bg-black/80 px-2 py-0.5 rounded text-[#F5B942]">
                    {item.resolution}
                  </span>
                  <span className="absolute top-2 right-2 text-[10px] font-mono bg-emerald-950/80 border border-emerald-500/30 px-2 py-0.5 rounded text-emerald-400">
                    {item.date}
                  </span>
                </div>

                <div>
                  <h4 className="font-bold text-white text-base leading-snug">{item.title}</h4>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">{item.location}</p>
                </div>

                <div className="text-xs font-mono text-emerald-400 font-bold bg-slate-950 p-2 rounded-lg border border-slate-800/80">
                  {item.metric}
                </div>
              </div>

              <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-800">
                {item.tags.map((tag, tIdx) => (
                  <span key={tIdx} className="text-[10px] font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-300">
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 8. FOOTER WITH LIVE TELEMETRY STATUS */}
      <footer className="py-12 px-4 sm:px-8 max-w-7xl mx-auto text-xs font-mono text-slate-500 space-y-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
          <div className="flex items-center gap-2 text-white font-bold text-sm">
            <Globe2 className="w-5 h-5 text-[#F5B942]" />
            GLOBAL FUELPULSE AI — SATELLITE EARTH OBSERVATION RADAR
          </div>

          <div className="flex items-center gap-6 text-slate-400">
            <span>NORAD ID: 58214</span>
            <span>UPLINK: ACTIVE</span>
            <span>STATUS: 99.98% HEALTH</span>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
          <p>© 2026 Global FuelPulse AI. Satellite Imaging & Earth-Observation Intelligence Engine.</p>
          <div className="flex gap-4">
            <a href="#hero" className="hover:text-white transition-colors">Orbit View</a>
            <a href="#compare" className="hover:text-white transition-colors">Drag to Compare</a>
            <a href="#fleet" className="hover:text-white transition-colors">Fleet Hardware</a>
            <a href="#tasking" className="hover:text-white transition-colors">Tasking Form</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
