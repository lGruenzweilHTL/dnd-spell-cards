import json
import requests
import psycopg2
from psycopg2.extras import Json

DB_PARAMS = {
    "dbname": "spells",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432",
}

URLS = [
    "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/main/data/spells/spells-phb.json",
    "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/main/data/spells/spells-xge.json",
    "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/main/data/spells/spells-tce.json",
]


def parse_entries(entries):
    desc = ""
    for entry in entries:
        if isinstance(entry, str):
            desc += entry + "\n"
        elif isinstance(entry, dict):
            if entry.get("type") == "entries":
                desc += entry.get("name", "") + "\n"
                desc += parse_entries(entry.get("entries", []))
            elif entry.get("type") == "list":
                for item in entry.get("items", []):
                    desc += f"- {item}\n"
    return desc


def transform_spell(spell):
    slug = spell.get("name", "").lower().replace(" ", "-")
    level = spell.get("level", 0)

    components = spell.get("components", {})
    req_v = "v" in components
    req_s = "s" in components
    req_m = "m" in components
    comp_str = ""
    if req_v:
        comp_str += "V"
    if req_s:
        comp_str += " S" if comp_str else "S"
    if req_m:
        comp_str += " M" if comp_str else "M"

    material = ""
    if req_m:
        m = components.get("m")
        if isinstance(m, dict):
            material = m.get("text", "")
        elif isinstance(m, str):
            material = m

    duration = spell.get("duration", [{}])[0]
    dur_str = "Instantaneous"
    if duration.get("type") == "timed":
        dur_str = f"{duration.get('duration', {}).get('amount', '')} {duration.get('duration', {}).get('type', '')}"

    concentration = duration.get("concentration", False)

    casting = spell.get("time", [{}])[0]
    cast_str = f"{casting.get('number', '')} {casting.get('unit', '')}"

    desc = parse_entries(spell.get("entries", []))
    higher_level = (
        parse_entries(spell.get("entriesHigherLevel", [{}])[0].get("entries", []))
        if spell.get("entriesHigherLevel")
        else ""
    )

    rng = spell.get("range", {})
    rng_str = f"{rng.get('distance', {}).get('amount', '')} {rng.get('distance', {}).get('type', '')}"

    return {
        "slug": slug,
        "name": spell.get("name"),
        "desc": desc.strip(),
        "higher_level": higher_level.strip(),
        "page": str(spell.get("page", "")),
        "range": rng_str.strip(),
        "target_range_sort": rng.get("distance", {}).get("amount", 0),
        "requires_verbal": req_v,
        "requires_somatic": req_s,
        "requires_material": req_m,
        "material": material,
        "is_ritual": spell.get("meta", {}).get("ritual", False),
        "duration": dur_str.strip(),
        "requires_concentration": concentration,
        "casting_time": cast_str.strip(),
        "level": level,
        "school": spell.get("school", ""),
        "spell_lists": [
            c.get("name") for c in spell.get("classes", {}).get("fromClassList", [])
        ],
        "source_slug": spell.get("source", "").lower(),
        "source_title": spell.get("source", ""),
    }


