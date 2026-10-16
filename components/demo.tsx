"use client";

import { Home, User, Briefcase, FileText } from "lucide-react";
import { NavBar } from "@/components/ui/tubelight-navbar";
import { BackgroundPaths } from "@/components/ui/background-paths";
import { AnimatedGrid } from "@/components/ui/animated-grid";

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

export default AnimatedGridDemo;
