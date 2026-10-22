import { useEffect, useMemo, useState } from "react";

import { BRAND } from "../brand";
import { ThemeContext } from "./themeContext";

const STORAGE_KEY = `${BRAND.slug}-theme-mode`;
const MODES = ["light", "dark", "system"];
const LIGHT_QUERY = "(prefers-color-scheme: light)";

const systemTheme = () =>
  window.matchMedia?.(LIGHT_QUERY).matches ? "light" : "dark";

function initialMode() {
  const stored = localStorage.getItem(STORAGE_KEY);
  return MODES.includes(stored) ? stored : "system";
}

export function ThemeProvider({ children }) {
  const [mode, setMode] = useState(initialMode);
  const [osTheme, setOsTheme] = useState(systemTheme);

  // Follow the operating-system preference while mode is "system".
  useEffect(() => {
    const query = window.matchMedia?.(LIGHT_QUERY);
    if (!query) return undefined;

    const onChange = () => setOsTheme(query.matches ? "light" : "dark");
    query.addEventListener("change", onChange);
    return () => query.removeEventListener("change", onChange);
  }, []);

  const theme = mode === "system" ? osTheme : mode;

  useEffect(() => {
    document.documentElement.classList.toggle("theme-light", theme === "light");
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, mode);
  }, [theme, mode]);

  const value = useMemo(
    () => ({
      theme,
      mode,
      setMode,
      toggleTheme: () => setMode(theme === "dark" ? "light" : "dark"),
    }),
    [theme, mode]
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
