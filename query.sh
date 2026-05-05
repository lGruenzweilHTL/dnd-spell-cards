#!/bin/sh
docker-compose exec -T db psql -U postgres -d spells -c "$1" 
