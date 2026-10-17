import * as React from "react";
import { cn } from "@/lib/utils";

export interface NewsGlobeIconProps extends React.SVGProps<SVGSVGElement> {
  size?: number | string;
  className?: string;
}

export const NewsGlobeIcon: React.FC<NewsGlobeIconProps> = ({
  size = 36,
  className,
  ...props
}) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={cn("inline-block shrink-0", className)}
      role="img"
      aria-label="News Globe Icon"
      {...props}
    >
      {/* Left Ribbon Back Fold */}
      <path d="M 10 50 C 10 59 18 64 22 64 L 22 52 Z" fill="#9F1239" />
      {/* Right Ribbon Back Fold */}
      <path d="M 90 50 C 90 59 82 64 78 64 L 78 52 Z" fill="#9F1239" />

      {/* Globe Sphere */}
      <circle cx="50" cy="50" r="34" fill="#38BDF8" />

      {/* Globe Coordinate Grid Lines */}
      <line x1="50" y1="16" x2="50" y2="84" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" />
      <line x1="16" y1="50" x2="84" y2="50" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" />
      <path d="M 23 34 Q 50 42 77 34" fill="none" stroke="#FFFFFF" strokeWidth="2.2" strokeLinecap="round" />
      <path d="M 23 66 Q 50 58 77 66" fill="none" stroke="#FFFFFF" strokeWidth="2.2" strokeLinecap="round" />
      <path d="M 50 16 C 34 16 28 32 28 50 C 28 68 34 84 50 84" fill="none" stroke="#FFFFFF" strokeWidth="2.2" />
      <path d="M 50 16 C 66 16 72 32 72 50 C 72 68 66 84 50 84" fill="none" stroke="#FFFFFF" strokeWidth="2.2" />
      <circle cx="50" cy="50" r="34" fill="none" stroke="#0284C7" strokeWidth="1.8" />

      {/* Ribbon Side Folds Under (Dark Crimson) */}
      <path d="M 16 58 C 14 62 16 66 22 66 L 22 58 Z" fill="#881337" />
      <path d="M 84 58 C 86 62 84 66 78 66 L 78 58 Z" fill="#881337" />

      {/* Central Red NEWS Banner */}
      <rect x="14" y="37" width="72" height="26" rx="4" fill="#EF4444" />

      {/* Text: NEWS */}
      <text
        x="50"
        y="55.5"
        fontFamily="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
        fontWeight="900"
        fontSize="16"
        fill="#FFFFFF"
        textAnchor="middle"
        letterSpacing="0.5"
      >
        NEWS
      </text>
    </svg>
  );
};

export default NewsGlobeIcon;
