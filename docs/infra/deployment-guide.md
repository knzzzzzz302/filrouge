# Guide de deploiement

## Pre-requis
- Docker + Docker Compose
- Node.js 20+
- PostgreSQL 16+

## Etapes locales
1. `docker compose up -d db`
2. Backend: `npm install && npm run migrate && npm run dev`
3. Frontend: `npm install && npm run dev`

## Etapes production
1. Build images
2. Deploiement via pipeline CI/CD
3. Execution migrations
4. Smoke tests
