import React from "react"
import { HeroWithMockup } from "@/components/ui/hero-with-mockup"
import { TreeNav } from "@/components/ui/tree-nav"

export function HeroDemo() {
  return (
    <HeroWithMockup
      title="Build AI-powered apps in minutes, not months"
      description="Create sophisticated AI applications with our intuitive platform. No ML expertise required."
      primaryCta={{
        text: "Start Building",
        href: "/signup",
      }}
      secondaryCta={{
        text: "View on GitHub",
        href: "https://github.com/your-ai-platform",
      }}
      mockupImage={{
        alt: "AI Platform Dashboard",
        width: 1248,
        height: 765,
        src: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
      }}
    />
  )
}

const TREE_ITEMS = [
  { label: "Overview", href: "#overview" },
  { label: "Installation", href: "#installation" },
  { label: "Usage", href: "#usage" },
  { label: "Theming", href: "#theming", badge: "New" },
  { label: "Accessibility", href: "#accessibility" },
  { label: "Changelog", href: "#changelog" },
];

export function TreeNavDemo() {
  const [active, setActive] = React.useState(TREE_ITEMS[0].href);

  return (
    <div className="flex w-full justify-center py-8">
      <TreeNav
        className="w-full max-w-[240px]"
        items={TREE_ITEMS}
        activeHref={active}
        onSelect={(item, event) => {
          event.preventDefault();
          setActive(item.href);
        }}
      />
    </div>
  );
}

export default TreeNavDemo;
