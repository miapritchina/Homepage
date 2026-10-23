# Ink, Water, Stone 墨水石

A field guide for painting Chinese ink in Procreate: paper, ink, water,
mineral pigments, the brush sets, step-by-step projects, and downloadable
paper canvases and palettes.

It started as a Claude artifact and now lives here as a standalone app that
can be installed and works offline.

## Run it

No build step. Serve this folder with any static server and open it:

```sh
npx http-server .
```

Live at <https://miapritchina.github.io/Homepage/projects/ink-water-stone/>.

## Install and offline

- **iPhone / iPad:** open the page in Safari → Share → *Add to Home Screen*.
- **Android / desktop Chrome:** use *Install app* from the browser menu.

On the first visit `sw.js` (a service worker) stores the page, fonts and
library at once, then fetches the remaining images and textures (~45 MB) in
the background. The footer shows progress and says *Saved for offline use*
when everything is stored. After that the guide, including building canvases
and palettes, works with no connection.

Download buttons open the share sheet on phones and tablets (so you can *Save
to Files*), and use a normal download on desktop.

## What's inside

| Path | What |
| --- | --- |
| `index.html` | The whole guide: markup, styles and scripts |
| `art/`, `img/`, `ms/`, `strokes/` | Paintings, photos, manual pages, brush previews |
| `tex/` | Full-size paper textures used to build Procreate canvases |
| `canvas.json`, `palettes.json` | Data for the generated canvases and palettes |
| `fonts/` | Fraunces, Literata and Noto Serif SC, subset to the characters used |
| `vendor/jszip.min.js` | JSZip 3.10.1, used to build `.procreate` and `.swatches` files |
| `icons/`, `manifest.webmanifest` | App icon and install metadata |
| `sw.js` | Service worker for offline use |
| `build.py` | Regenerates the file list in `sw.js` |

## Changing files

After adding, removing or editing any file, run:

```sh
python3 build.py
```

It rewrites the list of files (with content hashes) in `sw.js`. Installed
copies then pick up only the files that changed on their next visit.

If you add text with new Chinese characters, re-subset the Noto Serif SC
fonts in `fonts/` to include them, or they will fall back to a system font.
