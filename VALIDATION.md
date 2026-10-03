# Website verification — October 4, 2026

- `npm run build` and `npm run check`: passed. Three static routes, all local links and artwork, unique archive identifiers, metadata, $5 USD price, and six-mission demo configuration.
- JavaScript syntax check: passed.
- Catalogue: 72 entries covering both normal faction rosters, wildlife, and labelled mission-specific assets. Each has artwork, a role, and a description.
- Gallery: 29 pieces, including 12 model renders. Concept art, model renders, and gameplay have separate labels and filters.
- Browser interactions: faction/type combinations, search, empty results and reset, the perspective switch, mobile navigation, image inspection, previous/next navigation, arrow keys, Escape dismissal, and focus return passed.
- Responsive checks: desktop 1280px, mobile 390px, and the narrower in-app preview. No unintended horizontal scrolling. The mobile catalogue uses one readable column; the image viewer fits the viewport.
- Project-path preview: all routes and relative assets worked beneath `/Red-Frontier-Marsfall-website/`.
- Published website: homepage HTTP 200. All three routes opened in the browser with the expected content, images loaded, and no site console warnings or errors.
- Purchase button links to the owner-supplied Gumroad storefront. The demo URL is intentionally unset and displays “Demo download coming soon.”
- Motion preferences have a dedicated CSS reduced-motion override. No external fonts, analytics, trackers, or live services are required for the pages to render.

The website is published at https://junglejimjim.github.io/Red-Frontier-Marsfall-website/.
