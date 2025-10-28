from flask import Flask, render_template, request, jsonify
import json
import os
import glob

app = Flask(__name__)

# Chemin du fichier de données
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RED_TEAM_FILE = os.path.join(DATA_DIR, "red_team_names.json")
RED_AVATAR_FILE = os.path.join(DATA_DIR, "red_team_avatar.json")
BLUE_TEAM_FILE = os.path.join(DATA_DIR, "blue_team_names.json")
BLUE_AVATAR_FILE = os.path.join(DATA_DIR, "blue_team_avatar.json")


# Fonction pour supprimer tous les fichiers JSON au démarrage
def clear_all_json_files():
    """Supprime tous les fichiers JSON dans le dossier data au démarrage"""
    if os.path.exists(DATA_DIR):
        json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
        for json_file in json_files:
            try:
                os.remove(json_file)
                print(f"Fichier supprimé: {json_file}")
            except Exception as e:
                print(f"Erreur lors de la suppression de {json_file}: {e}")


@app.route("/")
def loading():
    # Supprimer tous les JSON au chargement de la page d'accueil
    clear_all_json_files()
    return render_template("loading.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/mode")
def mode():
    return render_template("mode.html")


@app.route("/sport")
def sport():
    return render_template("sport.html")


@app.route("/basketball")
def basketball():
    # Charger les données de l'équipe rouge si elles existent
    red_team_completed = False
    red_team_names = None
    red_avatar_id = None

    if os.path.exists(RED_TEAM_FILE) and os.path.exists(RED_AVATAR_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team_names = json.load(f)
            with open(RED_AVATAR_FILE, "r", encoding="utf-8") as f:
                red_avatar_data = json.load(f)
                red_avatar_id = red_avatar_data.get("avatar")
            red_team_completed = True
        except:
            pass

    # Charger les données de l'équipe bleue si elles existent
    blue_team_completed = False
    blue_team_names = None
    blue_avatar_id = None

    if os.path.exists(BLUE_TEAM_FILE) and os.path.exists(BLUE_AVATAR_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team_names = json.load(f)
            with open(BLUE_AVATAR_FILE, "r", encoding="utf-8") as f:
                blue_avatar_data = json.load(f)
                blue_avatar_id = blue_avatar_data.get("avatar")
            blue_team_completed = True
        except:
            pass

    return render_template(
        "basketball.html",
        red_team_completed=red_team_completed,
        red_team_names=red_team_names,
        red_avatar_id=red_avatar_id,
        blue_team_completed=blue_team_completed,
        blue_team_names=blue_team_names,
        blue_avatar_id=blue_avatar_id,
    )


@app.route("/nom_red_basketball")
def nom_red_basketball():
    return render_template("nom_red_basketball.html")


@app.route("/nom_blue_basketball")
def nom_blue_basketball():
    return render_template("nom_blue_basketball.html")


@app.route("/avatar_red_basketball")
def avatar_red_basketball():
    return render_template("avatar_red_basketball.html")


@app.route("/avatar_blue_basketball")
def avatar_blue_basketball():
    return render_template("avatar_blue_basketball.html")


@app.route("/save-red-team", methods=["POST"])
def save_red_team():
    """Sauvegarde les noms de l'équipe rouge dans un fichier JSON"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        red_team_data = request.get_json()

        # Sauvegarder dans le fichier JSON
        with open(RED_TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump(red_team_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Équipe rouge sauvegardée"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-red-avatar", methods=["POST"])
def save_red_avatar():
    """Sauvegarde l'avatar de l'équipe rouge dans un fichier JSON"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        avatar_data = request.get_json()

        # Sauvegarder dans le fichier JSON
        with open(RED_AVATAR_FILE, "w", encoding="utf-8") as f:
            json.dump(avatar_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Avatar équipe rouge sauvegardé"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-blue-team", methods=["POST"])
def save_blue_team():
    """Sauvegarde les noms de l'équipe bleue dans un fichier JSON"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        blue_team_data = request.get_json()

        # Sauvegarder dans le fichier JSON
        with open(BLUE_TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump(blue_team_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Équipe bleue sauvegardée"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-blue-avatar", methods=["POST"])
def save_blue_avatar():
    """Sauvegarde l'avatar de l'équipe bleue dans un fichier JSON"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        avatar_data = request.get_json()

        # Sauvegarder dans le fichier JSON
        with open(BLUE_AVATAR_FILE, "w", encoding="utf-8") as f:
            json.dump(avatar_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Avatar équipe bleue sauvegardé"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
