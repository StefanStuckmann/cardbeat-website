# cardbeat-website

The website for [CardBeat](https://apps.apple.com/app/id1488252091), the digital corkboard for plotting novels and screenplays on iPhone and iPad.

Plain static HTML and CSS, served by GitHub Pages from `main`. No build step, no external requests (system fonts, inline SVG, local images).

| Path | Page |
|---|---|
| `index.html` | English landing page with FAQ |
| `de/index.html` | German landing page |
| `compare.html` | CardBeat vs. Scrivener, Freeform and paper index cards |
| `impressum.html`, `privacy.html` | Legal notice and privacy policy |

The FAQ appears twice on each landing page: once as HTML, once as `FAQPage` JSON-LD in the `<head>`. Keep them in sync.

Screenshots in `assets/img/` are resized WebP copies of the raw captures in the app repo (`AppStoreScreenshots/tools/raw`).

## Preview locally

```
python3 -m http.server 8000
```
