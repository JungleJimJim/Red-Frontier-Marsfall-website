# Red Frontier: Marsfall — official website

[Visit the live website](https://junglejimjim.github.io/Red-Frontier-Marsfall-website/).

A cinematic, responsive sales website for Jungle Jim’s single-player Mars RTS.

- **The game:** gameplay hook, strategy/direct-control switch, factions, campaign and skirmish features, free six-mission demo, and $5 full-game offer.
- **Units & buildings:** the complete standard faction rosters, Martian wildlife, and labelled campaign-specific entries. Every entry has concept artwork and a tactical description. Filter by faction or type, search, and inspect images.
- **Renders & art:** cinematic key art, authored model renders, concept studies, and actual gameplay captures. Filter by category and browse a keyboard-accessible image viewer.

The site uses real static pages, local artwork and fonts, CSS animations, progressive native page transitions, and small JavaScript enhancements. There are no runtime packages, analytics, cookies, or third-party image/font requests. All content is readable without JavaScript. Reduced-motion preferences are respected.

## Run and build

Requires Node.js 20 or newer. No package installation is necessary.

```sh
npm run dev
```

Open `http://127.0.0.1:4173/`.

```sh
npm run build
npm run check
```

Building updates the three checked-in HTML pages and creates a portable static site in `dist/`. The link and content check verifies all three pages, artwork, metadata, and purchase/demo settings. Deploy only the contents of `dist/` on another static host.

## Purchase link and demo

Edit `src/site-config.js`, run `npm run build`, and commit the changed files.

- Full game: **$5 USD**, linking to the owner-supplied store `https://backgroundpeople.gumroad.com`.
- Demo: **six missions**, with `demoUrl` intentionally empty until the download is ready. The site displays “Demo download coming soon” and offers no broken download action.
- The footer credits **Jungle Jim** and links to `https://junglejimjim.github.io/3D/` under the requested store heading.

When available, replace `purchaseUrl` with the exact Marsfall product URL so customers go directly to the product rather than the storefront.

## GitHub Pages

GitHub Pages is enabled using **main / (root)**. Pushing updated generated pages to `main` republishes the site. `.nojekyll` keeps the static files intact.

The live URL is:

`https://junglejimjim.github.io/Red-Frontier-Marsfall-website/`

Relative URLs support both that project path and a custom domain without changing the code. Instructions follow [GitHub’s publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Edit the website

- `src/page-templates.mjs`: the three page templates, navigation, footer, feature descriptions, and sales content.
- `src/styles.css`: responsive layouts, colors, typography, motion, and reduced-motion styling.
- `src/app.js`: filters, search, gallery navigation, mobile navigation, and the perspective switch.
- `src/content.js`: the artwork catalogue and gallery records.
- `src/site-config.js`: price, checkout, demo, and author links.
- `asset-sources.json`: original local source paths and crop coordinates for every web asset.

`scripts/prepare-assets.py` reproduces the optimized WebP artwork from the existing Marsfall library in the parent workspace. It needs Pillow and the original local files; it is not needed to build or deploy this repository. Original images and game files are never modified. The local Rajdhani font includes its SIL Open Font License in `assets/fonts/OFL.txt`.

Concept art is labelled separately from model renders and gameplay; some atlas artwork represents mission-specific designs. Marketing content is based on the current game source, without claims of multiplayer or photorealistic gameplay.

Game art, branding, and authored content © Jungle Jim. The font is licensed separately as documented above.
