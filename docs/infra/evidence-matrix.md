# Matrice de preuves pour le jury INFRA

| Critere jury | Preuve a montrer en direct | Fichier/preuve support |
|---|---|---|
| Architecture reseau securisee | Schema reseau + explication flux | `docs/infra/network-architecture.md` |
| Plan d'adressage IP | Tableau IP siege/agences | `docs/infra/ip-addressing-plan.md` |
| Configuration serveurs | AD, DNS, DHCP visibles sur VM serveur | `docs/infra/server-configuration-guide.md` |
| Gestion des droits | Groupes AD + GPO appliquees | `docs/access-control-matrix.md` + capture `gpresult` |
| VPN site-a-site | Etat tunnel UP + ping inter-site | `infra/vpn/ipsec-template.conf` + captures |
| Politique de securite | Regles pare-feu, segmentation, logs | `docs/infra/security-policy.md` |
| Sauvegarde/supervision | Job backup + dashboard monitoring | `docs/infra/backup-supervision-plan.md` |
| Cloud/hybride | Argumentaire cout/benefice | `docs/infra/cloud-proposal.md` |
| Budgetisation | Tableau materiel + cout total | `docs/infra/hardware-budget.md` |
| Qualite de demo | Scenario 10 min maitrise | `docs/oral-outline.md` + `docs/demo-script.md` |
