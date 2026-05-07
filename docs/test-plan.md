# Plan de test

## Backend
- Tests unitaires services
- Tests integration endpoints critiques

## Frontend
- Tests composants principaux
- Tests parcours auth + creation bien

## Non-fonctionnel
- Lighthouse performance/accessibilite
- Scan securite dependances


## Execution locale
- Backend: `cd apps/backend && npm test`
- Frontend: `cd apps/frontend && npm test`
- Data: `node data/scripts/clean-sales.js && node data/scripts/analytics.js`
