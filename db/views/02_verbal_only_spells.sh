#!/bin/bash
# Find spells that only require a Verbal component (useful when restrained)
./query.sh "SELECT name, level, school, casting_time FROM spells WHERE requires_verbal = true AND requires_somatic = false AND requires_material = false ORDER BY level, name;"
