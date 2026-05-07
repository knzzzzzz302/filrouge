# Setup maquette VM (soutenance)

## Objectif minimum
- 1 VM serveur (Windows Server: AD/DNS/DHCP)
- 1 VM agence (Windows client)
- 1 routeur/firewall virtuel

## Topologie labo recommandee
- `vSwitch_Siege` (10.10.20.0/24 pour serveurs)
- `vSwitch_Agence01` (10.20.1.0/24)
- `vSwitch_WAN` (reseau transit VPN)

## Etapes
1. Creer VM `DC01` (Windows Server).
2. Configurer IP statique `10.10.20.10/24`, GW `10.10.20.1`.
3. Installer AD DS + DNS + DHCP.
4. Creer VM `AG01-CL01` (Windows 10/11).
5. Configurer DHCP sur agence via relay/routeur.
6. Joindre `AG01-CL01` au domaine `yplaza.local`.
7. Appliquer GPO de securite.
8. Verifier VPN UP entre agence et siege.

## Tests demo
- Login domaine sur poste agence.
- `nslookup dc01.yplaza.local`.
- `ipconfig /all` montre bail DHCP attendu.
- Ping serveur siege via tunnel.
