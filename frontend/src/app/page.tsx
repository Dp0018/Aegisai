"use client";

import React from "react";
import { useAuth } from "@/features/auth/hooks/useAuth";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function Home() {
    const { user, logout } = useAuth();

    if (!user) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-background text-muted-foreground">
                <div className="flex flex-col items-center gap-2">
                    <svg className="h-8 w-8 animate-spin text-primary" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    <span>Verifying session...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="relative min-h-screen bg-background font-sans text-foreground antialiased transition-colors duration-200">
            {/* Dynamic Background Grid */}
            <div 
                className="absolute inset-0 opacity-[0.15] dark:opacity-[0.2]"
                style={{
                    backgroundImage: `linear-gradient(to right, var(--border) 1px, transparent 1px), linear-gradient(to bottom, var(--border) 1px, transparent 1px)`,
                    backgroundSize: "4rem 4rem",
                    maskImage: "radial-gradient(ellipse 60% 50% at 50% 50%, #000 60%, transparent 100%)",
                    WebkitMaskImage: "radial-gradient(ellipse 60% 50% at 50% 50%, #000 60%, transparent 100%)",
                }}
            />

            <header className="relative z-10 border-b border-border bg-card/40 backdrop-blur-md">
                <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
                    <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-primary-foreground font-bold shadow-md">
                            A
                        </div>
                        <span className="text-xl font-bold tracking-tight text-foreground">AegisAI</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="flex flex-col text-right">
                            <span className="text-sm font-semibold text-foreground">{user.full_name}</span>
                            <span className="text-xs text-muted-foreground capitalize">{user.role} role</span>
                        </div>
                        <ThemeToggle />
                        <button
                            onClick={() => logout()}
                            className="rounded-lg border border-border bg-muted/30 px-4 py-2 text-sm font-medium text-foreground transition-all hover:bg-accent hover:text-accent-foreground active:scale-95"
                        >
                            Log Out
                        </button>
                    </div>
                </div>
            </header>

            <main className="relative z-10 mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
                <div className="rounded-2xl border border-border/80 bg-card/30 p-8 shadow-xl backdrop-blur-xl md:p-12">
                    <div className="max-w-2xl">
                        <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold tracking-wide text-primary">
                            Authentication Verified
                        </span>
                        <h1 className="mt-4 text-4xl font-extrabold tracking-tight text-foreground md:text-5xl">
                            AegisAI Console
                        </h1>
                        <p className="mt-4 text-lg leading-relaxed text-muted-foreground">
                            Welcome, <strong className="text-foreground">{user.full_name}</strong>. You have logged in successfully as an <span className="capitalize font-semibold text-primary">{user.role}</span>.
                        </p>
                        <p className="mt-2 text-sm text-muted-foreground/80">
                            Session User ID: {user.id}
                        </p>
                        <div className="mt-8 border-t border-border pt-8">
                            <h2 className="text-lg font-semibold text-foreground">Ready for Dashboard Features</h2>
                            <p className="mt-1 text-sm text-muted-foreground">
                                This placeholder confirms the client API token rotation, route guards, dark/light theme config, and auth context logic is 100% operational. Next, we will connect the main operators chat controls.
                            </p>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
