# Homepage

A single-page index of my deployed projects, plus a home for small
independent projects.

## Layout

```
index.html, manifest.webmanifest, icons/   the homepage (repo root)
projects/<name>/                           one self-contained project per folder
```

The homepage stays at the root so its GitHub Pages URL doesn't change. Each
project under `projects/` is independent of the homepage and of every other
project — see [`projects/README.md`](projects/README.md) for the rules.

## Homepage

`index.html` is the whole site — no build step, no dependencies. Open the file
directly in a browser to preview it, or serve the folder with any static server:

```sh
npx http-server .
```

### Publishing

The page is meant to be served by GitHub Pages from this repository. Once the
branch is merged, enable it under **Settings → Pages → Build and deployment**,
source **Deploy from a branch**, branch `main`, folder `/ (root)`.

It will then be live at <https://miapritchina.github.io/Homepage/>.

To serve it from the bare `miapritchina.github.io` domain instead, rename this
repository to `miapritchina.github.io`.

### Icons

`icons/icon.svg` is the source mark — the masthead seal, with the Instrument
Serif `M` converted to an outline so it renders identically without the
webfont. The PNGs next to it are rasterised from that SVG and listed in
`manifest.webmanifest`, which is what gives the page a real icon when it is
installed to a phone home screen rather than a screenshot of the page.

### Adding a project

Copy an existing `<li class="entry">` block in `index.html`, update the title,
description, tags and the two links, then bump the `--i` values that follow so
the load-in animation stays in order.

For a project kept in this repo, link to `projects/<name>/` instead of an
external URL.
