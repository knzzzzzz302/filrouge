# Memo jury INFRA (1 page)

## Objectif
Relier 1 siege + 12 agences avec une architecture securisee, administrable et evolutive.

## Architecture
- Topologie hub-and-spoke (siege = hub).
- Segmentation: Users, Servers, Admin, DMZ.
- Interconnexion via VPN IPSec site-a-site.

## Services critiques
- AD DS: identites, groupes, OU.
- DNS: resolution interne.
- DHCP: attribution IP centralisee.
- Pare-feu: deny-by-default, flux autorises au strict necessaire.

## Securite
- Moindre privilege + groupes AD metier.
- GPO: verrouillage session, policy mots de passe, pare-feu endpoint.
- Journalisation centralisee + alertes.

## Continuité
- Sauvegarde 3-2-1 chiffree.
- Tests de restauration mensuels.
- RPO/RTO documentes (cf. PRA/PCA).

## Demo en 5 preuves
1. Etat tunnel VPN: UP.
2. Poste agence recoit DHCP correct.
3. `nslookup` DNS interne reussi.
4. `gpresult` prouve GPO appliquee.
5. Regle pare-feu bloque un flux interdit.

## Valeur metier
- Administration centralisee multi-sites.
- Reduction surface d'attaque.
- Base solide pour extension cloud hybride.
