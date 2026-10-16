"use client";

import React from "react";
import { Home, User, Briefcase, FileText } from "lucide-react";
import { NavBar } from "@/components/ui/tubelight-navbar";
import { BackgroundPaths } from "@/components/ui/background-paths";
import { AnimatedGrid } from "@/components/ui/animated-grid";
import { Component as GlowButton } from "@/components/ui/glow-button";
import { AuthComponent } from "@/components/ui/sign-up";

// A simple placeholder logo for demonstration
const CustomLogo = () => (
  <div className="bg-blue-500 text-white rounded-md p-1.5">
    <svg 
      className="h-4 w-4" 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    >
      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
    </svg>
  </div>
);

export function CustomAuthDemo() {
  return (
    <AuthComponent 
      logo={<CustomLogo />} 
      brandName="MyWebApp" 
    />
  );
}

export function GlowButtonDemo() {
  return (
    <div className="flex h-screen w-screen items-center justify-center bg-background text-foreground">
      <GlowButton label="Generate Intelligence" />
    </div>
  );
}

export function AnimatedGridDemo() {
  return (
    <div className="relative h-screen w-full overflow-hidden bg-background">
      <AnimatedGrid />
      <div className="relative z-10 flex h-full w-full flex-col items-center justify-center gap-2 text-center">
        <h1 className="text-4xl font-semibold tracking-tight text-foreground">
          Build faster.
        </h1>
        <p className="max-w-md text-muted-foreground">
          A CSS-only animated grid backdrop for heroes and section backgrounds.
        </p>
      </div>
    </div>
  );
}

export function DemoBackgroundPaths() {
  return <BackgroundPaths title="Background Paths" />;
}

export function NavBarDemo() {
  const navItems = [
    { name: "Home", url: "#", icon: Home },
    { name: "About", url: "#", icon: User },
    { name: "Projects", url: "#", icon: Briefcase },
    { name: "Resume", url: "#", icon: FileText },
  ];

  return <NavBar items={navItems} />;
}

export default function Default() {
  return <CustomAuthDemo />;
}
