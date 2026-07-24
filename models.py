# ============================================================
# Y-PLAZA — Couche métier orientée objet (models.py)
#
# Ce module applique les principes de la POO :
#   - ENCAPSULATION : les attributs sensibles sont privés (_prefixe)
#     et exposés via des propriétés (@property) contrôlées
#   - HÉRITAGE      : Bien est une classe abstraite dont héritent
#     Appartement, Maison, LocalCommercial, Terrain
#   - POLYMORPHISME : chaque sous-classe redéfinit coefficient_marche()
#     et libelle() — le même appel produit un résultat adapté au type
#   - ABSTRACTION   : Database masque les détails SQL au reste du code
#   - SOLID / SRP   : une classe = une responsabilité
# ============================================================

from abc import ABC, abstractmethod
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


# ------------------------------------------------------------
# ABSTRACTION — accès aux données centralisé
# ------------------------------------------------------------
class Database:
    """Encapsule toutes les interactions SQLite.

    Le reste de l'application n'écrit jamais de sqlite3.connect() :
    si demain on passe à PostgreSQL, seule cette classe change.
    """

    def __init__(self, chemin):
        self._chemin = chemin  # privé : personne ne modifie le chemin en douce

    @property
    def chemin(self):
        """Lecture seule : le chemin de la base ne s'écrase pas de l'extérieur."""
        return self._chemin

    def _connexion(self):
        conn = sqlite3.connect(self._chemin)
        conn.row_factory = sqlite3.Row
        return conn

    def query(self, sql, params=()):
        """SELECT multiple → liste de lignes."""
        conn = self._connexion()
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return rows

    def query_one(self, sql, params=()):
        """SELECT unique → une ligne ou None."""
        conn = self._connexion()
        row = conn.execute(sql, params).fetchone()
        conn.close()
        return row

    def execute(self, sql, params=()):
        """INSERT / UPDATE / DELETE → id de la ligne insérée."""
        conn = self._connexion()
        cur = conn.execute(sql, params)
        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id

    def execute_many(self, sql, seq):
        conn = self._connexion()
        conn.executemany(sql, seq)
        conn.commit()
        conn.close()


# ------------------------------------------------------------
# HÉRITAGE — Bien est abstraite, chaque type de bien en hérite
# ------------------------------------------------------------
class Bien(ABC):
    """Classe abstraite représentant un bien immobilier.

    Impossible d'instancier Bien directement : on passe par
    Bien.creer() qui renvoie la bonne sous-classe (fabrique).
    """

    def __init__(self, titre, ville, prix, surface, pieces=0,
                 description="", statut="A vendre", image_url=None, id=None):
        self.id = id
        self.titre = titre
        self.ville = ville
        self._prix = 0          # attributs protégés : validés par les setters
        self._surface = 0
        self.prix = prix        # passe par le setter → validation
        self.surface = surface
        self.pieces = pieces
        self.description = description
        self.statut = statut
        self.image_url = image_url

    # --- ENCAPSULATION : prix et surface ne peuvent pas être négatifs ---
    @property
    def prix(self):
        return self._prix

    @prix.setter
    def prix(self, valeur):
        valeur = float(valeur)
        if valeur < 0:
            raise ValueError("Le prix ne peut pas être négatif.")
        self._prix = valeur

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, valeur):
        valeur = float(valeur)
        if valeur <= 0:
            raise ValueError("La surface doit être strictement positive.")
        self._surface = valeur

    # --- Comportement commun à tous les biens ---
    @property
    def prix_m2(self):
        return self._prix / self._surface

    def prix_formate(self):
        return f"{self._prix:,.0f} €".replace(",", " ")

    # --- POLYMORPHISME : redéfinis par chaque sous-classe ---
    @abstractmethod
    def coefficient_marche(self):
        """Coefficient appliqué au prix au m² de référence selon le type."""

    @abstractmethod
    def libelle(self):
        """Nom du type de bien, tel qu'affiché et stocké."""

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.titre} — {self.prix_formate()}>"

    # --- FABRIQUE : construit la bonne sous-classe à partir du type ---
    @staticmethod
    def creer(type_bien, **kwargs):
        classes = {
            "Appartement": Appartement,
            "Maison": Maison,
            "Local commercial": LocalCommercial,
            "Terrain": Terrain,
        }
        classe = classes.get(type_bien, Appartement)
        return classe(**kwargs)

    @staticmethod
    def depuis_ligne(row):
        """Reconstruit un objet métier à partir d'une ligne SQL."""
        return Bien.creer(
            row["type"],
            id=row["id"], titre=row["titre"], ville=row["ville"],
            prix=row["prix"], surface=row["surface"], pieces=row["pieces"],
            description=row["description"], statut=row["statut"],
            image_url=row["image_url"],
        )


