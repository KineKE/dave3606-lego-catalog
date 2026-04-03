#!/bin/sh

# Note: Do not use the `shared_buffers` configuration with such a small value in real life!
# It severely restricts the internal caching in PostgreSQL,to highlight the effects
# of the indexes even though the database isn't huge.

set -a
. ./.env
set +a

docker run \
    -d \
    --name lego-postgres \
    --env-file .env \
    -p "${DB_PORT}:5432" \
    postgres:18 \
    -c shared_buffers=128kB
