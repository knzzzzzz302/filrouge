# Ordre d'affichage ecran par ecran (oral INFRA)

## Sequence recommandee (10 min)
1. Ouvrir `docs/infra/network-architecture.md`
   - Expliquer topologie + segmentation.
2. Ouvrir `docs/infra/ip-addressing-plan.md`
   - Expliquer logique /24, gateways, DHCP ranges.
3. Ouvrir console AD (VM serveur)
   - Montrer OU + groupes + users.
4. Ouvrir terminal poste agence
   - `ipconfig /all`, `nslookup`, `gpresult`.
5. Ouvrir console firewall/VPN
   - Etat tunnel UP + regles filtrage.
6. Ouvrir `docs/infra/security-policy.md`
   - Relier aux controles vus en live.
7. Ouvrir `docs/infra/backup-supervision-plan.md`
   - Sauvegarde + supervision + alertes.
8. Ouvrir `docs/infra/cloud-proposal.md` puis `docs/infra/hardware-budget.md`
   - Vision cible + cout.

## Raccourci plan B (si panne)
1. `docs/infra/capture-evidence-checklist.md`
2. Captures INFRA_01 ... INFRA_08
3. `docs/infra/risk-and-fallback-plan.md`
