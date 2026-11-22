# cardbeat-website

The website for [CardBeat](https://apps.apple.com/app/id1488252091), the digital corkboard for plotting novels and screenplays on iPhone and iPad.

Plain static HTML and CSS, served by GitHub Pages from `main` at https://cardbeat.app (see `CNAME`). No build step, no external requests (system fonts, inline SVG, local images).

| Path | Page |
|---|---|
| `index.html` | English landing page with FAQ |
| `de/index.html` | German landing page |
| `compare.html` | CardBeat vs. Scrivener, Freeform and paper index cards |
| `impressum.html`, `privacy.html` | Legal notice and privacy policy |
| `llms.txt` | Plain-text fact sheet for AI agents ([llmstxt.org](https://llmstxt.org)) |

The FAQ appears twice on each landing page: once as HTML, once as `FAQPage` JSON-LD in the `<head>`. Keep them in sync.

When you change a page, also update its `<lastmod>` in `sitemap.xml`, and `llms.txt` if a fact changes (price, platforms, features). The author's `sameAs` links must be the same in every JSON-LD block.

## Checks

```
python3 -m unittest discover tests
```

Standard library only; also runs in GitHub Actions on every push and PR. It checks that JSON-LD parses, the FAQ copies match, sitemap entries and `hreflang` agree with the pages, every indexable page is in the sitemap, and `llms.txt` links resolve.

Screenshots in `assets/img/` are resized WebP copies of the raw captures in the app repo (`AppStoreScreenshots/tools/raw`).

## Preview locally

```
python3 -m http.server 8000
```
