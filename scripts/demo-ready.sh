#!/usr/bin/env bash
set -e

echo "[1/6] Data pipeline"
node data/scripts/clean-sales.js
node data/scripts/analytics.js

echo "[2/6] Backend install"
cd apps/backend
npm install

echo "[3/6] Backend checks"
npm run build
npm test

echo "[4/6] Frontend install"
cd ../frontend
npm install

echo "[5/6] Frontend checks"
npm run build
npm test

echo "[6/6] Ready"
echo "Projet pret pour demo technique (hors DB Docker/VM infra)."
