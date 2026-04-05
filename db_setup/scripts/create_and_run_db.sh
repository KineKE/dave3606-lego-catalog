#!/bin/sh

# Note: Do not use the `shared_buffers` configuration with such a small value in real life!
# It severely restricts the internal caching in PostgreSQL,to highlight the effects
# of the indexes even though the database isn't huge.

. "$(dirname "$0")/load_env.sh"

docker run \
    -d \
    --name "${DB_CONTAINER_NAME}" \
    --env-file "${ENV_FILE}" \
    -p "${DB_PORT}:5432" \
    postgres:18 \
    -c shared_buffers=128kB
