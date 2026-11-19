# AegisAI Engineering & Design Standards

## Core Architecture & Context
This repository houses **AegisAI**, an enterprise GenAI platform featuring FastAPI (backend), Next.js 14 (frontend), LangGraph (multi-agent orchestration), Kafka (telemetry streaming), and vector indexing (ChromaDB & Pinecone).

---

## Non-Negotiable Frontend, Copy & Launch Rules

Every contribution, modification, and generation across the website and frontend must strictly follow these constraints:

### 1. Visual Design (Anti-"Vibe Coded")
- **No purple gradients:** Do not use purple gradients (`from-purple-...`, indigo/violet flashy mesh gradients). Maintain disciplined, premium enterprise styling.
- **No pill-shaped buttons:** Action buttons must use clean geometric radii (`rounded-md`, `rounded-lg`), NEVER `rounded-full`.
- **No emoji icons:** Use clean SVG icons (Lucide React), never raw emojis (🚀, 🔥, ✨, etc.) as UI embellishments or headings.
- **No over-the-top scroll animations:** No scroll-jacking, dizzying parallax, or unnecessary scroll-tied transforms. Keep transitions snappy and functional.
- **No AI slop photos / AI slop:** No uncanny AI-generated stock photography or fake visual fluff.

### 2. Copy & Messaging
- **No vague hero copy:** Write concrete, high-signal explanations of what the software does. Never use empty buzzwords.
- **No em dashes:** The em dash (`—`) is strictly prohibited everywhere in copy, UI, and docs. Use standard punctuation.
- **No fake reviews / fake metrics:** Never fabricate customer testimonials, reviews, fake client logos, or fake counter tickers.

### 3. Launch Gates (Do Not Launch Until Complete)
1. **Custom domain** connected and verified.
2. **Custom favicon** added (replacing default framework icons).
3. **"Made with AI"** tag/badge completely absent or removed.
4. **Terms and Conditions page** (`/terms`) created and operational.

### 4. Precision
- Every instruction must be followed precisely with zero errors and rigorous validation.
