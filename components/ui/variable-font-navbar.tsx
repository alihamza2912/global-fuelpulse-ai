"use client";

import React, { useState } from "react";
import { Newspaper, Bot, Globe, User, LogIn } from "lucide-react";
import { VariableFontHover } from "./variable-font-hover";
import { cn } from "@/lib/utils";

export interface NavbarProps {
  newsCount?: number;
  aiQuotaUsed?: number;
  aiQuotaLimit?: number;
  currentLanguage?: string;
  userName?: string | null;
  onOpenNews?: () => void;
  onOpenAI?: () => void;
  onOpenLanguage?: () => void;
  onOpenAccount?: () => void;
  className?: string;
}

/**
 * Global FuelPulse AI — Premium Custom Navbar
 * Left: Fuel/Energy logo + GLOBAL FUELPULSE AI + GLOBAL ENERGY INTELLIGENCE
 * Right: Exactly four controls [News, AI Analyst, Language, User Account]
 */
export function GlobalFuelPulseNavbar({
  newsCount = 4,
  aiQuotaUsed = 0,
  aiQuotaLimit = 3,
  currentLanguage = "EN",
  userName = null,
  onOpenNews,
  onOpenAI,
  onOpenLanguage,
  onOpenAccount,
  className,
}: NavbarProps) {
  const remainingQuota = Math.max(0, aiQuotaLimit - aiQuotaUsed);

  return (
    <header
      className={cn(
        "w-full h-14 px-4 md:px-6 flex items-center justify-between",
        "bg-[#080D1A]/95 backdrop-blur-md border-b border-white/[0.08]",
        className
      )}
    >
      {/* Left: Brand Lockup */}
      <div className="flex items-center gap-3 select-none">
        <div className="w-8 h-8 rounded-md bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center shadow-sm">
          <span className="text-[#0B101E] font-extrabold text-xs tracking-tight">FP</span>
        </div>
        <div className="flex flex-col">
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-bold tracking-tight text-white uppercase font-sans">
              Global FuelPulse
            </span>
            <span className="bg-amber-400 text-[#070A12] text-[10px] font-black px-1.5 py-0.5 rounded tracking-wider">
              AI
            </span>
          </div>
          <span className="text-[10px] font-semibold text-slate-400 tracking-wider uppercase">
            Global Energy Intelligence
          </span>
        </div>
      </div>

      {/* Right: Exactly 4 Controls [News, AI Analyst, Language, Account] */}
      <div className="flex items-center gap-2">
        {/* 1. News */}
        <VariableFontHover
          label={`News (${newsCount})`}
          icon={<Newspaper className="w-3.5 h-3.5 text-amber-400" />}
          onClick={onOpenNews}
          fromWeight={500}
          toWeight={700}
        />

        {/* 2. AI Analyst */}
        <VariableFontHover
          label={`AI (${remainingQuota}/${aiQuotaLimit})`}
          icon={<Bot className="w-3.5 h-3.5 text-emerald-400" />}
          onClick={onOpenAI}
          fromWeight={500}
          toWeight={700}
        />

        {/* 3. Language */}
        <button
          type="button"
          onClick={onOpenLanguage}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white rounded-full bg-white/[0.03] hover:bg-white/[0.08] border border-white/10 transition-colors duration-150 outline-none"
        >
          <Globe className="w-3.5 h-3.5 text-slate-400" />
          <span>{currentLanguage} ▾</span>
        </button>

        {/* 4. User Account / User ID */}
        <button
          type="button"
          onClick={onOpenAccount}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white rounded-full bg-white/[0.03] hover:bg-white/[0.08] border border-white/10 transition-colors duration-150 outline-none"
        >
          {userName ? (
            <>
              <User className="w-3.5 h-3.5 text-emerald-400" />
              <span>{userName}</span>
            </>
          ) : (
            <>
              <LogIn className="w-3.5 h-3.5 text-amber-400" />
              <span>Sign In</span>
            </>
          )}
        </button>
      </div>
    </header>
  );
}

export default GlobalFuelPulseNavbar;
