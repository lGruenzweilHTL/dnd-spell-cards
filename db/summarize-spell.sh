#!/bin/sh
docker-compose -f compose.yaml exec -T db psql -U postgres -d spells -c "UPDATE spells SET summary = '$2' WHERE name = '$1';"
