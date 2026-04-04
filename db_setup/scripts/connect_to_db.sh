#!/bin/sh

. "$(dirname "$0")/load_env.sh"

docker exec -it "${DB_CONTAINER_NAME}" psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"
