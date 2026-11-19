# Strict Design, Copywriting & Launch Standards

This repository enforces strict, non-negotiable frontend design, copy, and release rules. All code, design, and content generated or modified must strictly abide by these principles.

---

## 1. Visual Design & UI Restrictions (Anti-"Vibe Coded")

- **Zero Purple Gradients:** Never use purple gradients (`from-purple-...`, `bg-gradient-to-...` with purple/indigo/violet mashups). Use clean, intentional, brand-grounded color palettes (slate, zinc, neutral, monochrome with subtle disciplined accents).
- **No Pill-Shaped Buttons:** Never use `rounded-full` for interactive action buttons. Buttons must use crisp, structured geometric corners (e.g., `rounded-md` or `rounded-lg`).
- **No Emoji Icons:** Never use emojis (e.g., 🚀, 🔥, ✨, 🧠, ⚡) as UI icons, section accents, or heading decorations. Use professional SVG icons (such as Lucide React).
- **No Over-the-Top Scroll Animations:** Never introduce scroll-jacking, intense parallax, excessive scale/tilt on scroll, or distracting motion gimmicks. Interactions must be fast, subtle, and utilitarian.
- **No AI Slop Photos or Assets:** Never use distorted, generic, or uncanny AI-generated stock photos, faux portraits, or decorative AI slop. Use real diagrams, authentic product telemetry, or clean vector iconography.

---

## 2. Copywriting & Content Integrity

- **No Vague Hero Text:** Never write buzzword-filled, ambiguous hero headlines (e.g., "Revolutionize your workflow with next-gen synergy"). Always write clear, concrete, factual, and direct explanations of what the software actually does.
- **Strictly No Em Dashes:** The em dash character (`—` / `&mdash;`) is forbidden across all website copy, UI strings, and documentation. Use hyphens (`-`), colons, commas, or separate sentences instead.
- **No Fake Reviews or Testimonials:** Never fabricate user testimonials, quote fictional executives, or use placeholder persona avatars.
- **No Fake Metrics or Counters:** Never invent bogus adoption stats (e.g., "10,000+ teams trust us", "99.99% accuracy" without telemetry backing, or fake animated counter tickers).

---

## 3. Mandatory Pre-Launch Checklist

The platform must **NEVER** launch or be tagged production-ready until all of the following requirements are satisfied:
1. **Custom Domain:** Connected and verified with SSL.
2. **Favicon:** Custom, production-ready favicon installed (no default Next.js/framework icons).
3. **No "Made with AI" Tag:** Ensure all "Made with AI" watermarks, banners, badges, and footer credits are completely removed.
4. **Terms and Conditions:** A dedicated, fully compliant `/terms` page is published and linked in the navigation/footer.

---

## 4. Execution Standard

- Follow every requirement precisely without deviation or hallucination.
- Double-check all diffs before finalizing changes to guarantee zero regressions against these standards.
