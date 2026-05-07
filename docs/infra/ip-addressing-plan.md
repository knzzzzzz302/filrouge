# Plan d'adressage IP Y-Plaza

## Regles de construction
- CIDR standardise en `/24` par segment.
- Gateway en `.1` sur chaque reseau.
- Infrastructure statique reservee en `.2` a `.49`.
- Pool DHCP en `.100` a `.199`.
- Reservations imprimantes/equipements en `.200` a `.219`.

## Siege (Aix-en-Provence)
| Segment | VLAN | Reseau | Gateway | Usage |
|---|---:|---|---|---|
| Users-Siege | 10 | 10.10.10.0/24 | 10.10.10.1 | 30 postes |
| Servers-Siege | 20 | 10.10.20.0/24 | 10.10.20.1 | AD, DNS, DHCP, fichiers, supervision |
| Admin-Siege | 30 | 10.10.30.0/24 | 10.10.30.1 | Equipe IT et bastion |
| DMZ-Siege | 40 | 10.10.40.0/24 | 10.10.40.1 | Services exposes |

## Agences (5 postes + 1 imprimante/site)
| Agence | Reseau | Gateway | DHCP |
|---|---|---|---|
| Agence01 | 10.20.1.0/24 | 10.20.1.1 | 10.20.1.100-199 |
| Agence02 | 10.20.2.0/24 | 10.20.2.1 | 10.20.2.100-199 |
| Agence03 | 10.20.3.0/24 | 10.20.3.1 | 10.20.3.100-199 |
| Agence04 | 10.20.4.0/24 | 10.20.4.1 | 10.20.4.100-199 |
| Agence05 | 10.20.5.0/24 | 10.20.5.1 | 10.20.5.100-199 |
| Agence06 | 10.20.6.0/24 | 10.20.6.1 | 10.20.6.100-199 |
| Agence07 | 10.20.7.0/24 | 10.20.7.1 | 10.20.7.100-199 |
| Agence08 | 10.20.8.0/24 | 10.20.8.1 | 10.20.8.100-199 |
| Agence09 | 10.20.9.0/24 | 10.20.9.1 | 10.20.9.100-199 |
| Agence10 | 10.20.10.0/24 | 10.20.10.1 | 10.20.10.100-199 |
| Agence11 | 10.20.11.0/24 | 10.20.11.1 | 10.20.11.100-199 |
| Agence12 | 10.20.12.0/24 | 10.20.12.1 | 10.20.12.100-199 |

## Reseau VPN
- Supernet tunnels: `10.250.0.0/24`
- Hub (siege): `10.250.0.1`
- Spokes agences: `10.250.0.11` a `10.250.0.22`

## DNS / DHCP references
- DNS primaire: `10.10.20.10`
- DNS secondaire (optionnel): `10.10.20.11`
- DHCP central via relais sur les routeurs d'agence.
