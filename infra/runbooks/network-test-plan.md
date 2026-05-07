# Plan de test reseau (recette INFRA)

## Prerequis
- VM serveur siege demarree (AD/DNS/DHCP).
- VM agence demarree et jointe au reseau agence.
- Equipement VPN/routeur actif.

## Tests connectivite
1. Ping `GatewayAgence` depuis un poste agence.
2. Ping `10.10.20.10` (DNS/AD siege) depuis agence.
3. `tracert 10.10.20.10` pour verifier passage via tunnel.

## Tests DNS
1. `nslookup dc01.yplaza.local` depuis agence.
2. `nslookup app.yplaza.local` depuis siege et agence.
3. Verifier qu'aucune resolution interne n'utilise DNS public.

## Tests DHCP
1. Renouveler le bail (`ipconfig /release`, `/renew`).
2. Verifier plage attendue (ex: `10.20.X.100-199`).
3. Verifier options DNS/Gateway poussees.

## Tests VPN IPSec
1. Etat tunnel `UP` sur hub et spoke.
2. Verification IKEv2 + suite chiffrement conforme.
3. Coupure/reprise lien WAN: tunnel doit se relever.

## Tests pare-feu et segmentation
1. Agence -> Admin VLAN siege: doit etre bloque.
2. Agence -> Serveur applicatif siege: autorise HTTPS/API.
3. Inter-agences: bloque.

## Critere d'acceptation
- 100% des tests critiques (VPN, DNS, DHCP, segmentation) validés.
- Toute anomalie documentee avec action corrective et date cible.
