# Performance Requirements

**Authoritative for:** performance budgets, image rules, caching, query rules. Audience: low-end Android phones on slow, unstable mobile networks.

## Provisional budgets (PROVISIONAL: measure in T-061, then revise this file)
These are starting targets so work can be tested; they are not measured facts.

| Item | Target |
|------|--------|
| Listing page HTML + CSS + JS, excluding images | <= 60 KB transferred (compressed) |
| JavaScript total on any public page | <= 30 KB compressed; pages must work with JavaScript disabled |
| Product grid thumbnail | <= 20 KB each; no full-size originals in grids |
| Images per listing page | <= 20 (page size) |
| Order form page | <= 50 KB excluding images; usable without JS |
| Listing usable (largest content visible) | <= 4 s on a "Fast 3G"-style throttle with 4x CPU slowdown in browser dev tools |
| Server response (listing, detail) | <= 500 ms at pilot scale on the chosen host |
| Database query count per page | bounded, no N+1 (asserted by test) |

## How to measure (evidence required in T-061)
1. Browser dev tools: network throttling + CPU throttling, cache disabled, record transferred size per resource and timings.
2. If available, a real low-end Android phone on a real mobile connection.
3. Query plans (`EXPLAIN`) for listing and search with realistic synthetic volume (e.g. 1,000 products).
Record numbers in the task report and update the table above.

## Rules
- Server-rendered pages; minimal JavaScript; no animations, autoplay media, web fonts, or third-party scripts. System fonts only (Burmese Unicode rendering on target devices: TECH-STACK U10).
- Responsive image derivatives generated at upload; set width/height attributes to avoid layout shift; lazy-load images below the fold; modern compressed formats where supported with a safe fallback.
- Server-side pagination (default 20, max 50); select only needed columns; avoid N+1 queries; no unbounded reads.
- Indexes only for real query patterns, with `EXPLAIN` evidence ([DATA-MODEL](DATA-MODEL.md#indexes)).
- Caching: MVP uses HTTP caching for static files and generated images (content-addressed names, long lifetime) only. **No shared cache of catalog HTML in the MVP.** Never cache private (admin/order) pages. If page caching is added later it must invalidate on price, stock, availability and publication changes (needs an ADR).
- Show stale price/stock labels ([DATA-MODEL](DATA-MODEL.md#visibility-rules-authoritative)).
- Compression (gzip/brotli) enabled in production (verify on the host).
