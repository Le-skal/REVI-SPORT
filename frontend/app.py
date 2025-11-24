from flask import Flask, render_template, request, jsonify
import json
import os
import glob
import random

app = Flask(__name__)

# Chemin du fichier de données
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")
RED_TEAM_FILE = os.path.join(DATA_DIR, "red_team_info.json")
BLUE_TEAM_FILE = os.path.join(DATA_DIR, "blue_team_info.json")
GAME_SETUP_FILE = os.path.join(DATA_DIR, "game_setup.json")
QUESTIONS_KNOWLEDGE_FILE = os.path.join(CONTENT_DIR, "questions-knowledge.json")
QUESTIONS_COUNTING_FILE = os.path.join(CONTENT_DIR, "questions-counting.json")
QUESTIONS_LINK_FILE = os.path.join(CONTENT_DIR, "questions-link.json")
QUESTIONS_MATH_FILE = os.path.join(CONTENT_DIR, "questions-math.json")
QUESTIONS_ORDER_PHRASE_FILE = os.path.join(CONTENT_DIR, "questions-orderPhrase.json")
QUESTIONS_ORDER_SYLLABES_FILE = os.path.join(
    CONTENT_DIR, "questions-orderSyllabes.json"
)


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

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team_data = json.load(f)
                red_team_names = {
                    "team_name": red_team_data.get("team_name"),
                    "joueur_1": red_team_data.get("joueur_1"),
                    "joueur_2": red_team_data.get("joueur_2"),
                    "joueur_3": red_team_data.get("joueur_3"),
                    "joueur_4": red_team_data.get("joueur_4"),
                    "joueur_5": red_team_data.get("joueur_5"),
                }
                red_avatar_id = red_team_data.get("avatar")
            red_team_completed = True
        except:
            pass

    # Charger les données de l'équipe bleue si elles existent
    blue_team_completed = False
    blue_team_names = None
    blue_avatar_id = None

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team_data = json.load(f)
                blue_team_names = {
                    "team_name": blue_team_data.get("team_name"),
                    "joueur_1": blue_team_data.get("joueur_1"),
                    "joueur_2": blue_team_data.get("joueur_2"),
                    "joueur_3": blue_team_data.get("joueur_3"),
                    "joueur_4": blue_team_data.get("joueur_4"),
                    "joueur_5": blue_team_data.get("joueur_5"),
                }
                blue_avatar_id = blue_team_data.get("avatar")
            blue_team_completed = True
        except:
            pass

    # Charger le niveau depuis game_setup.json
    level = None
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                level = game_setup.get("level")
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
        level=level,
    )


@app.route("/nom_red_basketball")
def nom_red_basketball():
    return render_template("nom_red_basketball.html")


@app.route("/nom_blue_basketball")
def nom_blue_basketball():
    return render_template("nom_blue_basketball.html")


@app.route("/avatar_red_basketball")
def avatar_red_basketball():
    red_team_name = None
    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team_data = json.load(f)
                red_team_name = red_team_data.get("team_name")
        except:
            pass
    return render_template("avatar_red_basketball.html", red_team_name=red_team_name)


@app.route("/avatar_blue_basketball")
def avatar_blue_basketball():
    blue_team_name = None
    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team_data = json.load(f)
                blue_team_name = blue_team_data.get("team_name")
        except:
            pass
    return render_template("avatar_blue_basketball.html", blue_team_name=blue_team_name)


@app.route("/countdown")
def countdown():
    return render_template("countdown.html")


@app.route("/question-selection")
def question_selection():
    return render_template("question-selection.html")


@app.route("/theme-selection")
def theme_selection():
    return render_template("theme-selection.html")


@app.route("/joker-selection")
def joker_selection():
    return render_template("joker-selection.html")


@app.route("/level-selection")
def level_selection():
    return render_template("level-selection.html")


@app.route("/configuration-timings")
def configuration_timings():
    # Load sport from game_setup.json
    sport = None
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
        except:
            sport = "basketball"

    return render_template("configuration-timings.html", sport=sport)


@app.route("/recapitulatif")
def recapitulatif():
    return render_template("recapitulatif.html")