class Appartement(Bien):
    def coefficient_marche(self):
        return 1.00

    def libelle(self):
        return "Appartement"


class Maison(Bien):
    def coefficient_marche(self):
        return 1.06          # une maison se valorise légèrement au-dessus

    def libelle(self):
        return "Maison"


class LocalCommercial(Bien):
    def coefficient_marche(self):
        return 0.85          # le professionnel se négocie sous le résidentiel

    def libelle(self):
        return "Local commercial"


class Terrain(Bien):
    def coefficient_marche(self):
        return 0.28          # terrain nu : forte décote au m²

    def libelle(self):
        return "Terrain"

    def prix_formate(self):
        # POLYMORPHISME : un terrain s'affiche avec sa surface parcellaire
        return f"{self._prix:,.0f} € ({self._surface:.0f} m² de terrain)".replace(",", " ")


# ------------------------------------------------------------
# ENCAPSULATION — le mot de passe n'est jamais accessible en clair
# ------------------------------------------------------------
class User:
    """Utilisateur de la plateforme (client ou agent)."""

    ROLE_CLIENT = "client"
    ROLE_AGENT = "agent"

    def __init__(self, nom, email, role=ROLE_CLIENT, password_hash=None, id=None):
        self.id = id
        self.nom = nom
        self.email = email.strip().lower()
        self.role = role if role in (self.ROLE_CLIENT, self.ROLE_AGENT) else self.ROLE_CLIENT
        self.__password_hash = password_hash   # double underscore = privé strict

    # --- Le mot de passe est en écriture seule : on ne peut jamais le relire ---
    @property
    def password(self):
        raise AttributeError("Le mot de passe ne peut pas être lu.")

    @password.setter
    def password(self, mot_de_passe):
        if len(mot_de_passe) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        self.__password_hash = generate_password_hash(mot_de_passe)

    @property
    def password_hash(self):
        return self.__password_hash

    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.__password_hash, mot_de_passe)

    def est_agent(self):
        return self.role == self.ROLE_AGENT

    def libelle_role(self):
        return "Agent" if self.est_agent() else "Client"

    @staticmethod
    def depuis_ligne(row):
        return User(
            id=row["id"], nom=row["nom"], email=row["email"],
            role=row["role"], password_hash=row["password_hash"],
        )

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


