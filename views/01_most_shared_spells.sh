#!/bin/bash
# Find spells that are available to the highest number of different classes
./query.sh "SELECT s.name, s.level, COUNT(c.id) as class_count, STRING_AGG(c.name, ', ') as classes FROM spells s JOIN spell_classes sc ON s.slug = sc.spell_slug JOIN classes c ON sc.class_id = c.id GROUP BY s.slug, s.name, s.level ORDER BY class_count DESC, s.level ASC LIMIT 15;"
