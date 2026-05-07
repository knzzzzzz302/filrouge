#!/usr/bin/env bash
set -e

docker compose up -d db
(cd apps/backend && npm install && npm run dev) &
(cd apps/frontend && npm install && npm run dev)
