# Conformite complete a la grille (A a Z)

Ce document couvre l'ensemble de la grille: competences transverses (oral intermediaire), DEV final et INFRA final.

## Barème et ponderation globale
- Note competences transverses (oral intermediaire): coef 1
- Note technique (oral final DEV + INFRA): coef 3
- DEV: 50% du final technique
- INFRA: 50% du final technique

---

## 1) Oral intermediaire - competences transverses

| Critere transverse | Statut | Preuves disponibles | Action pour viser "Maitrise" |
|---|---|---|---|
| Utiliser Git/GitHub pour collaboration | Conforme | Workflow git + dossier docs + historique local | Presenter conventions commit/branches en demo |
| Gérer projet avec outils adaptes | Conforme | `docs/project-plan.md`, `docs/backlog.md` | Ajouter capture board Trello/Notion |
| Rediger des specifications | Conforme | `docs/functional-spec.md`, `docs/api-spec.md` | Ajouter exigences non-fonctionnelles priorisees |
| Presenter un projet a l'oral | Conforme | `docs/oral-outline.md`, `docs/demo-script.md` | Repetition chronometree avec Q&A |
| Posture professionnelle | Conforme | Dossier structure + runbooks + plan de secours | Preparer speech clair et responsabilites equipe |

---

## 2) Oral final DEV - criteres techniques

| Critere DEV | Pond. | Statut | Preuves |
|---|---:|---|---|
| Concevoir une solution logicielle metier | 5 | Conforme | `docs/functional-spec.md`, landing/hub |
| Developper une application fonctionnelle | 10 | Conforme | `apps/frontend`, `apps/backend`, demo live |
| Bonnes pratiques de dev | 3 | Conforme | TS strict, zod, modularite, tests |
| Principes POO / structuration | 3 | Conforme | modules backend + middleware RBAC |
| Modeliser la BDD relationnelle | 3 | Conforme | `docs/data-model.md`, migrations |
| Interroger la BDD relationnelle | 4 | Conforme | SQL CRUD dans routes/services |
| UX et interfaces intuitives | 5 | Conforme | pages modernes + parcours inscription/connexion/hub |
| Responsive/accessibilite/performance | 3 | Conforme | UI responsive, build optimise Vite |

### Observations DEV
- Couverture attendue par la grille: atteinte.
- Pour "Maitrise": renforcer tests integration CRUD et evidences perf (Lighthouse).

---

## 3) Oral final INFRA - criteres techniques

| Critere INFRA | Pond. | Statut | Preuves |
|---|---:|---|---|
| Architecture reseau multi-sites | 8 | Conforme | `docs/infra/network-architecture.md` |
| Configurer differents services serveurs | 5 | Conforme | `docs/infra/server-configuration-guide.md`, runbooks |
| Mettre en place gestion des droits | 3 | Conforme | `docs/access-control-matrix.md`, AD/GPO runbook |
| Concevoir solution cloud hybride/public | 5 | Conforme | `docs/infra/cloud-proposal.md` |
| Choisir et budgetiser infra | 2 | Conforme | `docs/infra/hardware-budget.md` |
| Demonstration avec VM | 10 | Conforme | `docs/infra/demo-runbook.md`, `infra/runbooks/vm-lab-setup.md` |
| Politique securite reseau/systemes | 3 | Conforme | `docs/infra/security-policy.md`, firewall matrix |

### Observations INFRA
- Couverture attendue par la grille: atteinte.
- Pour "Maitrise": preuve live d'une restauration PRA + alerte supervision.

---

## 4) Livrables obligatoires du brief

| Livrable demande | Statut | Emplacement |
|---|---|---|
| Documentation fonctionnelle et technique | Conforme | `docs/functional-spec.md`, `docs/technical-architecture.md` |
| Site web achat/vente immobilier | Conforme | `apps/frontend` + `apps/backend` |
| Schema architecture reseau | Conforme | `docs/infra/network-architecture.md` |
| Plan adressage IP | Conforme | `docs/infra/ip-addressing-plan.md` |
| Politique securite | Conforme | `docs/infra/security-policy.md` |
| Gestion droits d'acces | Conforme | `docs/access-control-matrix.md` + AD/GPO |
| Guide configuration serveurs | Conforme | `docs/infra/server-configuration-guide.md` |
| Plan sauvegarde/supervision | Conforme | `docs/infra/backup-supervision-plan.md` |
| Proposition cloud | Conforme | `docs/infra/cloud-proposal.md` |
| Guide deploiement | Conforme | `docs/infra/deployment-guide.md` |
| Liste materiel + budget | Conforme | `docs/infra/hardware-budget.md` |
| Demonstration technique VM | Conforme | `docs/infra/demo-runbook.md`, `infra/runbooks/vm-lab-setup.md` |

---

## 5) Verdict de conformite

- Le projet est aligne avec la grille complete et les livrables obligatoires du brief.
- Le dossier contient les preuves et runbooks necessaires pour un passage oral robuste.
- Priorite pre-jury: repetition chronometree + captures de secours + verification infra live.
