# Politique de securite Y-Plaza

## Principes directeurs
- Moindre privilege et separation des roles.
- Zero trust interne simplifie: tout est interdit par defaut, ouverture explicite.
- Durcissement postes/serveurs par GPO.
- Traçabilite: logs centralises et horodatage coherent (NTP).

## Controle d'acces
- Comptes nominatifs obligatoires, partage de compte interdit.
- Groupes AD par metier (Direction, Commercial, RH/Juridique, IT).
- Groupes admin separes des comptes bureautiques.
- MFA obligatoire pour les acces admin et VPN admin.

## Politique mots de passe
- Longueur mini 12 caracteres.
- Historique des 10 derniers mots de passe.
- Expiration 90 jours (comptes privilegies) / 180 jours (standard).
- Verrouillage apres 5 tentatives (15 min).

## Regles pare-feu minimales
- Internet -> LAN: refuse.
- Internet -> DMZ: seulement ports publies (80/443 si necessaire).
- Agence -> Siege-Servers: DNS(53), DHCP-relay, LDAP/Kerberos/SMB selon besoin.
- Agence -> Admin VLAN: refuse.
- Inter-agences: refuse.
- Sortant serveurs: liste blanche (updates, sauvegarde, supervision).

## Durcissement endpoints et serveurs
- GPO: ecran verrouille 5 min, desactivation USB si politique metier, execution PowerShell restreinte.
- Antivirus/EDR actif et signatures a jour.
- Correctifs mensuels (patch Tuesday + fenetre de maintenance).

## Journalisation et supervision securite
- Centralisation syslog/events (90 jours minimum).
- Alertes en temps reel: echec login admin, tunnel VPN down, modification GPO critique.
- Revue hebdomadaire des journaux critiques.

## Sauvegardes et continuite
- Regle 3-2-1 (copie hors site ou cloud immuable).
- Sauvegardes chiffrees au repos et en transit.
- Test de restauration mensuel documente.
