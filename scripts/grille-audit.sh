#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required_files=(
  "docs/functional-spec.md"
  "docs/technical-architecture.md"
  "docs/data-model.md"
  "docs/api-spec.md"
  "docs/access-control-matrix.md"
  "docs/infra/network-architecture.md"
  "docs/infra/ip-addressing-plan.md"
  "docs/infra/security-policy.md"
  "docs/infra/server-configuration-guide.md"
  "docs/infra/backup-supervision-plan.md"
  "docs/infra/cloud-proposal.md"
  "docs/infra/deployment-guide.md"
  "docs/infra/hardware-budget.md"
  "docs/infra/demo-runbook.md"
  "docs/grille-alignment.md"
  "docs/grille-conformite-complete-a-z.md"
  "docs/livrables-mandatoires-checklist.md"
)

echo "== Audit grille Y-Plaza =="
missing=0
for file in "${required_files[@]}"; do
  if [[ -f "$ROOT/$file" ]]; then
    echo "[OK] $file"
  else
    echo "[MISSING] $file"
    missing=$((missing + 1))
  fi
done

if [[ $missing -gt 0 ]]; then
  echo "Resultat: $missing livrable(s) manquant(s)."
  exit 1
fi

echo "Resultat: conformite documentaire complete."
