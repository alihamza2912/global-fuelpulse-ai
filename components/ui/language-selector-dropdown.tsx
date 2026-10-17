import { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";
import { ChevronDown, Check } from "lucide-react";

export interface Language {
  code: string;
  label: string;
  flag: string;
}

export const languages: Language[] = [
  { code: "en", label: "English", flag: "🇺🇸" },
  { code: "zh-CN", label: "简体中文", flag: "🇨🇳" },
  { code: "zh-TW", label: "繁體中文", flag: "🇨🇳" },
  { code: "ja", label: "日本語", flag: "🇯🇵" },
  { code: "es", label: "Español", flag: "🇪🇸" },
  { code: "fr", label: "Français", flag: "🇫🇷" },
  { code: "pt-BR", label: "Português (BR)", flag: "🇧🇷" },
  { code: "ko", label: "한국어", flag: "🇰🇷" },
  { code: "ru", label: "Русский", flag: "🇷🇺" },
  { code: "tr", label: "Türkçe", flag: "🇹🇷" },
  { code: "id", label: "Bahasa Indonesia", flag: "🇮🇩" },
  { code: "de", label: "Deutsch", flag: "🇩🇪" },
  { code: "fa", label: "فارسی", flag: "🇮🇷" },
];

export interface LanguageSelectorDropdownProps {
  initialLanguage?: Language;
  onLanguageChange?: (lang: Language) => void;
  className?: string;
}

export const Component = ({
  initialLanguage,
  onLanguageChange,
  className
}: LanguageSelectorDropdownProps = {}) => {
  const [selected, setSelected] = useState<Language>(initialLanguage || languages[0]);
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (lang: Language) => {
    setSelected(lang);
    setOpen(false);
    if (onLanguageChange) {
      onLanguageChange(lang);
    }
  };

  return (
    <div className={cn("relative inline-block", className)} ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className={cn(
          "flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm",
          "bg-white/60 dark:bg-neutral-900/90 backdrop-blur-md shadow-sm",
          "border-gray-200 dark:border-neutral-700",
          "text-gray-800 dark:text-neutral-200",
          "hover:bg-gray-50 dark:hover:bg-neutral-800 transition-all",
          "focus:outline-none focus:ring-2 focus:ring-blue-500/20"
        )}
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <span>{selected.flag}</span>
        <span>{selected.label}</span>
        <ChevronDown className={cn("h-4 w-4 transition-transform duration-200", open && "rotate-180")} />
      </button>

      {/* Dropdown Menu */}
      {open && (
        <div
          className={cn(
            "absolute left-0 mt-2 w-48 rounded-xl overflow-hidden z-50",
            "bg-white/90 dark:bg-neutral-900/95 backdrop-blur-xl",
            "shadow-lg border border-gray-200 dark:border-neutral-700",
            "animate-fade-in py-1"
          )}
          role="listbox"
        >
          {languages.map((lang) => (
            <button
              key={lang.code}
              type="button"
              onClick={() => handleSelect(lang)}
              className={cn(
                "flex items-center gap-2 w-full px-3 py-2 text-sm text-left transition-colors",
                selected.code === lang.code
                  ? "font-semibold text-blue-600 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-950/30"
                  : "text-gray-800 dark:text-neutral-200 hover:bg-gray-100 dark:hover:bg-neutral-800"
              )}
              role="option"
              aria-selected={selected.code === lang.code}
            >
              <span>{lang.flag}</span>
              <span className="flex-1">{lang.label}</span>
              {selected.code === lang.code && (
                <Check className="h-4 w-4 text-blue-500 dark:text-blue-400" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export const LanguageSelectorDropdown = Component;
export default Component;
