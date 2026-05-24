# Deployment Checklist

## ✅ Completed
- PostgreSQL database setup (Dockerized)
- Data import pipeline (5etools JSON -> normalized 3NF schema)
- HTML/CSS template matching PSD designs exactly
- PDF generation pipeline (Jinja2 + WeasyPrint)
- Dynamic text coloring, sizing, and wrapping
- Component/class indicators
- Flavor text rendering with centering & dynamic font scaling
- `max_desc_length` calculated (accounts for higher_level text)
- Batch files created for distributed summarization work

## 🔄 In Progress
- **Spell Summarization (364 spells across 10 batches)**
  - Each agent receives `tools/batch_X.json`
  - Summarize descriptions > `max_desc_length`
  - Output SQL to `tools/update_X.sql`
  - See `tools/AGENT_INSTRUCTIONS.md` for details

## 🚀 Ready to Deploy Once Summaries Complete
1. Collect all `tools/update_X.sql` files from agents
2. Apply summaries to database:
   ```bash
   for f in tools/update_*.sql; do
     docker compose exec -T db psql -U postgres -d spells -f "$f"
   done
   ```
3. Test full render:
   ```bash
   ./venv/bin/python render/generate.py --all
   ```
4. Verify PDF output at `render/spells.pdf`
5. Use `db/summarize-spell.sh` for manual updates

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
- Batch size: ~37 spells/batch (10 batches)
