# Ink & Silk — Chinese paintings to 1912

A personal, browsable collection of historical Chinese paintings (landscape,
bird-and-flower, figure) with a deep-zoom viewer and pinned notes. Built for iPad;
works in any modern browser. Open `index.html` through any static server (for example `python3 -m http.server`); opening the file directly won't load the JSON. No build step: `index.html`, `style.css`, `app.js`
and the JSON files in `data/`.

## Where the images come from

| Source | How it is shown | Licence |
|---|---|---|
| The Metropolitan Museum of Art (Open Access) | Full-size original JPEG from `images.metmuseum.org` | CC0 |
| Cleveland Museum of Art (Open Access) | Top works: deep-zoom tiles cut from the master TIFF, stored in `tiles/`. Others: 3400 px print JPEG from Cleveland's CDN | CC0 |
| Art Institute of Chicago | Streamed zoom tiles from AIC's IIIF server | CC0 images; descriptions CC BY |
| Freer Gallery / National Museum of Asian Art (Smithsonian) | Streamed zoom tiles from the Smithsonian IIIF server | CC0 |
| Taipei National Palace Museum, Princeton, Yale, Minneapolis, Indianapolis, Harvard, Detroit and others (via Wikidata + Wikimedia Commons) | Original file from `upload.wikimedia.org`; very large files and TIFFs use a ~45 MP scaled JPEG from Wikimedia's thumbnailer | Public domain / CC0 (per file) |
| Palace Museum (Beijing), Shanghai Museum, Liaoning, Tianjin and other museums that allow no copies | Link-only card, no image | — |

Nothing is copied from the no-copy museums.

## Data and labels

- `data/paintings.json` is one record per painting. Field names are short to keep
  the file small: `t` title, `z` Chinese title, `a` painter, `s` school,
  `d` dynasty, `g` subject, `tg` themes, `im` images, `lo` link-only, etc.
- Dynasty, subject, theme, season, palette, material and format are assigned by
  keyword rules from museum titles, media and Wikidata properties. School,
  "approach" and the painter notes come from a hand-written table in
  `tools/artists.py`. They are a guide, not a catalogue.
- Pinned notes (`data/notes.json`, written in `tools/notes_src.py`) are
  interpretations written after looking at each image. Coordinates are fractions
  of the image (x, y, w, h), so they survive re-tiling at any resolution.

## Rebuilding

The `tools/` scripts expect a working folder with the harvested source data
(Met open-access CSV and API records, Cleveland and AIC API dumps, Smithsonian
open-access metadata, Wikidata query results). Run `build_data.py`, then
`export.py`. `tile_cma.py` downloads Cleveland master files and cuts DZI tiles;
`fix_dzi.py` normalizes the level numbering.

GitHub Pages limits a published site to about 1 GB, so tiles are capped at
30 MP per painting and only the most important Cleveland works are tiled.
