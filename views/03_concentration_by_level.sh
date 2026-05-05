#!/bin/bash
# Analyze what percentage of spells require concentration at each spell level
./query.sh "SELECT level, COUNT(*) as total_spells, SUM(CASE WHEN requires_concentration THEN 1 ELSE 0 END) as conc_spells, ROUND((SUM(CASE WHEN requires_concentration THEN 1 ELSE 0 END)::numeric / COUNT(*)) * 100, 1) as conc_percentage FROM spells GROUP BY level ORDER BY level;"