@app.route("/game-intro")
def game_intro():
    return render_template("game-intro.html")


@app.route("/game-knowledge")
def game_knowledge():
    # Get level from query parameter (default: 1)
    level = request.args.get("level", 1, type=int)
    if level < 1 or level > 5:
        level = 1

    # Get question index from query parameter (default: 0 for first question)
    question_index = request.args.get("question", 0, type=int)

    # Determine number of options based on level
    num_options = level + 1  # level 1: 2, level 2: 3, ..., level 5: 6

    # Load red and blue team data
    red_avatar = None
    blue_avatar = None

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            red_avatar = "1"

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            blue_avatar = "1"

    # Load question data
    with open(QUESTIONS_KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
        # Use the question_index parameter, fallback to 0
        if question_index < len(questions_data["questions"]):
            question = questions_data["questions"][question_index]
        else:
            question = questions_data["questions"][0]

    # Get all available options
    all_options = question.get("options", [])
    correct_answer_index = question.get("correctAnswer", 0)
    correct_answer = (
        all_options[correct_answer_index]
        if correct_answer_index < len(all_options)
        else all_options[0]
    )

    # Generate options based on level
    if len(all_options) > num_options:
        # Get all options except the correct one
        other_options = [
            opt for i, opt in enumerate(all_options) if i != correct_answer_index
        ]
        # Randomly select additional options
        selected_other_options = random.sample(other_options, num_options - 1)
        # Create final options list with correct answer
        final_options = selected_other_options + [correct_answer]
    else:
        # If not enough options, use all available
        final_options = all_options.copy()

    # Always shuffle the options to randomize order
    random.shuffle(final_options)

    # Find the index of correct answer in the shuffled list
    correct_answer_index = final_options.index(correct_answer)

    return render_template(
        "game-knowledge.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=0,
        blue_score=0,
        question_image=question.get("image"),
        question_text=question.get("question"),
        options=final_options,
        correctAnswer=correct_answer_index,
        level=level,
    )


@app.route("/game-counting")
def game_counting():
    # Get level from query parameter (default: 1)
    level = request.args.get("level", 1, type=int)
    if level < 1 or level > 5:
        level = 1

    # Get question index from query parameter (default: 0 for first question)
    question_index = request.args.get("question", 0, type=int)

    # Determine number of options based on level
    num_options = level + 1  # level 1: 2, level 2: 3, ..., level 5: 6

    # Load red and blue team data
    red_avatar = None
    blue_avatar = None

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            red_avatar = "1"

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            blue_avatar = "1"

    # Load question data
    with open(QUESTIONS_COUNTING_FILE, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
        # Use the question_index parameter, fallback to 0
        if question_index < len(questions_data["questions"]):
            question = questions_data["questions"][question_index]
        else:
            question = questions_data["questions"][0]

    # Get all available options
    all_options = question.get("options", [])
    correct_answer_index = question.get("correctAnswer", 0)
    correct_answer = (
        all_options[correct_answer_index]
        if correct_answer_index < len(all_options)
        else all_options[0]
    )

    # Generate options based on level
    if len(all_options) > num_options:
        # Get all options except the correct one
        other_options = [
            opt for i, opt in enumerate(all_options) if i != correct_answer_index
        ]
        # Randomly select additional options
        selected_other_options = random.sample(other_options, num_options - 1)
        # Create final options list with correct answer
        final_options = selected_other_options + [correct_answer]
    else:
        # If not enough options, use all available
        final_options = all_options.copy()

    # Always shuffle the options to randomize order
    random.shuffle(final_options)

    # Find the index of correct answer in the shuffled list
    correct_answer_index = final_options.index(correct_answer)

    return render_template(
        "game-counting.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=0,
        blue_score=0,
        question_image=question.get("image"),
        question_text=question.get("question"),
        options=final_options,
        correctAnswer=correct_answer_index,
        level=level,
    )


@app.route("/game-link")
def game_link():
    """Page de jeu de connexion (relier les éléments)"""
    # Get question index from query parameter (default: 0 for first question)
    question_index = request.args.get("question", 0, type=int)

    # Load red and blue team data
    red_avatar = None
    blue_avatar = None

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            red_avatar = "1"

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            blue_avatar = "1"

    # Load question data
    with open(QUESTIONS_LINK_FILE, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
        # Use the question_index parameter, fallback to 0
        if question_index < len(questions_data["questions"]):
            question = questions_data["questions"][question_index]
        else:
            question = questions_data["questions"][0]

    # Shuffle left and right items separately
    left_items = question.get("left_items", []).copy()
    right_items = question.get("right_items", []).copy()

    random.shuffle(left_items)
    random.shuffle(right_items)

    return render_template(
        "game-link.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=0,
        blue_score=0,
        question_text=question.get("question_text"),
        left_items=left_items,
        right_items=right_items,
        correct_pairs=question.get("correct_pairs", []),
    )


@app.route("/game-math")
def game_math():
    """Page de jeu de mathématiques"""
    # Get question index from query parameter (default: 0 for first question)
    question_index = request.args.get("question", 0, type=int)

    # Load red and blue team data
    red_avatar = None
    blue_avatar = None

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            red_avatar = "1"

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            blue_avatar = "1"

    # Load question data
    with open(QUESTIONS_MATH_FILE, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
        # Use the question_index parameter, fallback to 0
        if question_index < len(questions_data["questions"]):
            question = questions_data["questions"][question_index]
        else:
            question = questions_data["questions"][0]

    # Get all available options
    all_options = question.get("options", [])
    correct_answer_index = question.get("correctAnswer", 0)

    # Shuffle the options
    final_options = all_options.copy()
    random.shuffle(final_options)

    # Find the index of correct answer in the shuffled list
    correct_answer_index = final_options.index(all_options[correct_answer_index])

    return render_template(
        "game-math.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=0,
        blue_score=0,
        question_text=question.get("question"),
        options=final_options,
        correctAnswer=correct_answer_index,
    )


@app.route("/game-orderPhrase")
def game_orderPhrase():
    """Page de jeu d'ordre (reconstituer la phrase)"""
    # Get question index from query parameter (default: 0 for first question)
    question_index = request.args.get("question", 0, type=int)

    # Load red and blue team data
    red_avatar = None
    blue_avatar = None

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            red_avatar = "1"

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            blue_avatar = "1"

    # Load question data
    with open(QUESTIONS_ORDER_PHRASE_FILE, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
        # Use the question_index parameter, fallback to 0
        if question_index < len(questions_data["questions"]):
            question = questions_data["questions"][question_index]
        else:
            question = questions_data["questions"][0]

    # Get items and correct order
    items = question.get("items", [])
    correct_order = question.get("correctOrder", [])

    # Shuffle the items
    shuffled_indices = list(range(len(items)))
    random.shuffle(shuffled_indices)

    shuffled_items = [items[i] for i in shuffled_indices]

    # Recalculate correct order based on shuffled positions
    new_correct_order = []
    for correct_idx in correct_order:
        new_correct_order.append(shuffled_indices.index(correct_idx))

    return render_template(
        "game-orderPhrase.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=0,
        blue_score=0,
        question_text=question.get("question"),
        question_subtitle=question.get("subtitle"),
        phrase_label=question.get("phraseLabel", "Phrase à traduire en anglais"),
        items=items,
        shuffled_items=shuffled_items,
        correct_order=new_correct_order,
    )


@app.route("/game-orderSyllabes")
def game_orderSyllabes():
    """Page de jeu d'ordre des syllabes"""
    # Get question index from query parameter (default: 0 for first question)
    question_index = request.args.get("question", 0, type=int)

    # Load red and blue team data
    red_avatar = None
    blue_avatar = None

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            red_avatar = "1"

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            blue_avatar = "1"

    # Load question data
    with open(QUESTIONS_ORDER_SYLLABES_FILE, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
        # Use the question_index parameter, fallback to 0
        if question_index < len(questions_data["questions"]):
            question = questions_data["questions"][question_index]
        else:
            question = questions_data["questions"][0]

    # Get items and correct order
    items = question.get("items", [])
    correct_order = question.get("correctOrder", [])

    # Shuffle the items
    shuffled_indices = list(range(len(items)))
    random.shuffle(shuffled_indices)

    shuffled_items = [items[i] for i in shuffled_indices]

    # Recalculate correct order based on shuffled positions
    new_correct_order = []
    for correct_idx in correct_order:
        new_correct_order.append(shuffled_indices.index(correct_idx))

    return render_template(
        "game-orderSyllabes.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=0,
        blue_score=0,
        question_text=question.get("question"),
        question_image=question.get("image"),
        items=items,
        shuffled_items=shuffled_items,
        correct_order=new_correct_order,
    )


@app.route("/save-red-team", methods=["POST"])
def save_red_team():
    """Sauvegarde les noms de l'équipe rouge dans un fichier JSON"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        red_team_data = request.get_json()

        # Charger les données existantes s'il y en a
        existing_data = {}
        if os.path.exists(RED_TEAM_FILE):
            try:
                with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except:
                pass

        # Fusionner avec les nouvelles données
        existing_data.update(red_team_data)

        # Sauvegarder dans le fichier JSON
        with open(RED_TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Équipe rouge sauvegardée"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/get-game-setup")
def get_game_setup():
    """Récupère la configuration du jeu"""
    try:
        if os.path.exists(GAME_SETUP_FILE):
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                return jsonify(game_setup)
        else:
            return jsonify({}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-red-team")
def get_red_team():
    """Récupère les données de l'équipe rouge"""
    try:
        if os.path.exists(RED_TEAM_FILE):
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team = json.load(f)
                return jsonify(red_team)
        else:
            return jsonify({}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-blue-team")
def get_blue_team():
    """Récupère les données de l'équipe bleue"""
    try:
        if os.path.exists(BLUE_TEAM_FILE):
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team = json.load(f)
                return jsonify(blue_team)
        else:
            return jsonify({}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/save-red-avatar", methods=["POST"])
def save_red_avatar():
    """Sauvegarde l'avatar de l'équipe rouge dans le fichier JSON consolidé"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        avatar_data = request.get_json()

        # Charger les données existantes s'il y en a
        existing_data = {}
        if os.path.exists(RED_TEAM_FILE):
            try:
                with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except:
                pass

        # Fusionner avec les nouvelles données
        existing_data.update(avatar_data)

        # Sauvegarder dans le fichier JSON
        with open(RED_TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Avatar équipe rouge sauvegardé"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-blue-team", methods=["POST"])
def save_blue_team():
    """Sauvegarde les noms de l'équipe bleue dans le fichier JSON consolidé"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        blue_team_data = request.get_json()

        # Charger les données existantes s'il y en a
        existing_data = {}
        if os.path.exists(BLUE_TEAM_FILE):
            try:
                with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except:
                pass

        # Fusionner avec les nouvelles données
        existing_data.update(blue_team_data)

        # Sauvegarder dans le fichier JSON
        with open(BLUE_TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Équipe bleue sauvegardée"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-blue-avatar", methods=["POST"])
def save_blue_avatar():
    """Sauvegarde l'avatar de l'équipe bleue dans le fichier JSON consolidé"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        avatar_data = request.get_json()

        # Charger les données existantes s'il y en a
        existing_data = {}
        if os.path.exists(BLUE_TEAM_FILE):
            try:
                with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except:
                pass

        # Fusionner avec les nouvelles données
        existing_data.update(avatar_data)

        # Sauvegarder dans le fichier JSON
        with open(BLUE_TEAM_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Avatar équipe bleue sauvegardé"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-game-setup", methods=["POST"])
def save_game_setup():
    """Sauvegarde la configuration du jeu (thème et joker sélectionnés)"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)

        # Récupérer les données JSON du corps de la requête
        game_setup_data = request.get_json()

        # Charger les données existantes s'il y en a
        existing_data = {}
        if os.path.exists(GAME_SETUP_FILE):
            try:
                with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except:
                pass

        # Fusionner avec les nouvelles données
        existing_data.update(game_setup_data)

        # Sauvegarder dans le fichier JSON
        with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Configuration du jeu sauvegardée"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
