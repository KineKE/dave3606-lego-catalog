#!/bin/sh

. "$(dirname "$0")/load_env.sh"

docker stop "${DB_CONTAINER_NAME}"
