# Checklist de validation technique INFRA

## Reseau
- [ ] Plan IP complet valide (siege + 12 agences).
- [ ] Gateways et routes statiques/OSPF documentees.
- [ ] Segmentation VLAN appliquee.
- [ ] NAT operationnel pour sortie internet.

## VPN IPSec site-a-site
- [ ] Tunnel siege <-> agence pilote etabli.
- [ ] Chiffrement/IKE documentes.
- [ ] Tests ping inter-sites reussis.
- [ ] Policy de routage via VPN verifiee.

## AD / DNS / DHCP
- [ ] Domaine AD cree (OU + groupes + utilisateurs).
- [ ] DNS interne resolvant les noms AD et serveurs.
- [ ] DHCP operationnel sur au moins 1 site agence.
- [ ] GPO appliquees et verifiees par `gpresult`.

## Securite
- [ ] Politique pare-feu appliquee (deny by default).
- [ ] Acces admin restreint au VLAN Admin.
- [ ] Journalisation centralisee active.
- [ ] Matrice des droits coherent avec les groupes AD.

## Sauvegarde / supervision
- [ ] Sauvegardes planifiees + retention definie.
- [ ] Test de restauration effectue.
- [ ] Monitoring des services critiques actif.
- [ ] Alertes email/Teams configurees.

## Soutenance
- [ ] 1 VM serveur prete.
- [ ] 1-2 VM client/agence pretes.
- [ ] 1 routeur/firewall configure.
- [ ] Script de demo repete (10 min INFRA).
