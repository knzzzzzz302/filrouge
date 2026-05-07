# Y-Plaza - Projet B2 INFRA & DEV

Plateforme web centralisee pour l'achat/vente immobilier, avec couche data et architecture infra securisee.

## Stack
- Frontend: React + TypeScript + Vite
- Backend: Node.js + Express + TypeScript
- Base de donnees: PostgreSQL
- Infra locale: Docker Compose

## Structure
- `docs/`: documentation fonctionnelle, technique, infra, oral
- `apps/backend`: API REST + logique metier
- `apps/frontend`: interface utilisateur responsive
- `apps/shared`: schemas/types partages
- `data`: jeux de donnees et scripts analytics
- `infra`: artefacts d'infrastructure et runbooks
- `scripts`: scripts utilitaires projet

## Demarrage rapide
1. Copier `.env.example` en `.env` dans `apps/backend`.
2. Lancer `docker compose up -d db`.
3. Dans `apps/backend`: `npm install && npm run dev`.
4. Dans `apps/frontend`: `npm install && npm run dev`.

## Qualite
- Architecture orientee services
- Principes SOLID/DRY/KISS
- RBAC et validation des entrees
- Documentation technique et infra complete

## Verification rapide avant oral
- `bash scripts/demo-ready.sh`
- Ce script valide data, build et tests front/back.
- Pour la partie DB reelle: lancer PostgreSQL via Docker puis executer les migrations backend.

## Verification conformite grille
- `bash scripts/grille-audit.sh`
- Audit la presence de tous les livrables mandatoires du brief et de la grille.
