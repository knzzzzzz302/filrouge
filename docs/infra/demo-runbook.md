# Runbook demo INFRA (10 minutes)

## Pre-check (avant passage)
- Ouvrir les 3 VMs (serveur, agence, routeur/firewall).
- Verifier tunnel VPN actif.
- Verifier service AD DS, DNS, DHCP demarres.
- Avoir captures de secours en cas d'aléa.

## Minute par minute
1. **0:00-1:00**: Presenter l'architecture globale et les objectifs.
2. **1:00-2:30**: Montrer le plan IP (siege + agence pilote).
3. **2:30-4:00**: Montrer AD (OU, groupes, users) + logique des droits.
4. **4:00-5:00**: Montrer une GPO appliquee (ex: verrouillage session).
5. **5:00-6:30**: Montrer DNS/DHCP (bail adresse agence).
6. **6:30-8:00**: Montrer VPN IPSec (etat UP + ping inter-site).
7. **8:00-9:00**: Montrer securite (regles firewall et logs).
8. **9:00-10:00**: Conclure: sauvegarde/supervision + cloud + budget.

## Questions frequentes jury
- Pourquoi hub-and-spoke et pas full mesh ?
- Comment vous limitez les mouvements lateraux ?
- Que se passe-t-il si le serveur AD tombe ?
- Quel est votre RPO/RTO sur les donnees critiques ?
