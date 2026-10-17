import * as React from "react";
import { NewsGlobeIcon } from "./news-globe-icon";

export const NewsGlobeDemo: React.FC = () => {
  return (
    <div className="flex flex-col gap-4 p-6 bg-[#070A12] text-white rounded-xl border border-white/10">
      <h3 className="text-lg font-bold">News Globe Icon Integrations</h3>
      <div className="flex flex-wrap items-center gap-4">
        {/* Header Action Button (Classic 42px Matte Yellow with 36px Icon) */}
        <button className="h-[42px] px-4 bg-[#EAB308] hover:bg-[#FACC15] text-[#070A12] font-black text-xs uppercase tracking-wider rounded-md inline-flex items-center gap-2 border border-[#CA8A04] transition-all cursor-pointer">
          <NewsGlobeIcon size={36} />
          <span>LIVE NEWS (18)</span>
        </button>

        {/* Dark Obsidian Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#0E1526] border border-white/15 text-xs font-semibold text-slate-200">
          <NewsGlobeIcon size={16} />
          <span>GLOBAL WIRE 24/7</span>
        </div>

        {/* Large Display */}
        <NewsGlobeIcon size={44} />
      </div>
    </div>
  );
};

export default NewsGlobeDemo;
