# Projects

Small, independent projects that live in this repository alongside the
homepage. Each one sits in its own folder and is published by GitHub Pages at
`https://miapritchina.github.io/Homepage/projects/<name>/`.

## Rules

Every project folder is self-contained, as if it were its own repository:

- **One folder per project** — `projects/<name>/`, lowercase, hyphenated
  (e.g. `projects/tip-calculator/`).
- **An `index.html` at the folder root**, so the folder URL opens the project.
- **A `README.md`** saying what it is and how to run it.
- **No shared files.** Don't reference anything outside the project's own
  folder — no `../`, no root-absolute `/` paths, no imports from the homepage
  or another project. Copy what you need instead.
- **Its own tooling.** If a project needs a build step or dependencies, its
  `package.json`, lockfile and config live inside its folder and are run from
  there. Nothing is installed at the repository root.
- **Relative links only** within the project, so it works both from this repo
  and if the folder is moved out into a repository of its own.

## Adding a project

1. Create `projects/<name>/` with an `index.html` and a `README.md`.
2. Optionally list it on the homepage — see "Adding a project" in the root
   `README.md`, linking to `projects/<name>/`.
