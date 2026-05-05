#!/bin/bash
# Count the number of spells in each school of magic, broken down by source book
./query.sh "SELECT school, source_slug, COUNT(*) as spell_count FROM spells GROUP BY school, source_slug ORDER BY school, source_slug;"
