"use client";

import React from "react";

export function Logo({ className = "h-10 w-10" }: { className?: string }) {
    return (
        <svg
            className={className}
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <defs>
                {/* Clean enterprise blue / cyan gradients */}
                <linearGradient id="logoipsum-ring-1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#2563eb" />
                    <stop offset="100%" stopColor="#0ea5e9" />
                </linearGradient>
                <linearGradient id="logoipsum-ring-2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#0284c7" />
                    <stop offset="100%" stopColor="#06b6d4" />
                </linearGradient>
                <linearGradient id="logoipsum-ring-3" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#0f766e" />
                    <stop offset="100%" stopColor="#0284c7" />
                </linearGradient>
            </defs>

            {/* Ring 1 (Top Node) */}
            <circle cx="50" cy="38" r="20" stroke="url(#logoipsum-ring-1)" strokeWidth="6.5" />

            {/* Ring 2 (Bottom Left Node) with dynamic background-colored stroke mask for 3D gap */}
            <circle cx="37" cy="58" r="20" stroke="var(--background)" strokeWidth="11.5" />
            <circle cx="37" cy="58" r="20" stroke="url(#logoipsum-ring-2)" strokeWidth="6.5" />

            {/* Ring 3 (Bottom Right Node) with dynamic background-colored stroke mask for 3D gap */}
            <circle cx="63" cy="58" r="20" stroke="var(--background)" strokeWidth="11.5" />
            <circle cx="63" cy="58" r="20" stroke="url(#logoipsum-ring-3)" strokeWidth="6.5" />

            {/* Redraw Top-Right Arc of Ring 1 to create the interlocking weave */}
            <path
                d="M50 18 A 20 20 0 0 1 70 38"
                stroke="url(#logoipsum-ring-1)"
                strokeWidth="6.5"
                strokeLinecap="round"
            />
        </svg>
    );
}
