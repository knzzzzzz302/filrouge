# Y-PLAZA — Plateforme immobilière

Projet Fil Rouge B2 — UF INFRA & DEV
Kenzi Amine BENDJELLOUL — Ynov Campus Montpellier

---

## Lancer le projet

```bash
python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install flask
python3 app.py
```

Puis ouvrir http://127.0.0.1:5000

La base de données `yplaza.db` se crée automatiquement au premier
lancement, avec 16 biens de démonstration et un compte agent.

---

## Accès

| Rôle             | Identifiant          | Mot de passe      |
|------------------|----------------------|-------------------|
| Agent (démo)     | agent@yplaza.fr      | Demo2026!         |
| Code agence      | —                    | yplaza2026agent   |

Le code agence est exigé pour créer un compte disposant du rôle Agent.

---

## Structure

```
app.py              Routes Flask uniquement — aucune requête SQL
models.py           Couche métier orientée objet
templates/          Gabarits Jinja2
static/uploads/     Photographies téléversées
```

### models.py — les classes

| Classe                | Rôle                                                  |
|-----------------------|-------------------------------------------------------|
| Database              | Encapsule les accès SQLite                            |
| Bien (abstraite)      | Bien immobilier — ne peut pas être instanciée         |
| Appartement, Maison,  | Héritent de Bien, redéfinissent coefficient_marche()  |
| LocalCommercial,      |                                                       |
| Terrain               |                                                       |
| User                  | Compte — mot de passe en écriture seule               |
| Estimateur            | Applique le barème de marché                          |
| *Repository           | Requêtes SQL regroupées par domaine                   |

Coefficients de marché : Appartement 1,00 · Maison 1,06 ·
Local commercial 0,85 · Terrain 0,28

---

## Fonctionnalités

- Catalogue avec recherche libre et quatre filtres combinables
- Fiche détaillée et biens similaires
- Inscription, connexion, rôles client et agent
- Publication, modification et retrait d'annonces (agents)
- Favoris
- Messagerie interne avec compteur de non-lus
- Estimateur : vente, budget d'achat, loyer, rendement
- Tableau de bord du marché avec graphiques

---

## Sécurité

- Mots de passe hachés, jamais restituables depuis le code
- Sessions signées côté serveur
- Contrôle des rôles côté serveur, pas seulement dans l'interface
- Requêtes SQL paramétrées
- Téléversement : liste blanche d'extensions, renommage UUID, 5 Mo max
- Code d'enrôlement requis pour le rôle agent

---

## Déploiement

Version en ligne : https://yplazakenz.pythonanywhere.com

Fichier WSGI :

```python
import sys
path = '/home/yplazakenz/yplaza-premium'
if path not in sys.path:
    sys.path.append(path)
from app import app as application, init_db
init_db()
```
