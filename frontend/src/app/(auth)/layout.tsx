import { Logo } from "@/components/Logo";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Shield, GitFork, Database, Activity, CheckCircle2 } from "lucide-react";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="relative flex min-h-screen w-full flex-col bg-background text-foreground transition-colors duration-200 md:flex-row">
            
            {/* Left Panel: Enterprise Architecture & Platform Summary (Hidden on Mobile) */}
            <div className="relative hidden flex-1 flex-col justify-between overflow-hidden border-r border-border/60 bg-zinc-950 p-12 text-white dark:bg-black md:flex">
                {/* Background Grid Pattern */}
                <div 
                    className="absolute inset-0 opacity-10"
                    style={{
                        backgroundImage: `linear-gradient(to right, var(--border) 1px, transparent 1px), linear-gradient(to bottom, var(--border) 1px, transparent 1px)`,
                        backgroundSize: "2.5rem 2.5rem",
                    }}
                />
                
                {/* Top Brand Block */}
                <div className="relative z-10 flex items-center gap-3">
                    <Logo className="h-10 w-10 shrink-0" />
                    <div>
                        <span className="text-xl font-bold tracking-tight">AegisAI</span>
                        <span className="block text-[11px] font-medium text-zinc-400">Enterprise GenAI Platform</span>
                    </div>
                </div>

                {/* Center Content: Architecture Pipeline Overview */}
                <div className="relative z-10 my-auto max-w-lg space-y-6">
                    <div className="space-y-2">
                        <div className="inline-flex items-center gap-2 rounded-md border border-primary/30 bg-primary/10 px-2.5 py-1 text-xs font-semibold text-primary">
                            <Shield className="h-3.5 w-3.5" />
                            Deterministic Agent Governance
                        </div>
                        <h2 className="text-3xl font-bold tracking-tight text-white">
                            Autonomous agents with human oversight.
                        </h2>
                        <p className="text-sm leading-relaxed text-zinc-400">
                            AegisAI runs multi-agent workflows with structured verification gates, continuous Kafka telemetry, and vector indexing.
                        </p>
                    </div>

                    {/* Architecture Pipeline Deck */}
                    <div className="space-y-2.5 rounded-lg border border-white/10 bg-white/[0.03] p-4 text-xs">
                        <div className="text-[11px] font-semibold uppercase tracking-wider text-zinc-400">
                            Core Pipeline Architecture
                        </div>

                        <div className="grid grid-cols-2 gap-2 pt-1">
                            <div className="flex items-start gap-2.5 rounded-md border border-white/5 bg-white/[0.02] p-2.5">
                                <GitFork className="mt-0.5 h-4 w-4 shrink-0 text-sky-400" />
                                <div>
                                    <div className="font-semibold text-zinc-200">LangGraph Agents</div>
                                    <div className="text-[11px] text-zinc-400">Stateful task graphs</div>
                                </div>
                            </div>

                            <div className="flex items-start gap-2.5 rounded-md border border-white/5 bg-white/[0.02] p-2.5">
                                <Database className="mt-0.5 h-4 w-4 shrink-0 text-emerald-400" />
                                <div>
                                    <div className="font-semibold text-zinc-200">Vector Indexing</div>
                                    <div className="text-[11px] text-zinc-400">ChromaDB and Pinecone</div>
                                </div>
                            </div>

                            <div className="flex items-start gap-2.5 rounded-md border border-white/5 bg-white/[0.02] p-2.5">
                                <Activity className="mt-0.5 h-4 w-4 shrink-0 text-amber-400" />
                                <div>
                                    <div className="font-semibold text-zinc-200">Kafka Streaming</div>
                                    <div className="text-[11px] text-zinc-400">Real-time action audit</div>
                                </div>
                            </div>

                            <div className="flex items-start gap-2.5 rounded-md border border-white/5 bg-white/[0.02] p-2.5">
                                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
                                <div>
                                    <div className="font-semibold text-zinc-200">HITL Gate</div>
                                    <div className="text-[11px] text-zinc-400">Operator review stage</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bottom Status Deck */}
                <div className="relative z-10 flex items-center justify-between border-t border-white/10 pt-4 text-xs text-zinc-400">
                    <span>AegisAI v1.0 Production Architecture</span>
                    <span className="font-mono text-[11px] text-zinc-400">SOC2 Type II Ready</span>
                </div>
            </div>

            {/* Right Panel: Clean Control Desk Auth Forms */}
            <div className="relative flex flex-1 flex-col items-center justify-center p-8 transition-colors duration-200">
                {/* Dynamic Background Grid (Only visible on right pane) */}
                <div 
                    className="absolute inset-0 opacity-[0.12] dark:opacity-[0.18]"
                    style={{
                        backgroundImage: `linear-gradient(to right, var(--border) 1px, transparent 1px), linear-gradient(to bottom, var(--border) 1px, transparent 1px)`,
                        backgroundSize: "4rem 4rem",
                        maskImage: "radial-gradient(ellipse 60% 50% at 50% 50%, #000 60%, transparent 100%)",
                        WebkitMaskImage: "radial-gradient(ellipse 60% 50% at 50% 50%, #000 60%, transparent 100%)",
                    }}
                />

                {/* Theme Toggle Positioned Top-Right */}
                <div className="absolute top-6 right-6 z-20">
                    <ThemeToggle />
                </div>

                <div className="z-10 flex w-full justify-center">
                    {children}
                </div>

                <div className="z-10 mt-6 text-center text-xs text-muted-foreground">
                    <a href="/terms" className="hover:text-foreground transition-colors hover:underline">
                        Terms and Conditions
                    </a>
                </div>
            </div>

        </div>
    );
}
