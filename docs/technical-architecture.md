# Architecture technique

## Vue logique
- Front React consomme API REST Express
- Backend decoupe en services metier (auth, properties, clients, transactions, analytics)
- PostgreSQL centralise les donnees
- Jobs analytics sur snapshots CSV

## Normes
- TypeScript strict sur frontend/backend
- Validation schema (zod)
- Journalisation applicative (pino)
- Gestion erreurs centralisee

## Securite applicative
- JWT access token
- Hash mots de passe (bcrypt)
- RBAC middleware
- Rate limiting API
- Helmet + CORS controle