# ------------------------------------------------------------
# SRP — une classe dédiée au calcul d'estimation
# ------------------------------------------------------------
class Estimateur:
    """Estime la valeur d'un bien à partir d'un barème de marché.

    Le calcul est isolé ici : ni Flask ni SQL n'apparaissent,
    la classe est donc testable unitairement.
    """

    FRAIS_NOTAIRE_ANCIEN = 0.075
    COEF_ETAT = {"Neuf ou refait": 1.10, "Bon état": 1.00, "Travaux à prévoir": 0.83}

    def __init__(self, bareme_prix_m2, bareme_loyer_m2):
        self._prix_m2 = bareme_prix_m2
        self._loyer_m2 = bareme_loyer_m2

    @property
    def villes(self):
        return sorted(self._prix_m2.keys())

    def _coef_etat(self, etat):
        return self.COEF_ETAT.get(etat, 1.0)

    def estimer(self, bien, etat="Bon état"):
        """Prend un objet Bien (polymorphe) et renvoie l'estimation complète."""
        base = self._prix_m2.get(bien.ville, 3000)
        loyer_ref = self._loyer_m2.get(bien.ville, 12.0)
        coef = bien.coefficient_marche() * self._coef_etat(etat)

        valeur = base * bien.surface * coef
        loyer = 0 if isinstance(bien, Terrain) else loyer_ref * bien.surface * self._coef_etat(etat)

        return {
            "ville": bien.ville,
            "type": bien.libelle(),
            "surface": bien.surface,
            "etat": etat,
            "prix_m2_ref": base,
            "vente_basse": valeur * 0.93,
            "vente": valeur,
            "vente_haute": valeur * 1.07,
            "notaire": valeur * self.FRAIS_NOTAIRE_ANCIEN,
            "budget_achat": valeur * (1 + self.FRAIS_NOTAIRE_ANCIEN),
            "loyer": loyer,
            "rendement": (loyer * 12 / valeur * 100) if valeur and loyer else 0,
        }


# ------------------------------------------------------------
# SRP — dépôts (repositories) : ils parlent à la base, rien d'autre
# ------------------------------------------------------------
class BienRepository:
    """Toutes les requêtes concernant les biens sont regroupées ici."""

    def __init__(self, db: Database):
        self.db = db

    def tous(self, filtres=None):
        sql = "SELECT * FROM biens WHERE 1=1"
        params = []
        f = filtres or {}
        if f.get("q"):
            sql += " AND (titre LIKE ? OR description LIKE ? OR ville LIKE ?)"
            like = f"%{f['q']}%"
            params += [like, like, like]
        if f.get("ville"):
            sql += " AND ville = ?"; params.append(f["ville"])
        if f.get("type"):
            sql += " AND type = ?"; params.append(f["type"])
        if f.get("statut"):
            sql += " AND statut = ?"; params.append(f["statut"])
        if f.get("prix_max"):
            sql += " AND prix <= ?"; params.append(float(f["prix_max"]))
        sql += " ORDER BY id DESC"
        return self.db.query(sql, params)

    def par_id(self, bien_id):
        return self.db.query_one("SELECT * FROM biens WHERE id=?", (bien_id,))

    def objet_par_id(self, bien_id):
        """Renvoie un vrai objet métier (Maison, Appartement…)."""
        row = self.par_id(bien_id)
        return Bien.depuis_ligne(row) if row else None

    def similaires(self, bien_row, limite=3):
        return self.db.query(
            "SELECT * FROM biens WHERE id != ? AND (ville=? OR type=?) ORDER BY RANDOM() LIMIT ?",
            (bien_row["id"], bien_row["ville"], bien_row["type"], limite),
        )

    def ajouter(self, bien: Bien):
        return self.db.execute(
            "INSERT INTO biens (titre,type,ville,prix,surface,pieces,description,statut,image_url)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (bien.titre, bien.libelle(), bien.ville, bien.prix, bien.surface,
             bien.pieces, bien.description, bien.statut, bien.image_url),
        )

    def modifier(self, bien_id, bien: Bien):
        self.db.execute(
            "UPDATE biens SET titre=?,type=?,ville=?,prix=?,surface=?,pieces=?,"
            "description=?,statut=?,image_url=? WHERE id=?",
            (bien.titre, bien.libelle(), bien.ville, bien.prix, bien.surface,
             bien.pieces, bien.description, bien.statut, bien.image_url, bien_id),
        )

    def supprimer(self, bien_id):
        self.db.execute("DELETE FROM biens WHERE id=?", (bien_id,))
        self.db.execute("DELETE FROM favoris WHERE bien_id=?", (bien_id,))

    def villes(self):
        return [r["ville"] for r in self.db.query("SELECT DISTINCT ville FROM biens ORDER BY ville")]

    def statistiques(self):
        return self.db.query_one("""
            SELECT COUNT(*) total,
                   SUM(CASE WHEN statut='A vendre' THEN 1 ELSE 0 END) en_vente,
                   AVG(prix) prix_moyen, MIN(prix) prix_min, MAX(prix) prix_max,
                   AVG(prix/surface) prix_m2
            FROM biens
        """)

    def vedettes(self, limite=3):
        return self.db.query(
            "SELECT * FROM biens WHERE statut='A vendre' ORDER BY prix DESC LIMIT ?", (limite,)
        )

    def par_ville(self):
        return self.db.query("""
            SELECT ville, COUNT(*) nb, AVG(prix) prix_moyen, AVG(prix/surface) prix_m2
            FROM biens GROUP BY ville ORDER BY prix_m2 DESC
        """)

    def par_type(self):
        return self.db.query("SELECT type, COUNT(*) nb FROM biens GROUP BY type ORDER BY nb DESC")

    def par_statut(self):
        return self.db.query("SELECT statut, COUNT(*) nb FROM biens GROUP BY statut")


