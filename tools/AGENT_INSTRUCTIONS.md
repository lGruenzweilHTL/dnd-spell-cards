# Instructions for Future Agents - Spell Summary Task

## Context
The D&D Spell Card project has a PostgreSQL database with a `spells` table. Each spell has:
- `slug`: unique identifier
- `name`: spell name
- `desc`: full description text
- `max_desc_length`: maximum character length that fits in the 380px description box
- `summary`: (NULL by default) shorter summary to use instead of desc

## Your Task
You will receive one batch file (e.g., `batch_0.json`) containing spells that need summarization.

For each spell in your batch:
1. Check if `len(desc) > max_desc_length`
2. If YES: Write a concise summary that captures the essential mechanics
3. If NO: Skip (no SQL needed)

## Summary Guidelines
- MUST be ≤ `max_desc_length` characters
- Capture the spell's **core mechanics** (what it does, damage dice, duration)
- Keep the flavor/tone but remove verbose descriptions
- Use the same formatting as `desc` (line breaks with `\n`, not HTML)
- Preserve any {@tag} notations if present (or clean them if requried by render pipeline)

## Output Format
Create an SQL file named `update_X.sql` (where X matches your batch number) with:

```sql
UPDATE spells SET summary = 'Your concise summary here' WHERE slug = 'spell-slug';
UPDATE spells SET summary = 'Another summary' WHERE slug = 'another-spell';
...
```

## Example
For a spell with `max_desc_length = 400` but `desc` length = 800:
```sql
UPDATE spells SET summary = 'You create a bonfire on ground within range. Until the spell ends, the magic bonfire fills a 5-foot cube. Any creature in the bonfire''s space when you cast the spell must succeed on a Dexterity saving throw or take 1d8 fire damage. A creature must also make the saving throw when it moves into the bonfire''s space for the first time on a turn or ends its turn there.\nThe bonfire ignites flammable objects in its area that aren''t being worn or carried.\nThe spell''s damage increases by 1d8 when you reach 5th level (2d8), 11th level (3d8), and 17th level (4d8).' WHERE slug = 'create-bonfire';
```

## Important Notes
- Escape single quotes in SQL with double single-quotes (`''`)
- Only include UPDATE statements for spells that need summarization
- If all spells in your batch fit within their max_desc_length, output an empty file
- The batch files are located in `/home/lukas/Github/dnd-spell-db/tools/batch_X.json`

## File Mapping
- Input: `tools/batch_X.json`
- Output: `tools/update_X.sql`
