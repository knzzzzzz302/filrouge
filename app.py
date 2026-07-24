# ============================================================
# Y-PLAZA v3 — Plateforme immobilière complète
# Flask + SQLite.
#
# v3 :
#   - Landing page (/) + catalogue (/biens)
#   - Photos sur les annonces (banque Unsplash, libre de droits)
#   - Code agence obligatoire pour créer un compte Agent
#   - Estimateur vente / budget achat / loyer, basé sur un
#     barème de prix au m² du marché français (réf. 2026)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os
import uuid

app = Flask(__name__)
app.secret_key = "yplaza-fil-rouge-b2-secret"
DB_PATH = os.path.join(os.path.dirname(__file__), "yplaza.db")

# --- Upload d'images : règles de sécurité ---
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
EXTENSIONS_OK = {"jpg", "jpeg", "png", "webp"}          # liste blanche stricte
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024      # 5 Mo max par requête


def fichier_autorise(nom):
    """Vérifie l'extension contre la liste blanche."""
    return "." in nom and nom.rsplit(".", 1)[1].lower() in EXTENSIONS_OK


def sauver_image(fichier):
    """Enregistre l'image avec un nom ALÉATOIRE (uuid) pour empêcher
    l'écrasement de fichiers et l'exécution de noms malveillants.
    Retourne le chemin web ou None."""
    if not fichier or fichier.filename == "":
        return None
    if not fichier_autorise(fichier.filename):
        return None
    ext = fichier.filename.rsplit(".", 1)[1].lower()
    nom = f"{uuid.uuid4().hex}.{ext}"                    # jamais le nom d'origine
    fichier.save(os.path.join(UPLOAD_DIR, nom))
    return f"/static/uploads/{nom}"

# Code confidentiel remis aux agents par la direction
CODE_AGENT = "yplaza2026agent"

# ------------------------------------------------------------
# BARÈME MARCHÉ FRANÇAIS (réf. début 2026, ordre de grandeur
# des prix médians constatés). Utilisé par l'estimateur.
# ------------------------------------------------------------
PRIX_M2 = {
    "Paris": 9400, "Nice": 5300, "Aix-en-Provence": 5100, "Lyon": 4600,
    "Bordeaux": 4400, "Cassis": 7600, "Annecy": 5900, "Nantes": 3700,
    "Marseille": 3600, "Montpellier": 3500, "Toulouse": 3400,
    "Strasbourg": 3800, "Lille": 3300, "Rennes": 3900,
    "Avignon": 2600, "Saint-Rémy-de-Provence": 4300, "Gordes": 6200,
    "Lourmarin": 5400, "Sanary-sur-Mer": 6300, "Salon-de-Provence": 2900,
    "Aubagne": 3300, "Grenoble": 2900, "Dijon": 2800, "Reims": 2700,
    "Le Havre": 2200, "Saint-Étienne": 1500, "Perpignan": 2100,
}
LOYER_M2 = {
    "Paris": 31.0, "Nice": 18.5, "Aix-en-Provence": 17.5, "Lyon": 16.0,
    "Bordeaux": 15.5, "Cassis": 19.0, "Annecy": 17.0, "Nantes": 13.5,
    "Marseille": 15.0, "Montpellier": 15.5, "Toulouse": 13.5,
    "Strasbourg": 13.5, "Lille": 14.0, "Rennes": 13.5,
    "Avignon": 11.5, "Saint-Rémy-de-Provence": 14.0, "Gordes": 15.0,
    "Lourmarin": 14.0, "Sanary-sur-Mer": 16.0, "Salon-de-Provence": 12.0,
    "Aubagne": 13.0, "Grenoble": 13.0, "Dijon": 11.5, "Reims": 11.0,
    "Le Havre": 10.0, "Saint-Étienne": 8.5, "Perpignan": 10.5,
}
COEF_TYPE = {"Appartement": 1.00, "Maison": 1.06, "Local commercial": 0.85, "Terrain": 0.28}
COEF_ETAT = {"Neuf ou refait": 1.10, "Bon état": 1.00, "Travaux à prévoir": 0.83}
FRAIS_NOTAIRE_ANCIEN = 0.075  # ~7,5 % dans l'ancien


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ------------------------------------------------------------
# Biens de démonstration (photos Unsplash, libres de droits)
# ------------------------------------------------------------
U = "https://images.unsplash.com/"
IMG = lambda pid: f"{U}{pid}?auto=format&fit=crop&w=900&q=75"

