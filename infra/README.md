# Infra artifacts

- `topology/`: schema logique et flux reseau
- `vpn/`: exemples de configuration IPSec
- `runbooks/`: procedures AD, GPO, tests
- `firewall/`: matrice de regles et politique de filtrage

## Parcours recommande (ordre execution)
1. Lire `runbooks/vm-lab-setup.md`.
2. Appliquer `vpn/ipsec-template.conf` (adapter IP publiques).
3. Executer tests de `runbooks/network-test-plan.md`.
4. Verifier GPO via `runbooks/ad-gpo-runbook.md`.
5. Presenter les preuves en s'appuyant sur `docs/infra/evidence-matrix.md`.
