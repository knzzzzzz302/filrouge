# PCA / PRA Y-Plaza (INFRA)

## Objectifs
- Assurer la continuite de service (PCA) pour les operations critiques.
- Assurer la reprise apres incident majeur (PRA) avec delais cibles.

## Services critiques
1. AD DS / DNS / DHCP
2. VPN IPSec inter-sites
3. Application metier et base de donnees
4. Sauvegarde et supervision

## Cibles de reprise
- RPO cible:
  - AD/DNS/DHCP: 1 heure
  - Base applicative: 15 minutes
- RTO cible:
  - AD/DNS/DHCP: 2 heures
  - Application metier: 4 heures

## Strategie PCA
- Redondance logique des roles critiques (DNS secondaire, sauvegardes planifiees).
- Segmentation reseau pour contenir les incidents.
- Supervision proactive + alerting en temps reel.

## Strategie PRA (scenario incident majeur serveur siege)
1. Detection et qualification incident.
2. Isolation composant impacte (reseau/serveur).
3. Bascule vers instance de secours (si disponible).
4. Restauration depuis sauvegarde validee.
5. Verification de conformite (DNS, DHCP, auth, VPN, app).
6. Rapport post-mortem et actions preventives.

## Plan de communication de crise
- Responsable technique: informe direction et equipes agence.
- Message type avec ETA de restauration.
- Point de situation toutes les 30 min pendant incident majeur.

## Exercices
- Test PRA trimestriel (table-top + test technique).
- Compte-rendu d'exercice avec ecarts et plan d'amelioration.
