# ============================================================
# Y-PLAZA v5 — Plateforme immobilière (Projet Fil Rouge B2)
#
# ARCHITECTURE EN COUCHES :
#   models.py  → couche métier orientée objet (classes Bien, User,
#                Estimateur, Database, Repositories)
#   app.py     → couche présentation : routes Flask uniquement.
#                Aucune requête SQL n'est écrite ici, tout passe
#                par les repositories. Séparation des responsabilités.
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os
import uuid

from models import (
    Database, Bien, User, Estimateur,
    BienRepository, UserRepository, FavoriRepository, MessageRepository,
)

app = Flask(__name__)
app.secret_key = "yplaza-fil-rouge-b2-secret"

# --- Upload d'images : règles de sécurité ---
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
EXTENSIONS_OK = {"jpg", "jpeg", "png", "webp"}     # liste blanche stricte
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 Mo max

# Code confidentiel remis aux agents par la direction
CODE_AGENT = "yplaza2026agent"

# --- Instanciation des objets métier (une seule fois au démarrage) ---
db = Database(os.path.join(os.path.dirname(__file__), "yplaza.db"))
biens_repo = BienRepository(db)
users_repo = UserRepository(db)
favoris_repo = FavoriRepository(db)
messages_repo = MessageRepository(db)


def fichier_autorise(nom):
    """Vérifie l'extension contre la liste blanche."""
    return "." in nom and nom.rsplit(".", 1)[1].lower() in EXTENSIONS_OK


def sauver_image(fichier):
    """Enregistre l'image avec un nom ALEATOIRE (uuid) : empêche
    l'ecrasement de fichiers et neutralise les noms malveillants."""
    if not fichier or fichier.filename == "":
        return None
    if not fichier_autorise(fichier.filename):
        return None
    ext = fichier.filename.rsplit(".", 1)[1].lower()
    nom = f"{uuid.uuid4().hex}.{ext}"
    fichier.save(os.path.join(UPLOAD_DIR, nom))
    return f"/static/uploads/{nom}"


# ------------------------------------------------------------
# BAREMES DE MARCHE (references France, debut 2026)
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

estimateur = Estimateur(PRIX_M2, LOYER_M2)


# ------------------------------------------------------------
# Donnees de demonstration (photos Unsplash, libres de droits)
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
    """Cree les tables si besoin et insere les donnees de demonstration."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS biens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL, type TEXT NOT NULL, ville TEXT NOT NULL,
            prix REAL NOT NULL, surface REAL NOT NULL,
            pieces INTEGER NOT NULL DEFAULT 0,
            description TEXT, statut TEXT NOT NULL DEFAULT 'A vendre',
            image_url TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL, email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'client'
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS favoris (
            user_id INTEGER NOT NULL, bien_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, bien_id)
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bien_id INTEGER NOT NULL, expediteur_id INTEGER NOT NULL,
            contenu TEXT NOT NULL,
            date_envoi TEXT DEFAULT (datetime('now','localtime')),
            lu INTEGER NOT NULL DEFAULT 0
        )
    """)
    if db.query_one("SELECT COUNT(*) c FROM biens")["c"] == 0:
        db.execute_many(
            "INSERT INTO biens (titre,type,ville,prix,surface,pieces,description,statut,image_url)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            BIENS_DEMO,
        )
    # Compte agent de demonstration : agent@yplaza.fr / Demo2026!
    if users_repo.compter() == 0:
        agent = User("Agent Y-Plaza", "agent@yplaza.fr", role=User.ROLE_AGENT)
        agent.password = "Demo2026!"          # passe par le setter -> hachage
        users_repo.creer(agent)


# ------------------------------------------------------------
# Authentification
# ------------------------------------------------------------
def current_user():
    """Renvoie l'objet User connecte, ou None."""
    uid = session.get("user_id")
    return users_repo.par_id(uid) if uid else None


