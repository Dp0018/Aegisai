"use client";

import React from "react";
import { BarChart3, Terminal } from "lucide-react";

export default function AnalyticsPage() {
    return (
        <div className="relative min-h-[70vh] flex flex-col items-center justify-center text-center p-6">
            <div className="absolute -top-12 -left-12 h-64 w-64 rounded-full bg-primary/5 blur-3xl dark:bg-primary/5" />
            
            <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 text-primary shadow-sm border border-primary/20 mb-6">
                <BarChart3 className="h-8 w-8" />
            </div>

            <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
                Retrieval Analytics
            </h1>
            <p className="mt-2 max-w-sm text-sm text-muted-foreground leading-relaxed">
                Analyze semantic similarity metrics, chunk relevance, and vector database query loads. Graph charts coming soon.
            </p>

            <div className="mt-8 flex items-center gap-2 rounded-lg border border-border bg-card/60 px-4 py-2 font-mono text-xs text-muted-foreground shadow-sm">
                <Terminal className="h-3.5 w-3.5 text-primary" />
                <span>status: ANALYZING_PINECONE_INDEX</span>
            </div>
        </div>
    );
}
