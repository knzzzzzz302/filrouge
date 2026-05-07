# Script oral INFRA (10 minutes)

## 0:00 - 0:45 Introduction
"Bonjour, nous presentons l'architecture INFRA Y-Plaza. Notre objectif est de relier un siege a 12 agences avec une infrastructure securisee, administrable et evolutive."

## 0:45 - 2:15 Architecture reseau
"Nous avons choisi une topologie hub-and-spoke: le siege est le hub, les agences sont les spokes.  
Le reseau est segmente en VLAN Users, Servers, Admin et DMZ pour limiter les mouvements lateraux.  
Les flux inter-sites passent par des tunnels VPN IPSec."

## 2:15 - 3:30 Plan IP
"Le plan IP est standardise en /24 par segment.  
Chaque agence a son sous-reseau dedie en 10.20.X.0/24.  
Le siege utilise des sous-reseaux separes pour utilisateurs, serveurs, admin et DMZ."

## 3:30 - 5:30 Services AD / DNS / DHCP / GPO
"Le serveur central heberge AD DS, DNS et DHCP.  
Nous avons cree des OU et groupes metier pour appliquer le moindre privilege.  
Les GPO imposent les regles de securite: verrouillage session, politique de mot de passe et pare-feu endpoint."

## 5:30 - 7:00 Securite reseau
"Les regles pare-feu appliquent un deny-by-default.  
Les agences accedent aux services necessaires au siege, mais pas au VLAN Admin ni aux autres agences.  
La journalisation centralisee permet d'auditer les evenements critiques."

## 7:00 - 8:30 Sauvegarde et supervision
"Nous appliquons la regle 3-2-1 avec sauvegardes chiffrees.  
Les tests de restauration sont planifies mensuellement.  
La supervision couvre disponibilite services, ressources systeme et etat des tunnels VPN."

## 8:30 - 9:30 Demonstration en direct
"Nous montrons: tunnel VPN UP, bail DHCP agence, resolution DNS interne, login domaine et acces applicatif autorise."

## 9:30 - 10:00 Conclusion
"Cette architecture repond aux exigences de securite, d'exploitation et de scalabilite du cahier des charges.  
Les prochaines etapes sont l'industrialisation cloud hybride et l'automatisation des controles de conformite."
