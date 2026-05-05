# Architecture

This project is divided into three main components: Database (db), Tools, and Render pipeline.

## 1. Database (`db/`)
Handles data ingestion, normalization, and querying.
- **`compose.yaml`**: Defines a Dockerized PostgreSQL 15 database.
- **`import.py`**: ETL script. Fetches JSON data from 5etools mirror, normalizes it into 3NF (Third Normal Form), and imports classes from Open5e to resolve mappings.
- **Schema**:
  - `sources`: Source books (PHB, XGE, TCE).
  - `spells`: Core spell data (level, components, times, descriptions).
  - `classes`: D&D classes.
  - `spell_classes`: Many-to-many mapping of spells to classes.
- **`views/`**: Shell scripts leveraging `query.sh` to extract interesting datasets.

## 2. Tools (`tools/`)
Utility scripts used for one-off operations.
- **`analyze_psd.py`**: Extracts bounding box coordinates and layer structures from Photoshop (`.psd`) templates.
- **`extract_assets.py`**: Headless script using `psd-tools` to extract background images, school icons, and indicator tags (V, S, M, classes) into transparent PNGs.

## 3. Render Pipeline (`render/`)
Automated generation of printable spell cards.
- **HTML/CSS (`template.html`, `style.css`)**: Mimics the exact layout of the PSD templates using absolute positioning based on the bounding boxes extracted via `analyze_psd.py`.
- **Python Generator (`generate.py`)**: Uses `psycopg2` to query the database, `Jinja2` to inject data into the HTML template, and `WeasyPrint` to compile the output into a high-resolution, print-ready PDF.