def main():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            slug TEXT PRIMARY KEY,
            title TEXT
        );

        CREATE TABLE IF NOT EXISTS spells (
            slug TEXT PRIMARY KEY,
            name TEXT,
            "desc" TEXT,
            higher_level TEXT,
            page TEXT,
            range TEXT,
            target_range_sort INT,
            requires_verbal BOOLEAN,
            requires_somatic BOOLEAN,
            requires_material BOOLEAN,
            material TEXT,
            is_ritual BOOLEAN,
            duration TEXT,
            requires_concentration BOOLEAN,
            casting_time TEXT,
            level INT,
            school TEXT,
            source_slug TEXT REFERENCES sources(slug) ON DELETE RESTRICT,
            summary TEXT,
            flavor TEXT
        );

        CREATE TABLE IF NOT EXISTS classes (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS spell_classes (
            spell_slug TEXT REFERENCES spells(slug) ON DELETE CASCADE,
            class_id INT REFERENCES classes(id) ON DELETE CASCADE,
            PRIMARY KEY (spell_slug, class_id)
        );
    """)

    for url in URLS:
        print(f"Fetching {url}")
        res = requests.get(url)
        data = res.json()

        for spell in data.get("spell", []):
            try:
                s = transform_spell(spell)
                cur.execute(
                    "INSERT INTO sources (slug, title) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                    (s["source_slug"], s["source_title"]),
                )

                cur.execute(
                    """
                    INSERT INTO spells (
                        slug, name, "desc", higher_level, page, range, target_range_sort, 
                        requires_verbal, requires_somatic, requires_material, material, 
                        is_ritual, duration, requires_concentration, casting_time, 
                        level, school, source_slug
                    ) VALUES (
                        %(slug)s, %(name)s, %(desc)s, %(higher_level)s, %(page)s, %(range)s, %(target_range_sort)s, 
                        %(requires_verbal)s, %(requires_somatic)s, %(requires_material)s, %(material)s, 
                        %(is_ritual)s, %(duration)s, %(requires_concentration)s, %(casting_time)s, 
                        %(level)s, %(school)s, %(source_slug)s
                    ) ON CONFLICT (slug) DO UPDATE SET level = EXCLUDED.level;
                """,
                    s,
                )

                # Normalize classes
                if not isinstance(s["spell_lists"], list):
                    s["spell_lists"] = (
                        json.loads(s["spell_lists"])
                        if isinstance(s["spell_lists"], str)
                        else []
                    )

                for class_name in s["spell_lists"]:
                    cur.execute(
                        "INSERT INTO classes (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;",
                        (class_name,),
                    )
                    res_class = cur.fetchone()
                    if res_class:
                        class_id = res_class[0]
                    else:
                        cur.execute(
                            "SELECT id FROM classes WHERE name = %s;", (class_name,)
                        )
                        class_id = cur.fetchone()[0]

                    cur.execute(
                        "INSERT INTO spell_classes (spell_slug, class_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                        (s["slug"], class_id),
                    )

            except Exception as e:
                print(f"Error parsing spell {spell.get('name')}: {e}")

    # Second pass: Update classes from 5etools generated index
    print("Fetching classes from 5etools index...")
    lookup_res = requests.get(
        "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/main/data/generated/gendata-spell-source-lookup.json"
    )
    if lookup_res.status_code == 200:
        lookup_data = lookup_res.json()

        # Build mapping of spell slug -> list of classes
        # Structure is source -> spell_name_lower -> 'class' -> source -> class_name
        spell_to_classes = {}
        for src, spells_dict in lookup_data.items():
            for spell_name_lower, spell_info in spells_dict.items():
                spell_slug = (
                    spell_name_lower.replace(" ", "-")
                    .replace("'", "")
                    .replace("/", "-")
                )

                classes_set = set()
                if "class" in spell_info:
                    for class_src, class_dict in spell_info["class"].items():
                        for class_name in class_dict.keys():
                            classes_set.add(class_name)

                if classes_set:
                    # Merge across sources if spell has multiple sources
                    if spell_slug not in spell_to_classes:
                        spell_to_classes[spell_slug] = set()
                    spell_to_classes[spell_slug].update(classes_set)

        for slug, classes in spell_to_classes.items():
            for class_name in classes:
                cur.execute(
                    "INSERT INTO classes (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;",
                    (class_name,),
                )
                res_class = cur.fetchone()
                if res_class:
                    class_id = res_class[0]
                else:
                    cur.execute(
                        "SELECT id FROM classes WHERE name = %s;", (class_name,)
                    )
                    res = cur.fetchone()
                    if res:
                        class_id = res[0]
                    else:
                        continue

                cur.execute("SELECT 1 FROM spells WHERE slug = %s;", (slug,))
                if cur.fetchone():
                    cur.execute(
                        "INSERT INTO spell_classes (spell_slug, class_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                        (slug, class_id),
                    )

    conn.commit()
    cur.close()
    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