@app.context_processor
def inject_globals():
    u = current_user()
    non_lus = messages_repo.non_lus() if (u and u.est_agent()) else 0
    return {"user": u, "non_lus": non_lus}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Connectez-vous pour acceder a cette page.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def agent_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        if u is None or not u.est_agent():
            flash("Acces reserve aux agents Y-Plaza.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/inscription", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form.get("role", User.ROLE_CLIENT)
        code = request.form.get("code_agent", "").strip()

        if role == User.ROLE_AGENT and code != CODE_AGENT:
            flash("Code agence invalide. Le compte Agent necessite le code fourni par la direction.")
            return render_template("register.html")
        if users_repo.existe(request.form["email"]):
            flash("Un compte existe deja avec cet email.")
            return render_template("register.html")

        try:
            nouvel_user = User(request.form["nom"].strip(), request.form["email"], role=role)
            nouvel_user.password = request.form["password"]   # validation + hachage
        except ValueError as e:
            flash(str(e))
            return render_template("register.html")

        user_id = users_repo.creer(nouvel_user)
        session["user_id"] = user_id
        flash(f"Bienvenue {nouvel_user.nom} !")
        return redirect(url_for("landing"))
    return render_template("register.html")


@app.route("/connexion", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = users_repo.par_email(request.form["email"])
        if u is None or not u.verifier_mot_de_passe(request.form["password"]):
            flash("Email ou mot de passe incorrect.")
            return render_template("login.html")
        session["user_id"] = u.id
        flash(f"Ravi de vous revoir, {u.nom} !")
        return redirect(url_for("landing"))
    return render_template("login.html")


@app.route("/deconnexion")
def logout():
    session.clear()
    flash("Vous etes deconnecte.")
    return redirect(url_for("landing"))


# ------------------------------------------------------------
# Favoris
# ------------------------------------------------------------
def user_fav_ids():
    u = current_user()
    return favoris_repo.ids_pour(u.id) if u else set()


@app.route("/favori/<int:bien_id>", methods=["POST"])
@login_required
def toggle_favori(bien_id):
    favoris_repo.basculer(current_user().id, bien_id)
    return redirect(request.referrer or url_for("biens"))


@app.route("/mes-favoris")
@login_required
def favoris():
    return render_template("favoris.html",
                           biens=favoris_repo.biens_de(current_user().id),
                           favs=user_fav_ids())


# ------------------------------------------------------------
# Messagerie
# ------------------------------------------------------------
@app.route("/message/<int:bien_id>", methods=["POST"])
@login_required
def envoyer_message(bien_id):
    contenu = request.form.get("contenu", "").strip()
    if not contenu:
        flash("Le message est vide.")
        return redirect(url_for("detail", bien_id=bien_id))
    messages_repo.envoyer(bien_id, current_user().id, contenu)
    flash("Message envoye a l'agence.")
    return redirect(url_for("detail", bien_id=bien_id))


@app.route("/messagerie")
@agent_required
def messagerie():
    msgs = messages_repo.tous()
    messages_repo.marquer_lus()
    return render_template("messagerie.html", msgs=msgs)


# ------------------------------------------------------------
# Pages publiques
# ------------------------------------------------------------
@app.route("/")
def landing():
    return render_template("landing.html",
                           vedettes=biens_repo.vedettes(),
                           stats=biens_repo.statistiques(),
                           favs=user_fav_ids())


@app.route("/biens")
def biens():
    filtres = {
        "q": request.args.get("q", "").strip(),
        "ville": request.args.get("ville", ""),
        "type": request.args.get("type", ""),
        "statut": request.args.get("statut", ""),
        "prix_max": request.args.get("prix_max", ""),
    }
    return render_template("index.html",
                           biens=biens_repo.tous(filtres),
                           villes=biens_repo.villes(),
                           stats=biens_repo.statistiques(),
                           favs=user_fav_ids(),
                           q=filtres["q"], ville=filtres["ville"],
                           type_bien=filtres["type"], statut=filtres["statut"],
                           prix_max=filtres["prix_max"])


@app.route("/bien/<int:bien_id>")
def detail(bien_id):
    bien = biens_repo.par_id(bien_id)
    if bien is None:
        return redirect(url_for("biens"))
    return render_template("detail.html", bien=bien,
                           similaires=biens_repo.similaires(bien),
                           favs=user_fav_ids())


@app.route("/estimation", methods=["GET", "POST"])
def estimation():
    resultat = None
    if request.method == "POST":
        # On construit un vrai objet metier : la sous-classe est choisie
        # automatiquement, et son coefficient_marche() s'applique tout seul.
        bien = Bien.creer(
            request.form["type"],
            titre="Estimation", ville=request.form["ville"],
            prix=1, surface=float(request.form["surface"]),
        )
        resultat = estimateur.estimer(bien, request.form["etat"])
    return render_template("estimation.html", villes=estimateur.villes, resultat=resultat)


# ------------------------------------------------------------
# CRUD - agents uniquement
# ------------------------------------------------------------
def _bien_depuis_formulaire():
    """Construit un objet Bien (sous-classe adaptee) a partir du formulaire."""
    image = sauver_image(request.files.get("image_fichier"))
    if image is None:
        image = request.form.get("image_url", "").strip() or None
    return Bien.creer(
        request.form["type"],
        titre=request.form["titre"], ville=request.form["ville"],
        prix=request.form["prix"], surface=request.form["surface"],
        pieces=int(request.form.get("pieces") or 0),
        description=request.form["description"], statut=request.form["statut"],
        image_url=image,
    )


@app.route("/ajouter", methods=["GET", "POST"])
@agent_required
def ajouter():
    if request.method == "POST":
        try:
            biens_repo.ajouter(_bien_depuis_formulaire())
            flash("Bien publie.")
            return redirect(url_for("biens"))
        except ValueError as e:
            flash(str(e))
    return render_template("form.html", bien=None,
                           action="Publier le bien", titre_page="Nouveau bien")


@app.route("/modifier/<int:bien_id>", methods=["GET", "POST"])
@agent_required
def modifier(bien_id):
    if request.method == "POST":
        try:
            biens_repo.modifier(bien_id, _bien_depuis_formulaire())
            flash("Fiche mise a jour.")
            return redirect(url_for("detail", bien_id=bien_id))
        except ValueError as e:
            flash(str(e))
    return render_template("form.html", bien=biens_repo.par_id(bien_id),
                           action="Enregistrer", titre_page="Modifier le bien")


@app.route("/supprimer/<int:bien_id>", methods=["POST"])
@agent_required
def supprimer(bien_id):
    biens_repo.supprimer(bien_id)
    flash("Bien supprime.")
    return redirect(url_for("biens"))


# ------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",
                           par_ville=biens_repo.par_ville(),
                           par_type=biens_repo.par_type(),
                           par_statut=biens_repo.par_statut(),
                           stats=biens_repo.statistiques())


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
