import os
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


def fetch_spells():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
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
        ORDER BY s.level, s.name
        LIMIT 20; -- Just testing first 20 for now to keep generation fast
    """)

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
        ]
        spell["classes"] = [
            c.lower() for c in spell["classes"] if c.lower() in valid_classes
        ]

    cur.close()
    conn.close()
    return spells


def main():
    print("Fetching spells from database...")
    spells = fetch_spells()
    print(f"Loaded {len(spells)} spells.")

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
    # Ensure we run in the correct directory for relative asset paths
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
