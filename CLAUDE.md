# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Source content (Markdown/YAML, in Indonesian) plus Node.js generator scripts that render an
IBANKCORE core-banking training document (`.docx`) and slide deck (`.pptx`). There is no
application code to run — the deliverables are the generated Office files in `dist/`.

## Commands

```bash
npm install            # deps: docx, pptxgenjs, js-yaml, image-size
npm run build           # generate both docx + pptx into dist/
npm run build:docx      # node scripts/md_to_docx.js materi_training_ibankcore.md dist/materi_training_ibankcore.docx
npm run build:pptx      # node scripts/md_to_pptx.js slides_training_ibankcore.md dist/materi_training_ibankcore.pptx
```

There is no test suite or linter. Validate changes by running the relevant build and, if
possible, opening the resulting `.docx`/`.pptx`, or optionally rendering to images:

```bash
soffice --headless --convert-to pdf dist/materi_training_ibankcore.pptx
pdftoppm -jpeg -r 100 materi_training_ibankcore.pdf slide
```

Diagrams (`diagrams/*.png`) are generated from Python/matplotlib, not drawn/screenshotted:

```bash
python3 scripts/make_diagrams.py   # requires Python 3 + matplotlib; overwrites all 4 PNGs
```

## Architecture

Two independent, one-way source → generator → output pipelines that share the same
`diagrams/` PNGs:

1. **Document pipeline**: `materi_training_ibankcore.md` (standard Markdown with a small
   YAML front matter block for the cover page) → `scripts/md_to_docx.js` (hand-rolled
   Markdown parser built on the `docx` library) → `dist/materi_training_ibankcore.docx`.
   - Front matter fields: `title`, `subtitle`, `tagline`, `org`, `note`, `header`.
   - Headings `#`/`##`/`###` map to Word Heading 1/2/3 (each H1 visually starts a new section).
   - One paragraph must be one line in the source (no mid-paragraph manual line breaks).
   - The first row of any `| ... |` table is treated as the header row.
   - Image paths (`![alt](diagrams/x.png)`) are resolved relative to the `.md` file itself.

2. **Slide pipeline**: `slides_training_ibankcore.md` is *not* plain Markdown — it's a
   sequence of YAML blocks separated by `===` lines, each block requiring a `layout:` key.
   `scripts/md_to_pptx.js` dispatches on `layout` via `if/else if` branches to build each
   slide with `pptxgenjs`. Supported layouts: `title`, `cards`, `image`, `table-grid`,
   `numbered-cards`, `two-column`, `summary`. `two-column` is the most flexible, with panel
   sub-fields (`panel`, `heading`/`intro`, `bullets`, `items`, `rows`, `list_cards`, `drcr`,
   `note`, `panel_top`/`panel_bottom`) — see `README.md` for the full field reference per
   layout before adding new slides. Adding a genuinely new layout means adding a new
   `else if (sl.layout === "...")` branch in `md_to_pptx.js` following the existing pattern.

### Design system (must stay consistent across both outputs)

Colors and fonts are hardcoded in the two generator scripts, not centralized in a config —
when adding new visual elements, reuse these rather than introducing new colors/fonts:

| Token | Hex | Use |
|---|---|---|
| Navy Dark | `12233F` | Dark background, titles |
| Navy | `1E2761` | Secondary dark panel accent |
| Ice | `CADCFC` | Text on dark background |
| Gold | `C0862B` | Accent / kicker / numbers |
| Grey Text | `44546A` | Body text on light background |
| Card BG | `EAF1F8` | Light card background |
| Light BG | `F5F8FC` | Very light card/panel background |

Fonts: headings use `Cambria` (serif), body uses `Calibri` (sans) — chosen because both
render consistently between LibreOffice preview and real Microsoft Office.

## Editing workflow

- Edit `materi_training_ibankcore.md` or `slides_training_ibankcore.md` directly, then
  rerun the corresponding `npm run build:*` command — do not hand-edit files in `dist/`
  (they are regenerated output and gitignored/deletable).
- `diagrams/*.png` are shared by both sources; edit the Python drawing code in
  `scripts/make_diagrams.py` (box positions, colors, labels) and regenerate rather than
  editing the PNGs directly.
