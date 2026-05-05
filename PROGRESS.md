# D&D Spell Cards - Project Progress

## Goal
Build a normalized PostgreSQL database of D&D 5e spells (PHB, XGE, TCE) and an automated HTML/CSS -> PDF rendering pipeline that exactly matches the provided Photoshop (PSD) templates for printing spell cards.

## Accomplished So Far

### 1. Database & Ingestion
- **PostgreSQL Setup:** Dockerized PostgreSQL 15 database (`db/compose.yaml`).
- **Data Ingestion:** Created `db/import.py` to fetch, parse, and normalize JSON data from 5etools into a 3NF schema (spells, sources, classes, spell_classes).
- **Class Mappings:** Accurately linked spells to classes using 5etools' `gendata-spell-source-lookup.json` to handle non-SRD spells correctly.
- **Summarization:** Added a manual `summary` column to the `spells` table. If populated, the render pipeline uses this instead of the full spell description. Created `db/summarize-spell.sh` to easily update this field.

### 2. Assets & PSD Analysis
- Extracted all required assets from the PSD templates (backgrounds, school icons, class/component indicators) into `render/assets/`.
- Analyzed PSD text layers to exactly match fonts (`Ringbearer`, `MPlantin`), sizes, bounding boxes, alignments, and line-heights.

### 3. Rendering Pipeline
- **Engine:** Python script (`render/generate.py`) using `Jinja2` and `WeasyPrint` to query the database and output `render/spells.pdf`.
- **Text Formatting:** Built a regex cleaner to strip 5etools metadata tags (e.g., `{@damage 1d6}` -> `1d6`).
- **Translations:** Abbreviated and capitalized game terms (e.g., "1 action" -> "1 Action", "1 bonus action" -> "Bonus", "touch" -> "Touch", "Cantrip" -> "C").
- **Dynamic Styling (`style.css` & `template.html`):**
  - Text scales dynamically for long spell names to prevent overflow.
  - Detail fields (`Range`, `Duration`, `Time`) are aligned precisely and set to `nowrap`.
  - Conditional theme coloring (`#000` for Divination/Transmutation backgrounds, `#fff` for others).
  - Component/Class indicators are injected automatically based on boolean flags and relational data.
  - Page/Source numbers display at the bottom, with an appended `*` if a custom summary is being used instead of the raw description.

## Next Steps (Pending Tasks)

1. **Flavor Text Overhaul:**
   - **Current State:** The `.flavour` text box currently displays material components (e.g., "Materials: A tiny ball of bat guano").
   - **New Requirement:** Replace this with custom flavor text for *each spell*. This should be something funny about the spell or an in-character quote you could say while casting it.
   - **Styling Requirement:** The flavor text box is restricted to a max of 2 lines. If the new flavor text linewraps, we must ensure the dynamic font sizing math properly shrinks it so it fits the bounding box without truncating or overflowing.

## File Map
- `db/` - Database container, import script, and query/summarize helpers.
- `render/` - PDF generation script, HTML/CSS templates, and extracted assets/fonts.
- `tools/` - Python scripts for PSD layer/text extraction and analysis.
