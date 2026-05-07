# Plan sauvegarde et supervision

## Sauvegardes
- DB: full chaque nuit + WAL toutes 15 min
- Fichiers: incremental quotidien
- Tests de restauration mensuels
- Chiffrement: AES-256 au repos, TLS en transit
- Retention:
  - Quotidien: 30 jours
  - Hebdomadaire: 12 semaines
  - Mensuel: 12 mois

## Supervision
- Disponibilite API/DB
- CPU/RAM/disque serveurs
- Etat tunnels VPN
- Alertes email/Teams
- Seuils d'alerte:
  - CPU > 85% pendant 10 min
  - Disque > 80%
  - Tunnel VPN down > 2 min
- Escalade:
  1. IT support
  2. Admin reseau
  3. Responsable technique
