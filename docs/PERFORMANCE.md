# Performance Requirements

- Design mobile-first for low-end Android devices and unstable networks.
- Prefer server-rendered content where appropriate.
- Minimize client JavaScript, animations, autoplay media, and third-party scripts.
- Generate responsive optimized image derivatives.
- Reserve image dimensions to avoid layout shifts.
- Lazy-load below-the-fold images.
- Never load full-resolution originals in product grids.
- Paginate server-side and cap result counts.
- Avoid N+1 queries and unbounded database reads.
- Select only required columns.
- Index actual query patterns and inspect query plans.
- Cache public catalog data only when correct.
- Never shared-cache private customer/admin data.
- Invalidate cached data when prices, stock, or publication status change.
- Clearly indicate stale price or stock information.
- Measure transfer size, image payload, JavaScript, latency, and query performance before setting numeric budgets.
