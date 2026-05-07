# Commandes demo INFRA (cheatsheet)

## Poste agence (Windows)
- Renouveler DHCP:
  - `ipconfig /release`
  - `ipconfig /renew`
- Afficher configuration IP:
  - `ipconfig /all`
- Tester DNS:
  - `nslookup dc01.yplaza.local`
- Tester connectivite siege:
  - `ping 10.10.20.10`
  - `tracert 10.10.20.10`
- Verifier GPO:
  - `gpupdate /force`
  - `gpresult /r`

## Serveur AD (Windows Server)
- Verifier services:
  - `Get-Service DNS,DHCPServer,NTDS`
- Verifier scope DHCP:
  - `Get-DhcpServerv4Scope`
- Verifier baux DHCP:
  - `Get-DhcpServerv4Lease -ScopeId 10.20.1.0`

## Routeur/Firewall (exemple IPSec)
- Verifier tunnels:
  - `ipsec statusall` (strongSwan)
- Reload config:
  - `ipsec reload`
- Restart tunnel:
  - `ipsec down yplaza-agency01 && ipsec up yplaza-agency01`

## Rappel oral
- Montrer chaque commande + resultat attendu en 20-30 sec max.
- Si incident: basculer immediatement vers captures de secours.
