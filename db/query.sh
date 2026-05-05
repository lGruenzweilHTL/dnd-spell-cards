#!/bin/sh
docker-compose -f ../compose.yaml exec -T db psql -U postgres -d spells -c "$1"