BIENS_DEMO = [
    ("Bastide provençale rénovée", "Maison", "Aix-en-Provence", 1250000, 240, 7,
     "Bastide du XVIIIe entièrement restaurée, oliveraie de 8000 m², piscine à débordement, vue Sainte-Victoire.",
     "A vendre", IMG("photo-1600596542815-ffad4c1539a9")),
    ("Appartement haussmannien Cours Mirabeau", "Appartement", "Aix-en-Provence", 685000, 128, 4,
     "Étage noble, moulures et parquets d'origine, 3 chambres, balcon filant sur le Cours.",
     "A vendre", IMG("photo-1522708323590-d24dbb6b0267")),
    ("Loft atelier d'artiste", "Appartement", "Marseille", 495000, 145, 3,
     "Ancien atelier réhabilité au Panier, verrière zénithale, hauteur sous plafond 4,5 m.",
     "En négociation", IMG("photo-1493809842364-78817add7ffb")),
    ("Villa contemporaine vue mer", "Maison", "Cassis", 1890000, 210, 6,
     "Architecture contemporaine, baies toute hauteur, piscine miroir, accès calanques à pied.",
     "A vendre", IMG("photo-1613490493576-7fde63acd811")),
    ("Mas viticole et ses dépendances", "Maison", "Lourmarin", 2400000, 380, 9,
     "Mas en pierre au cœur du Luberon, 4 ha de vignes AOC, cave voûtée, maison d'amis.",
     "A vendre", IMG("photo-1600585154340-be6161a56a0c")),
    ("T3 lumineux quartier Mazarin", "Appartement", "Aix-en-Provence", 420000, 82, 3,
     "Immeuble en pierre de taille, double exposition, cave et grenier.",
     "Vendu", IMG("photo-1560448204-e02f11c3d0e2")),
    ("Penthouse terrasse panoramique", "Appartement", "Marseille", 890000, 160, 5,
     "Dernier étage, terrasse de 90 m² vue Notre-Dame de la Garde, 2 parkings.",
     "A vendre", IMG("photo-1512917774080-9991f1c4c750")),
    ("Local commercial rue piétonne", "Local commercial", "Avignon", 310000, 95, 2,
     "Emplacement n°1 intra-muros, vitrine 8 m, bail tous commerces.",
     "A vendre", IMG("photo-1441986300917-64674bd600d8")),
    ("Maison de village et patio", "Maison", "Saint-Rémy-de-Provence", 560000, 150, 5,
     "Maison de caractère au centre du village, patio ombragé, garage attenant.",
     "En négociation", IMG("photo-1600047509807-ba8f99d2cdde")),
    ("Terrain constructible viabilisé", "Terrain", "Aubagne", 245000, 900, 0,
     "Parcelle plane et viabilisée, quartier résidentiel calme, CU opérationnel.",
     "A vendre", IMG("photo-1500382017468-9049fed747ef")),
    ("Duplex design Vieux-Port", "Appartement", "Marseille", 720000, 118, 4,
     "Duplex refait par architecte, cuisine Bulthaup, vue port depuis le séjour.",
     "A vendre", IMG("photo-1600607687920-4e2a09cf159d")),
    ("Bergerie restaurée et son domaine", "Maison", "Gordes", 1650000, 195, 6,
     "Pierre sèche restaurée dans les règles de l'art, 2 ha, vue vallée, calme absolu.",
     "A vendre", IMG("photo-1564013799919-ab600027ffc6")),
    ("Bureaux neufs quartier d'affaires", "Local commercial", "Aix-en-Provence", 540000, 210, 6,
     "Plateau livré brut de béton, parc de la Duranne, 12 places de parking.",
     "A vendre", IMG("photo-1497366216548-37526070297c")),
    ("Studio investisseur centre ancien", "Appartement", "Avignon", 128000, 28, 1,
     "Loué 520 €/mois, rentabilité brute 4,9 %, faibles charges.",
     "Vendu", IMG("photo-1502672260266-1c1ef2d93688")),
    ("Villa pieds dans l'eau", "Maison", "Sanary-sur-Mer", 2150000, 185, 6,
     "Accès mer direct, ponton privé, rénovée en 2024, prestations hôtelières.",
     "En négociation", IMG("photo-1600566753086-00f18fb6b3ea")),
    ("Ferme équestre en activité", "Maison", "Salon-de-Provence", 980000, 320, 8,
     "Carrière 60x25, 18 boxes, fourrière, maison principale et logement gardien.",
     "A vendre", IMG("photo-1560185127-6ed189bf02f4")),
]


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS biens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL, type TEXT NOT NULL, ville TEXT NOT NULL,
            prix REAL NOT NULL, surface REAL NOT NULL,
            pieces INTEGER NOT NULL DEFAULT 0,
            description TEXT, statut TEXT NOT NULL DEFAULT 'A vendre',
            image_url TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'client'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bien_id INTEGER NOT NULL,
            expediteur_id INTEGER NOT NULL,
            contenu TEXT NOT NULL,
            date_envoi TEXT DEFAULT (datetime('now','localtime')),
            lu INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS favoris (
            user_id INTEGER NOT NULL, bien_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, bien_id)
        )
    """)
    if conn.execute("SELECT COUNT(*) c FROM biens").fetchone()["c"] == 0:
        conn.executemany(
            "INSERT INTO biens (titre,type,ville,prix,surface,pieces,description,statut,image_url) VALUES (?,?,?,?,?,?,?,?,?)",
            BIENS_DEMO,
        )
    if conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"] == 0:
        conn.execute(
            "INSERT INTO users (nom,email,password_hash,role) VALUES (?,?,?,?)",
            ("Agent Y-Plaza", "agent@yplaza.fr", generate_password_hash("Demo2026!"), "agent"),
        )
    conn.commit()
    conn.close()


# ------------------------------------------------------------
# Auth helpers
# ------------------------------------------------------------
def current_user():
    uid = session.get("user_id")
    if uid is None:
        return None
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return user


@app.context_processor
def inject_user():
    return {"user": current_user()}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Connectez-vous pour accéder à cette page.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def agent_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        if u is None or u["role"] != "agent":
            flash("Accès réservé aux agents Y-Plaza.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ------------------------------------------------------------
# Inscription (avec code agence) / Connexion / Déconnexion
# ------------------------------------------------------------
@app.route("/inscription", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom = request.form["nom"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        role = request.form.get("role", "client")
        code = request.form.get("code_agent", "").strip()

        if role == "agent" and code != CODE_AGENT:
            flash("Code agence invalide. Le compte Agent nécessite le code fourni par la direction.")
            return render_template("register.html")
        if role not in ("client", "agent"):
            role = "client"
        if len(password) < 8:
            flash("Le mot de passe doit contenir au moins 8 caractères.")
            return render_template("register.html")

        conn = get_db()
        if conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
            conn.close()
            flash("Un compte existe déjà avec cet email.")
            return render_template("register.html")
        conn.execute(
            "INSERT INTO users (nom,email,password_hash,role) VALUES (?,?,?,?)",
            (nom, email, generate_password_hash(password), role),
        )
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        session["user_id"] = user["id"]
        flash(f"Bienvenue {nom} !")
        return redirect(url_for("landing"))
    return render_template("register.html")


@app.route("/connexion", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Email ou mot de passe incorrect.")
            return render_template("login.html")
        session["user_id"] = user["id"]
        flash(f"Ravi de vous revoir, {user['nom']} !")
        return redirect(url_for("landing"))
    return render_template("login.html")


@app.route("/deconnexion")
def logout():
    session.clear()
    flash("Vous êtes déconnecté.")
    return redirect(url_for("landing"))


# ------------------------------------------------------------
# Favoris
# ------------------------------------------------------------
def user_fav_ids():
    u = current_user()
    if u is None:
        return set()
    conn = get_db()
    rows = conn.execute("SELECT bien_id FROM favoris WHERE user_id=?", (u["id"],)).fetchall()
    conn.close()
    return {r["bien_id"] for r in rows}


@app.route("/favori/<int:bien_id>", methods=["POST"])
@login_required
def toggle_favori(bien_id):
    u = current_user()
    conn = get_db()
    if conn.execute("SELECT 1 FROM favoris WHERE user_id=? AND bien_id=?", (u["id"], bien_id)).fetchone():
        conn.execute("DELETE FROM favoris WHERE user_id=? AND bien_id=?", (u["id"], bien_id))
    else:
        conn.execute("INSERT INTO favoris (user_id,bien_id) VALUES (?,?)", (u["id"], bien_id))
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for("biens"))


@app.route("/mes-favoris")
@login_required
def favoris():
    u = current_user()
    conn = get_db()
    biens_list = conn.execute("""
        SELECT b.* FROM biens b JOIN favoris f ON f.bien_id=b.id
        WHERE f.user_id=? ORDER BY b.id DESC
    """, (u["id"],)).fetchall()
    conn.close()
    return render_template("favoris.html", biens=biens_list, favs=user_fav_ids())


# ------------------------------------------------------------
# Messagerie : un client écrit sur un bien, les agents lisent
# ------------------------------------------------------------
@app.route("/message/<int:bien_id>", methods=["POST"])
@login_required
def envoyer_message(bien_id):
    u = current_user()
    contenu = request.form.get("contenu", "").strip()
    if not contenu:
        flash("Le message est vide.")
        return redirect(url_for("detail", bien_id=bien_id))
    conn = get_db()
    conn.execute(
        "INSERT INTO messages (bien_id, expediteur_id, contenu) VALUES (?,?,?)",
        (bien_id, u["id"], contenu),
    )
    conn.commit(); conn.close()
    flash("Message envoyé à l'agence.")
    return redirect(url_for("detail", bien_id=bien_id))


@app.route("/messagerie")
@agent_required
def messagerie():
    conn = get_db()
    msgs = conn.execute("""
        SELECT m.*, u.nom AS expediteur, u.email, b.titre AS bien_titre, b.id AS bid
        FROM messages m
        JOIN users u ON u.id = m.expediteur_id
        JOIN biens b ON b.id = m.bien_id
        ORDER BY m.id DESC
    """).fetchall()
    # Marque tout comme lu à l'ouverture
    conn.execute("UPDATE messages SET lu = 1")
    conn.commit(); conn.close()
    return render_template("messagerie.html", msgs=msgs)


def nb_messages_non_lus():
    u = current_user()
    if u is None or u["role"] != "agent":
        return 0
    conn = get_db()
    n = conn.execute("SELECT COUNT(*) c FROM messages WHERE lu = 0").fetchone()["c"]
    conn.close()
    return n


@app.context_processor
def inject_unread():
    return {"non_lus": nb_messages_non_lus()}


# ------------------------------------------------------------
# Landing page
# ------------------------------------------------------------
@app.route("/")
def landing():
    conn = get_db()
    vedettes = conn.execute(
        "SELECT * FROM biens WHERE statut='A vendre' ORDER BY prix DESC LIMIT 3"
    ).fetchall()
    stats = conn.execute("""
        SELECT COUNT(*) total,
               SUM(CASE WHEN statut='A vendre' THEN 1 ELSE 0 END) en_vente,
               AVG(prix/surface) prix_m2
        FROM biens
    """).fetchone()
    conn.close()
    return render_template("landing.html", vedettes=vedettes, stats=stats, favs=user_fav_ids())


# ------------------------------------------------------------
# Catalogue : liste + recherche + filtres
# ------------------------------------------------------------
@app.route("/biens")
def biens():
    q = request.args.get("q", "").strip()
    ville = request.args.get("ville", "")
    type_bien = request.args.get("type", "")
    statut = request.args.get("statut", "")
    prix_max = request.args.get("prix_max", "")

    sql = "SELECT * FROM biens WHERE 1=1"
    params = []
    if q:
        sql += " AND (titre LIKE ? OR description LIKE ? OR ville LIKE ?)"
        like = f"%{q}%"
        params += [like, like, like]
    if ville:
        sql += " AND ville = ?"; params.append(ville)
    if type_bien:
        sql += " AND type = ?"; params.append(type_bien)
    if statut:
        sql += " AND statut = ?"; params.append(statut)
    if prix_max:
        sql += " AND prix <= ?"; params.append(float(prix_max))
    sql += " ORDER BY id DESC"

    conn = get_db()
    biens_list = conn.execute(sql, params).fetchall()
    villes = [r["ville"] for r in conn.execute("SELECT DISTINCT ville FROM biens ORDER BY ville")]
    stats = conn.execute("""
        SELECT COUNT(*) total,
               SUM(CASE WHEN statut='A vendre' THEN 1 ELSE 0 END) en_vente,
               AVG(prix) prix_moyen, AVG(prix/surface) prix_m2
        FROM biens
    """).fetchone()
    conn.close()
    return render_template("index.html", biens=biens_list, villes=villes, stats=stats,
                           favs=user_fav_ids(),
                           q=q, ville=ville, type_bien=type_bien, statut=statut, prix_max=prix_max)


# ------------------------------------------------------------
# Estimateur (vente / budget achat / loyer)
# ------------------------------------------------------------
@app.route("/estimation", methods=["GET", "POST"])
def estimation():
    resultat = None
    if request.method == "POST":
        ville = request.form["ville"]
        type_bien = request.form["type"]
        surface = float(request.form["surface"])
        etat = request.form["etat"]

        base_m2 = PRIX_M2.get(ville, 3000)          # défaut si ville inconnue
        loyer_m2 = LOYER_M2.get(ville, 12.0)
        coef = COEF_TYPE.get(type_bien, 1.0) * COEF_ETAT.get(etat, 1.0)

        valeur = base_m2 * surface * coef
        loyer = loyer_m2 * surface * COEF_ETAT.get(etat, 1.0)
        if type_bien == "Terrain":
            loyer = 0  # un terrain nu ne se loue pas en résidentiel

        resultat = {
            "ville": ville, "type": type_bien, "surface": surface, "etat": etat,
            "prix_m2_ref": base_m2,
            "vente_basse": valeur * 0.93,
            "vente": valeur,
            "vente_haute": valeur * 1.07,
            "notaire": valeur * FRAIS_NOTAIRE_ANCIEN,
            "budget_achat": valeur * (1 + FRAIS_NOTAIRE_ANCIEN),
            "loyer": loyer,
            "rendement": (loyer * 12 / valeur * 100) if valeur and loyer else 0,
        }
    return render_template("estimation.html", villes=sorted(PRIX_M2.keys()), resultat=resultat)


# ------------------------------------------------------------
# Détail
# ------------------------------------------------------------
@app.route("/bien/<int:bien_id>")
def detail(bien_id):
    conn = get_db()
    bien = conn.execute("SELECT * FROM biens WHERE id=?", (bien_id,)).fetchone()
    if bien is None:
        conn.close()
        return redirect(url_for("biens"))
    similaires = conn.execute(
        "SELECT * FROM biens WHERE id != ? AND (ville=? OR type=?) ORDER BY RANDOM() LIMIT 3",
        (bien_id, bien["ville"], bien["type"]),
    ).fetchall()
    conn.close()
    return render_template("detail.html", bien=bien, similaires=similaires, favs=user_fav_ids())


# ------------------------------------------------------------
# CRUD — agents uniquement
# ------------------------------------------------------------
def _form_values():
    # Un fichier uploadé est prioritaire sur l'URL saisie
    image = sauver_image(request.files.get("image_fichier"))
    if image is None:
        image = request.form.get("image_url", "").strip() or None
    return (
        request.form["titre"], request.form["type"], request.form["ville"],
        float(request.form["prix"]), float(request.form["surface"]),
        int(request.form.get("pieces") or 0),
        request.form["description"], request.form["statut"],
        image,
    )


@app.route("/ajouter", methods=["GET", "POST"])
@agent_required
def ajouter():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO biens (titre,type,ville,prix,surface,pieces,description,statut,image_url) VALUES (?,?,?,?,?,?,?,?,?)",
            _form_values(),
        )
        conn.commit(); conn.close()
        flash("Bien publié.")
        return redirect(url_for("biens"))
    return render_template("form.html", bien=None, action="Publier le bien", titre_page="Nouveau bien")


@app.route("/modifier/<int:bien_id>", methods=["GET", "POST"])
@agent_required
def modifier(bien_id):
    conn = get_db()
    if request.method == "POST":
        conn.execute(
            "UPDATE biens SET titre=?,type=?,ville=?,prix=?,surface=?,pieces=?,description=?,statut=?,image_url=? WHERE id=?",
            _form_values() + (bien_id,),
        )
        conn.commit(); conn.close()
        flash("Fiche mise à jour.")
        return redirect(url_for("detail", bien_id=bien_id))
    bien = conn.execute("SELECT * FROM biens WHERE id=?", (bien_id,)).fetchone()
    conn.close()
    return render_template("form.html", bien=bien, action="Enregistrer", titre_page="Modifier le bien")


@app.route("/supprimer/<int:bien_id>", methods=["POST"])
@agent_required
def supprimer(bien_id):
    conn = get_db()
    conn.execute("DELETE FROM biens WHERE id=?", (bien_id,))
    conn.execute("DELETE FROM favoris WHERE bien_id=?", (bien_id,))
    conn.commit(); conn.close()
    flash("Bien supprimé.")
    return redirect(url_for("biens"))


# ------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    par_ville = conn.execute("""
        SELECT ville, COUNT(*) nb, AVG(prix) prix_moyen, AVG(prix/surface) prix_m2
        FROM biens GROUP BY ville ORDER BY prix_m2 DESC
    """).fetchall()
    par_type = conn.execute("SELECT type, COUNT(*) nb FROM biens GROUP BY type ORDER BY nb DESC").fetchall()
    par_statut = conn.execute("SELECT statut, COUNT(*) nb FROM biens GROUP BY statut").fetchall()
    stats = conn.execute("""
        SELECT COUNT(*) total, AVG(prix) prix_moyen, MIN(prix) prix_min,
               MAX(prix) prix_max, AVG(prix/surface) prix_m2
        FROM biens
    """).fetchone()
    conn.close()
    return render_template("dashboard.html", par_ville=par_ville, par_type=par_type,
                           par_statut=par_statut, stats=stats)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
