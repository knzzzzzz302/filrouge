# Alignement complet a la grille d'evaluation (DEV + INFRA)

Ce document mappe chaque critere de la grille aux livrables/proves du projet Y-Plaza.

## 1) Oral final DEV (50%)

| Critere DEV (grille) | Pond. | Ce qui est implemente | Preuve a montrer | Niveau cible |
|---|---:|---|---|---|
| Concevoir une solution repondant au besoin metier | 5 | Plateforme Y-Plaza avec parcours client/auth/hub et API metier | `docs/functional-spec.md`, landing + hub live | Acquis/Maitrise |
| Developper une application fonctionnelle | 10 | Front React + Backend Express + routes metier auth/properties/clients/transactions/analytics | Demo live `frontend + backend`, `apps/backend/src/app.ts` | Acquis |
| Bonnes pratiques de dev | 3 | TS strict, validation `zod`, separation app/server, tests | `apps/backend/tsconfig.json`, tests `vitest` | Acquis |
| Principes POO / conception | 3 | Architecture services/modules + middleware RBAC | `apps/backend/src/modules/*`, `middleware/auth.ts` | Acquis |
| Modeliser une BDD relationnelle | 3 | Tables properties/clients/transactions + relations | `docs/data-model.md`, `src/db/migrate.js` | Acquis |
| Interroger une BDD relationnelle | 4 | CRUD SQL et requetes analytics | routes backend + `docs/api-spec.md` | Acquis |
| UX / interfaces intuitives | 5 | UI moderne multi-pages (landing/inscription/connexion/hub) | navigation live + `styles.css` | Acquis |
| Responsive/accessibilite/performance | 3 | UI responsive, formulaires clairs, build Vite optimise | test sur mobile/desktop + build output | Acquis |

### Actions pour viser "Maitrise" en DEV
- Ajouter tests integration API CRUD (au-dela des tests actuels).
- Ajouter instrumentation perf (Lighthouse export).
- Montrer un cas de securite applicative bloque (RBAC/401/403) en live.

---

## 2) Oral final INFRA (50%)

| Critere INFRA (grille) | Pond. | Ce qui est livre | Preuve a montrer | Niveau cible |
|---|---:|---|---|---|
| Concevoir une architecture reseau multi-sites | 8 | Topologie hub-and-spoke + segmentation VLAN + flux | `docs/infra/network-architecture.md` | Acquis/Maitrise |
| Configurer des serveurs pour differents services | 5 | Runbook AD/DNS/DHCP + plan deployment | `docs/infra/server-configuration-guide.md` | Acquis |
| Mettre en place un systeme de gestion des droits | 3 | Matrice des droits + groupes AD/GPO | `docs/access-control-matrix.md`, `infra/runbooks/ad-gpo-runbook.md` | Acquis |
| Concevoir une solution cloud hybride/public | 5 | Proposition cloud + benefices/exploitation | `docs/infra/cloud-proposal.md` | Acquis |
| Choisir et budgetiser une infrastructure | 2 | Liste materiel + CAPEX + hypotheses OPEX | `docs/infra/hardware-budget.md` | Acquis |
| Presenter une demonstration avec des VM | 10 | Runbook demo + setup VM + tests reseau | `docs/infra/demo-runbook.md`, `infra/runbooks/vm-lab-setup.md` | Acquis/Maitrise |
| Appliquer une politique de securite reseau/systemes | 3 | Politique securite + firewall matrix + logs/sauvegarde | `docs/infra/security-policy.md`, `infra/firewall/firewall-policy-matrix.md` | Acquis |

### Actions pour viser "Maitrise" en INFRA
- Executer un test PRA en live (mini restauration).
- Montrer une alerte supervision temps reel (VPN down/recover).
- Montrer preuves horodatees pour chaque critere (captures INFRA_01..08).

---

## 3) Strategie de passage oral (optimisation note)

## A. Ce qu'il faut absolument montrer en live
1. Tunnel VPN UP + ping inter-site.
2. DHCP bail conforme sur poste agence.
3. DNS interne (`nslookup`) resolu.
4. AD + groupes + GPO appliquee (`gpresult`).
5. Hub applicatif Y-Plaza fonctionnel.

## B. Ordre de passage recommande
- Utiliser `docs/infra/screen-flow-oral.md` pour l'ordre ecran/evidence.
- Utiliser `docs/infra/oral-script-infra.md` pour le discours.
- Utiliser `docs/infra/capture-evidence-checklist.md` comme plan B.

## C. Niveau cible par critere
- Minimum acceptable: **Acquis** sur tous les criteres a forte pond.
- Critiques pour monter la note: VPN+VM demo+architecture (INFRA) et application fonctionnelle (DEV).

---

## 4) Checklist finale alignee grille

- [ ] Tous les criteres de la grille ont une preuve associee.
- [ ] Chaque preuve est testee en condition reelle avant oral.
- [ ] Script oral repete au chrono (10 min DEV + 10 min INFRA).
- [ ] Plan B captures disponible en local.
- [ ] Reponses pretes aux questions frequentes jury.
