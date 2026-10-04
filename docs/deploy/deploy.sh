#!/usr/bin/env bash
set -euo pipefail
cd /home/manga-notify/app
: "${TAG:?Release tag is required}"
export TAG
docker compose config --quiet
docker compose pull
docker compose up -d --wait --wait-timeout 120
# Persist the selected release for subsequent restarts.
sed -i '/^TAG=/d' .env
printf 'TAG=%s\n' "$TAG" >> .env
