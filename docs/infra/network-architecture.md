# Architecture reseau Y-Plaza

## Objectif
Relier le siege et les 12 agences avec une architecture securisee, scalable et simple a exploiter.

## Topologie cible
- Mode hub-and-spoke: le siege est le hub, chaque agence est un spoke.
- Chaque agence est isolee des autres agences (pas de trafic lateral direct).
- Les flux inter-sites passent par des tunnels VPN IPSec.

## Segmentation par zones
- `VLAN10` Users-Siege (postes bureautiques).
- `VLAN20` Servers-Siege (AD/DNS/DHCP, fichiers, supervision, applicatif/DB).
- `VLAN30` Admin-Siege (bastion, administration reseau/serveurs).
- `VLAN40` DMZ-Siege (exposition controlee des services web).
- `VLAN50+` Agences (un sous-reseau par agence).

## Composants principaux
- 1 pare-feu/routeur central au siege.
- 1 equipement edge par agence (routeur ou firewall SMB).
- 2 serveurs au siege:
  - Serveur A: AD DS + DNS + DHCP.
  - Serveur B: Fichiers/sauvegarde/supervision + services applicatifs.
- Commutation manageable au siege et en agence.

## Flux autorises (principes)
- Agence -> Siege AD/DNS/DHCP: autorise.
- Agence -> Application metier (siege): autorise (HTTPS/API).
- Agence -> Admin VLAN: interdit.
- Agence -> autre Agence: interdit.
- DMZ -> LAN interne: interdit par defaut (exceptions explicites uniquement).

## Capacite et evolutivite
- Plan IP reserve pour 12 agences (extensible a 20+).
- Supervision des liens VPN et de la disponibilite des services critiques.
- Possibilite de migration hybride cloud sans rupture de plan d'adressage.