class UserRepository:
    """Toutes les requêtes concernant les utilisateurs."""

    def __init__(self, db: Database):
        self.db = db

    def par_id(self, user_id):
        row = self.db.query_one("SELECT * FROM users WHERE id=?", (user_id,))
        return User.depuis_ligne(row) if row else None

    def par_email(self, email):
        row = self.db.query_one("SELECT * FROM users WHERE email=?", (email.strip().lower(),))
        return User.depuis_ligne(row) if row else None

    def existe(self, email):
        return self.par_email(email) is not None

    def creer(self, user: User):
        return self.db.execute(
            "INSERT INTO users (nom,email,password_hash,role) VALUES (?,?,?,?)",
            (user.nom, user.email, user.password_hash, user.role),
        )

    def compter(self):
        return self.db.query_one("SELECT COUNT(*) c FROM users")["c"]


class FavoriRepository:
    def __init__(self, db: Database):
        self.db = db

    def ids_pour(self, user_id):
        rows = self.db.query("SELECT bien_id FROM favoris WHERE user_id=?", (user_id,))
        return {r["bien_id"] for r in rows}

    def basculer(self, user_id, bien_id):
        existe = self.db.query_one(
            "SELECT 1 FROM favoris WHERE user_id=? AND bien_id=?", (user_id, bien_id))
        if existe:
            self.db.execute("DELETE FROM favoris WHERE user_id=? AND bien_id=?", (user_id, bien_id))
        else:
            self.db.execute("INSERT INTO favoris (user_id,bien_id) VALUES (?,?)", (user_id, bien_id))

    def biens_de(self, user_id):
        return self.db.query("""
            SELECT b.* FROM biens b JOIN favoris f ON f.bien_id=b.id
            WHERE f.user_id=? ORDER BY b.id DESC
        """, (user_id,))


class MessageRepository:
    def __init__(self, db: Database):
        self.db = db

    def envoyer(self, bien_id, expediteur_id, contenu):
        self.db.execute(
            "INSERT INTO messages (bien_id, expediteur_id, contenu) VALUES (?,?,?)",
            (bien_id, expediteur_id, contenu),
        )

    def tous(self):
        return self.db.query("""
            SELECT m.*, u.nom AS expediteur, u.email, b.titre AS bien_titre, b.id AS bid
            FROM messages m
            JOIN users u ON u.id = m.expediteur_id
            JOIN biens b ON b.id = m.bien_id
            ORDER BY m.id DESC
        """)

    def marquer_lus(self):
        self.db.execute("UPDATE messages SET lu = 1")

    def non_lus(self):
        return self.db.query_one("SELECT COUNT(*) c FROM messages WHERE lu = 0")["c"]
