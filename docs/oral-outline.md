# Trame oral INFRA (10 min)

## 0:00 - 1:00 Contexte et objectif
- Rappel du besoin Y-Plaza: 1 siege + 12 agences.
- Enjeu: connectivite securisee + administration centralisee.

## 1:00 - 3:00 Architecture reseau
- Schema topologique hub-and-spoke.
- Segmentation VLAN (Users/Servers/Admin/DMZ).
- Flux autorises/interdits.

## 3:00 - 4:30 Plan IP
- Methode de construction du plan.
- Exemple siege + 2 agences.
- Reseau VPN et passerelles.

## 4:30 - 6:30 Services infra
- AD DS: OU, groupes, delegation.
- DNS/DHCP: resolution et attribution IP.
- GPO: durcissement postes.

## 6:30 - 8:00 Securite
- Politique pare-feu et filtrage inter-zones.
- Gestion des droits et moindre privilege.
- Sauvegarde et supervision (alertes critiques).

## 8:00 - 9:30 Demo technique
- VM serveur + VM agence + routeur.
- Preuves: tunnel VPN up, login domaine, DNS, DHCP, acces applicatif.

## 9:30 - 10:00 Conclusion
- Risques restants + plan de mitigation.
- Roadmap d'industrialisation.
