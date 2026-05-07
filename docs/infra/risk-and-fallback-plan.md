# Plan de risques et fallback soutenance

## Risques techniques
| Risque | Impact | Mitigation |
|---|---|---|
| Tunnel VPN down | Demo inter-site bloquee | Script de restart tunnel + captures de secours |
| DHCP KO | Clients sans IP | Scope de secours local agence + IP statique temporaire |
| DNS KO | Resolution de noms impossible | DNS secondaire configure |
| VM serveur lente/figee | Demo interrompue | Snapshot pre-demo + redemarrage rapide |
| Erreur manip live | Perte de temps oral | Runbook minute par minute imprime |

## Plan B demo
- Captures ecrans horodatees des etapes critiques.
- Export configuration routeur/firewall.
- Resultats de tests pre-enregistres (ping, tracert, gpresult).
- Ordre de repli:
  1) Montrer preuve capture.
  2) Expliquer cause probable.
  3) Presenter action corrective.

## RPO/RTO proposes
- RPO cible: 15 min (journaux + sauvegarde incrementale).
- RTO cible: 2h pour service AD/DNS/DHCP critique.
