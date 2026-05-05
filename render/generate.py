import os
import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

DB_PARAMS = {
    "dbname": "spells",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432",
}


def fetch_spells(spell_names=None):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = """
        SELECT 
            s.*,
            COALESCE(
                (SELECT array_agg(c.name) 
                 FROM spell_classes sc 
                 JOIN classes c ON sc.class_id = c.id 
                 WHERE sc.spell_slug = s.slug), 
                '{}'
            ) as classes
        FROM spells s
    """

    params = ()
    if spell_names:
        query += " WHERE s.name ILIKE ANY(%s)"
        params = ([f"%{n.strip()}%" for n in spell_names],)

    query += " ORDER BY s.level, s.name"

    cur.execute(query, params)
    spells = cur.fetchall()

    # Normalize school abbreviations to full names matching our pngs
    school_map = {
        "A": "abjuration",
        "C": "conjuration",
        "D": "divination",
        "E": "enchantment",
        "V": "evocation",
        "I": "illusion",
        "N": "necromancy",
        "T": "transmutation",
    }

    for spell in spells:
        # Map 5etools short school names to full names
        if spell["school"] in school_map:
            spell["school"] = school_map[spell["school"]]
        else:
            spell["school"] = (
                spell["school"].lower() if spell["school"] else "evocation"
            )

        # Clean up classes for indicator mapping
        valid_classes = [
            "bard",
            "cleric",
            "druid",
            "paladin",
            "ranger",
            "sorcerer",
            "warlock",
            "wizard",
            "artificer",
        ]
        spell["classes"] = [
            c.lower() for c in spell["classes"] if c.lower() in valid_classes
        ]

    cur.close()
    conn.close()
    return spells


def main():
    parser = argparse.ArgumentParser(description="Generate D&D Spell Cards PDF")
    parser.add_argument(
        "--spells",
        "-s",
        type=str,
        help="Comma-separated list of spell names to generate",
    )
    args = parser.parse_args()

    spell_list = args.spells.split(",") if args.spells else None

    print("Fetching spells from database...")
    spells = fetch_spells(spell_list)
    print(f"Loaded {len(spells)} spells.")

    if not spells:
        print("No spells found. Exiting.")
        return

    print("Rendering HTML template...")
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    html_out = template.render(spells=spells)

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html_out)

    print("Generating PDF (this might take a moment)...")
    HTML(string=html_out, base_url=".").write_pdf("spells.pdf")

    print("Done! PDF saved to render/spells.pdf")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
