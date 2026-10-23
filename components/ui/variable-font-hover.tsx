"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export interface VariableFontHoverProps {
  label: string;
  className?: string;
  fromWeight?: number;
  toWeight?: number;
  color?: string;
  hoverColor?: string;
  onClick?: () => void;
  children?: React.ReactNode;
  icon?: React.ReactNode;
}

/**
 * VariableFontHover component
 * Provides subtle variable-font weight interpolation on hover and keyboard focus,
 * preventing layout shift by leveraging font-variation-settings and restrained scaling.
 */
export function VariableFontHover({
  label,
  className,
  fromWeight = 500,
  toWeight = 700,
  color = "#94A3B8",
  hoverColor = "#FFFFFF",
  onClick,
  children,
  icon,
}: VariableFontHoverProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.button
      type="button"
      onClick={onClick}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      onFocus={() => setIsHovered(true)}
      onBlur={() => setIsHovered(false)}
      className={cn(
        "relative inline-flex items-center justify-center gap-1.5 px-3.5 py-1.5 text-xs rounded-full outline-none select-none",
        "bg-white/[0.03] hover:bg-white/[0.08] border border-white/10 hover:border-amber-400/35",
        "focus-visible:ring-2 focus-visible:ring-amber-400/50 shadow-none transition-colors duration-200",
        className
      )}
      style={{
        fontVariationSettings: `'wght' ${isHovered ? toWeight : fromWeight}`,
        fontWeight: isHovered ? toWeight : fromWeight,
        color: isHovered ? hoverColor : color,
        transition:
          "font-variation-settings 0.25s cubic-bezier(0.16, 1, 0.3, 1), font-weight 0.25s ease, color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease",
      }}
    >
      {icon && <span className="opacity-90">{icon}</span>}
      <span>{children || label}</span>
    </motion.button>
  );
}

export default VariableFontHover;
