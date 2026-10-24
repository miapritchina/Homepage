# Repository layout

This repo holds the homepage plus small independent projects.

- The homepage is the repo root: `index.html`, `manifest.webmanifest`, `icons/`.
  It stays at the root because GitHub Pages serves it from there.
- Every other project lives in its own folder under `projects/<name>/` and must
  be fully independent: no references outside its folder, its own `README.md`
  and tooling. See `projects/README.md` for the rules.
- Never mix files between the homepage and a project, or between projects.
