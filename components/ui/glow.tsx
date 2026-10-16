import React from "react"
import { cn } from "@/lib/utils"
import { cva, type VariantProps } from "class-variance-authority"

const glowVariants = cva("absolute w-full pointer-events-none flex items-center justify-center", {
  variants: {
    variant: {
      top: "top-0",
      above: "-top-[128px]",
      bottom: "bottom-0",
      below: "-bottom-[128px]",
      center: "top-1/2 -translate-y-1/2",
    },
  },
  defaultVariants: {
    variant: "top",
  },
})

export interface GlowProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof glowVariants> {}

export function Glow({ className, variant, ...props }: GlowProps) {
  return (
    <div
      className={cn(glowVariants({ variant }), className)}
      {...props}
    >
      <div className="w-[850px] h-[350px] bg-gradient-to-r from-brand/20 via-brand/40 to-brand/20 blur-[120px] rounded-full dark:from-brand/30 dark:via-brand/50 dark:to-brand/30" />
    </div>
  )
}
