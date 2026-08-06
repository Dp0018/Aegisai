"use client";

import React from "react";
import { useTheme } from "./ThemeProvider";

export function ThemeToggle() {
    const { theme, toggleTheme } = useTheme();

    return (
        <button
            onClick={toggleTheme}
            className="relative flex h-10 w-10 items-center justify-center rounded-lg border border-border bg-card/60 text-foreground shadow-sm backdrop-blur-md transition-all hover:bg-accent hover:text-accent-foreground active:scale-95"
            aria-label="Toggle Theme"
        >
            {theme === "dark" ? (
                // Sun Icon (when in dark mode)
                <svg className="h-[1.2rem] w-[1.2rem] transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
                </svg>
            ) : (
                // Moon Icon (when in light mode)
                <svg className="h-[1.2rem] w-[1.2rem] transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
            )}
        </button>
    );
}
