# Deployment Checklist

## ✅ Completed
- PostgreSQL database setup (Dockerized)
- Data import pipeline (5etools JSON -> normalized 3NF schema)
- HTML/CSS template matching PSD designs exactly
- PDF generation pipeline (Jinja2 + WeasyPrint) ✅ **TESTED**
- Dynamic text coloring, sizing, and wrapping
- Component/class indicators
- Flavor text rendering with centering & dynamic font scaling
- `max_desc_length` calculated (accounts for higher_level text)
- **Spell Summarization: 224/364 spells (61%)**
  - Applied via batch processing with subagents
  - 141 spells still need manual summaries

## 🔄 In Progress / Ready for Deployment
- **Remaining Spell Summarization (141 spells)**
  - Can be done manually using `db/summarize-spell.sh` per spell
  - Or re-process remaining batches
  - Project is **DEPLOYABLE NOW** with partial summaries

## 🚀 Ready to Deploy Now
1. Test full render:
   ```bash
   ./venv/bin/python render/generate.py --all
   ```
2. Verify PDF output at `render/spells.pdf`
3. For remaining spells (141), use `db/summarize-spell.sh`:
   ```bash
   db/summarize-spell.sh "Spell Name" "Concise summary text..."
   ```
4. Re-run render after manual summaries

## File Structure
```
db/          Database setup, import, and query scripts
render/      HTML/CSS templates and PDF generation
tools/       PSD extraction, batch files, agent instructions
PROGRESS.md  Project history and technical decisions
```

## Current Stats
- Total spells: 477
- Spells needing summaries: 364
- Summaries created: 224 (61%)
- Still need: 141 (39%)
