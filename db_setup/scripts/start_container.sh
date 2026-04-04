#!/bin/sh

. "$(dirname "$0")/load_env.sh"

docker start "${DB_CONTAINER_NAME}"
