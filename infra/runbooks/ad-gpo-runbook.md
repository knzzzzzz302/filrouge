# Runbook AD/GPO (pas-a-pas)

## 1. Preparation du domaine
1. Promouvoir le serveur en controleur de domaine `yplaza.local`.
2. Verifier DNS integre AD actif.
3. Synchroniser l'heure NTP (critique Kerberos).

## 2. Organisation AD
1. Creer OU:
   - `OU=Siege,DC=yplaza,DC=local`
   - `OU=Agences,DC=yplaza,DC=local`
   - `OU=Serveurs,DC=yplaza,DC=local`
2. Creer sous-OU par agence (Agence01 ... Agence12).
3. Creer groupes:
   - `GG_Direction`
   - `GG_Commerciaux`
   - `GG_RH_Juridique`
   - `GG_IT_Admin`

## 3. Comptes et delegation
1. Creer comptes nominatifs et rattacher aux groupes metier.
2. Interdire comptes partages.
3. Deleguer administration locale aux profils IT uniquement.

## 4. GPO minimales a appliquer
1. `GPO_Security_Baseline`:
   - Verrouillage ecran 5 min
   - Mot de passe mini 12 caracteres
   - Lockout apres 5 tentatives
2. `GPO_Firewall_Endpoints`:
   - Pare-feu Windows actif
   - Blocage inbound non necessaire
3. `GPO_USB_Control` (si demande metier):
   - Restriction stockage USB hors exceptions

## 5. Validation
1. Sur poste test: `gpupdate /force`.
2. Verifier resultats: `gpresult /r`.
3. Controler event logs `GroupPolicy`.

## 6. Preuves pour soutenance
- Capture OU + groupes AD.
- Capture GPO liees aux OU.
- Capture `gpresult /r` sur poste agence.
