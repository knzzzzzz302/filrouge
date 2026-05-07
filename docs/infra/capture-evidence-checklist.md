# Checklist captures de preuves (jury INFRA)

## Avant demo
- [ ] Horloge systeme visible (date/heure)
- [ ] Nom des VMs visible (serveur, agence, routeur)
- [ ] Fichiers docs ouverts (architecture + IP + securite)

## Captures obligatoires
- [ ] Schema architecture reseau final
- [ ] Tableau plan d'adressage IP complet
- [ ] Etat tunnel VPN IPSec (UP)
- [ ] Ping agence -> serveur siege (reussi)
- [ ] `nslookup` domaine interne depuis agence
- [ ] `ipconfig /all` avec bail DHCP attendu
- [ ] Console AD: OU + groupes + utilisateurs
- [ ] `gpresult /r` prouvant application GPO
- [ ] Extrait regles pare-feu (allow/deny)
- [ ] Tableau sauvegarde/supervision

## Captures de secours (plan B)
- [ ] Resultat d'un test de restauration
- [ ] Dashboard supervision (service UP/DOWN)
- [ ] Export configuration VPN/routeur
- [ ] Journal evenement securite (tentative refusee)

## Convention nommage fichiers
- `INFRA_01_architecture.png`
- `INFRA_02_plan_ip.png`
- `INFRA_03_vpn_up.png`
- `INFRA_04_dns_nslookup.png`
- `INFRA_05_dhcp_bail.png`
- `INFRA_06_ad_ou_groupes.png`
- `INFRA_07_gpresult.png`
- `INFRA_08_firewall_rules.png`
