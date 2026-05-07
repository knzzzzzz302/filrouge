# Matrice de politique pare-feu

| Source | Destination | Service/Port | Action | Justification |
|---|---|---|---|---|
| Internet | DMZ Web | TCP 443 | Allow | Publication portail web |
| Internet | LAN interne | Any | Deny | Protection reseau interne |
| Agences VLAN | DNS Siege | UDP/TCP 53 | Allow | Resolution DNS interne |
| Agences VLAN | AD Siege | LDAP/Kerberos/SMB | Allow (scope limite) | Authentification domaine |
| Agences VLAN | App Siege | TCP 443 | Allow | Acces plateforme Y-Plaza |
| Agences VLAN | Admin VLAN | Any | Deny | Limiter surface d'attaque |
| AgenceX | AgenceY | Any | Deny | Eviter mouvement lateral |
| Serveurs | Internet | Updates/NTP/Backup | Allow (whitelist) | Maintenance et sauvegarde |
| Admin VLAN | Equipements reseau | SSH/RDP/HTTPS | Allow | Administration ciblee |
| Any | Any | Any | Deny | Regle par defaut |

## Notes d'implementation
- Ordre des regles critique: autorisations precises avant deny global.
- Journaliser tous les denies critiques (inter-zones, admin, VPN).
