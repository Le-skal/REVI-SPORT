from flask import Flask, render_template, request, jsonify
from urllib.parse import quote
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


def get_answer_time():
    """Load answerTime from game_setup.json, default to 30"""
    try:
        if os.path.exists(GAME_SETUP_FILE):
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                return game_setup.get("answerTime", 30)
    except:
        pass
    return 30


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


@app.route("/parcours")
def parcours():
    return render_template("parcours.html")


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

    # Charger le niveau, sport et mode depuis game_setup.json
    level = None
    sport = "basketball"
    mode = "sport-collectif"
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                level = game_setup.get("level")
                sport = game_setup.get("sport", "basketball")
                mode = game_setup.get("mode", "sport-collectif")
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
        sport=sport,
        mode=mode,
    )


@app.route("/game-management")
def game_management():
    # Load red team data
    red_team_name = "Rouge"
    red_avatar_id = "1"
    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team_data = json.load(f)
                red_team_name = red_team_data.get("team_name", "Rouge")
                red_avatar_id = red_team_data.get("avatar", "1")
        except:
            pass

    # Load blue team data
    blue_team_name = "Bleue"
    blue_avatar_id = "2"
    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team_data = json.load(f)
                blue_team_name = blue_team_data.get("team_name", "Bleue")
                blue_avatar_id = blue_team_data.get("avatar", "2")
        except:
            pass

    # Load game setup for time and sport
    game_time_minutes = 32
    sport = "basketball"
    mode = None
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                game_time_minutes = game_setup.get("gameTime", 32)
                sport = game_setup.get("sport", "basketball")
                mode = game_setup.get("mode")
        except:
            pass

    # Load game management data
    game_management_file = os.path.join(DATA_DIR, "game-management.json")
    red_score = 0
    blue_score = 0
    events = []
    if os.path.exists(game_management_file):
        try:
            with open(game_management_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
                red_score = game_data.get("red_score", 0)
                blue_score = game_data.get("blue_score", 0)
                events = game_data.get("events", [])
        except:
            pass

    game_time = f"{game_time_minutes:02d} : 00"

    return render_template(
        "game-management.html",
        red_team_name=red_team_name,
        red_avatar_id=red_avatar_id,
        blue_team_name=blue_team_name,
        blue_avatar_id=blue_avatar_id,
        red_score=red_score,
        blue_score=blue_score,
        game_time=game_time,
        game_time_minutes=game_time_minutes,
        events=events,
        sport=sport,
        mode=mode,
    )


@app.route("/nom_red_basketball")
def nom_red_basketball():
    sport = "basketball"
    mode = None
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                mode = game_setup.get("mode")
        except:
            pass
    return render_template("nom_red_basketball.html", sport=sport, mode=mode)


@app.route("/nom_blue_basketball")
def nom_blue_basketball():
    sport = "basketball"
    mode = None
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                mode = game_setup.get("mode")
        except:
            pass
    return render_template("nom_blue_basketball.html", sport=sport, mode=mode)


@app.route("/avatar_red_basketball")
def avatar_red_basketball():
    red_team_name = None
    sport = "basketball"
    mode = None
    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team_data = json.load(f)
                red_team_name = red_team_data.get("team_name")
        except:
            pass
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                mode = game_setup.get("mode")
        except:
            pass
    return render_template(
        "avatar_red_basketball.html",
        red_team_name=red_team_name,
        sport=sport,
        mode=mode,
    )


@app.route("/avatar_blue_basketball")
def avatar_blue_basketball():
    blue_team_name = None
    sport = "basketball"
    mode = None
    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team_data = json.load(f)
                blue_team_name = blue_team_data.get("team_name")
        except:
            pass
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                mode = game_setup.get("mode")
        except:
            pass
    return render_template(
        "avatar_blue_basketball.html",
        blue_team_name=blue_team_name,
        sport=sport,
        mode=mode,
    )


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
    # Load game mode
    mode = "sport-collectif"
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                mode = game_setup.get("mode", "sport-collectif")
        except:
            pass
    return render_template("joker-selection.html", mode=mode)


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
    sport = "basketball"
    parcours = None
    mode = None
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                parcours = game_setup.get("parcours")
                mode = game_setup.get("mode")
        except:
            pass
    return render_template(
        "recapitulatif.html", sport=sport, parcours=parcours, mode=mode
    )


@app.route("/game-end")
def game_end():
    """Route pour la page de fin de match avec statistiques détaillées"""

    # Charger game-management.json pour les scores et events
    game_management_file = os.path.join(DATA_DIR, "game-management.json")
    game_data = {"red_score": 0, "blue_score": 0, "events": []}
    if os.path.exists(game_management_file):
        try:
            with open(game_management_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
        except:
            pass

    # Charger game_setup.json pour les infos du jeu
    game_setup = {}
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
        except:
            pass

    # Charger les infos des équipes
    red_team_name = "Équipe rouge"
    red_avatar = "1"
    red_players = []
    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_team_name = red_data.get("team_name", "Équipe rouge")
                red_avatar = red_data.get("avatar", "1")
                for i in range(1, 11):
                    p = red_data.get(f"joueur_{i}")
                    if p:
                        red_players.append(p)
        except:
            pass

    blue_team_name = "Équipe bleue"
    blue_avatar = "2"
    blue_players = []
    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_team_name = blue_data.get("team_name", "Équipe bleue")
                blue_avatar = blue_data.get("avatar", "2")
                for i in range(1, 11):
                    p = blue_data.get(f"joueur_{i}")
                    if p:
                        blue_players.append(p)
        except:
            pass

    # Calculer les scores finaux
    red_score = game_data.get("red_score", 0)
    blue_score = game_data.get("blue_score", 0)
    winner = (
        "red" if red_score > blue_score else "blue" if blue_score > red_score else "tie"
    )

    # Analyser les events pour extraire les statistiques
    events = game_data.get("events", [])

    # Stats par joueur
    player_stats = {}
    questions_list = []
    penalties_list = []
    jokers_red = []
    jokers_blue = []

    for event in events:
        team = event.get("team", "")
        player = event.get("player", "Joueur")
        action = event.get("action", "")
        result = event.get("result", "")
        result_class = event.get("result_class", "")

        # Initialiser les stats du joueur si nécessaire
        if player and team in ["red", "blue"]:
            key = f"{team}_{player}"
            if key not in player_stats:
                player_stats[key] = {
                    "team": team,
                    "player": player,
                    "points_scored": 0,
                    "duels_won": 0,
                    "duels_total": 0,
                    "jokers_used": 0,
                }

            # Comptabiliser les questions (duels)
            if "Question" in action and result_class in ["correct", "incorrect"]:
                player_stats[key]["duels_total"] += 1

                if result_class == "correct":
                    try:
                        pts = int(result.replace("+", "").replace(" pts", "").strip())
                        player_stats[key]["points_scored"] += pts
                        player_stats[key]["duels_won"] += 1
                    except:
                        player_stats[key]["duels_won"] += 1

                # Ajouter à la liste des questions
                questions_list.append(
                    {
                        "theme": action.replace("Question ", "").replace(
                            "Bonus", "Bonus"
                        ),
                        "question": action,
                        "answer": "Correcte",
                        "team": team,
                        "player": player,
                        "points": result.replace("+", "").replace(" pts", "").strip(),
                    }
                )

            # Comptabiliser les jokers
            if result_class == "joker":
                player_stats[key]["jokers_used"] += 1
                joker_data = {"icon": "🃏", "player": player, "joker": action}
                if team == "red":
                    jokers_red.append(joker_data)
                else:
                    jokers_blue.append(joker_data)

            # Comptabiliser les pénalités
            if result_class == "penalty":
                penalties_list.append(
                    {"team": team, "player": player, "reason": action, "icon": "⚠️"}
                )

    # Trouver le MVP de chaque équipe (celui avec le plus de points)
    red_mvp = {
        "player": red_players[0] if red_players else "Joueur",
        "avatar": red_avatar,
        "stats": {
            "points_scored": 0,
            "duels_won": 0,
            "duels_total": 0,
            "jokers_used": 0,
        },
    }
    blue_mvp = {
        "player": blue_players[0] if blue_players else "Joueur",
        "avatar": blue_avatar,
        "stats": {
            "points_scored": 0,
            "duels_won": 0,
            "duels_total": 0,
            "jokers_used": 0,
        },
    }

    for key, stats in player_stats.items():
        if (
            stats["team"] == "red"
            and stats["points_scored"] > red_mvp["stats"]["points_scored"]
        ):
            red_mvp = {
                "player": stats["player"],
                "avatar": red_avatar,
                "stats": {
                    "points_scored": stats["points_scored"],
                    "duels_won": stats["duels_won"],
                    "duels_total": stats["duels_total"],
                    "jokers_used": stats["jokers_used"],
                },
            }
        elif (
            stats["team"] == "blue"
            and stats["points_scored"] > blue_mvp["stats"]["points_scored"]
        ):
            blue_mvp = {
                "player": stats["player"],
                "avatar": blue_avatar,
                "stats": {
                    "points_scored": stats["points_scored"],
                    "duels_won": stats["duels_won"],
                    "duels_total": stats["duels_total"],
                    "jokers_used": stats["jokers_used"],
                },
            }

    # Construire les rounds/duels à partir des events de questions
    duels_list = []
    question_events = [
        e for e in events
        if "Question" in e.get("action", "") and e.get("result_class") in ["correct", "incorrect"]
    ]

    # Grouper par paires (rouge puis bleu)
    red_event = None
    for event in question_events:
        if event.get("team") == "red":
            red_event = event
        elif event.get("team") == "blue" and red_event:
            # On a une paire rouge/bleu
            red_correct = red_event.get("result_class") == "correct"
            blue_correct = event.get("result_class") == "correct"

            if red_correct and blue_correct:
                result = "tie"
                result_text = "Égalité"
            elif not red_correct and not blue_correct:
                result = "tie"
                result_text = "Égalité"
            elif red_correct:
                result = "red"
                result_text = f"Victoire {red_event.get('player', 'Rouge')}"
            else:
                result = "blue"
                result_text = f"Victoire {event.get('player', 'Bleu')}"

            duels_list.append({
                "red_player": red_event.get("player", "Joueur"),
                "blue_player": event.get("player", "Joueur"),
                "red_correct": red_correct,
                "blue_correct": blue_correct,
                "winner": result,
                "result_text": result_text,
            })
            red_event = None

    # Construire les données finales
    data = {
        "final_score": {
            "red_team": red_score,
            "blue_team": blue_score,
            "winner": winner,
        },
        "teams": {
            "red": {
                "name": red_team_name,
                "avatar": red_avatar,
                "players": red_players,
            },
            "blue": {
                "name": blue_team_name,
                "avatar": blue_avatar,
                "players": blue_players,
            },
        },
        "mvp": {
            "red": red_mvp,
            "blue": blue_mvp,
        },
        "duels": duels_list,
        "questions": questions_list,
        "penalties": penalties_list,
        "jokers": {"red": jokers_red, "blue": jokers_blue},
        "game_info": {
            "mode": game_setup.get("mode", "sport-collectif"),
            "sport": game_setup.get("sport", "basketball"),
            "level": game_setup.get("level", "Cycle 4"),
            "duration": "00:00",
            "themes": game_setup.get("themes", []),
        },
    }

    return render_template("game-end.html", data=data)


@app.route("/lancement")
def lancement():
    """Page de lancement des questions en mode relais-biathlon"""
    # Get team from query parameter (red or blue)
    team = request.args.get("team", "red")
    parcours_num = request.args.get("parcours", "1")

    # Check if this is a penalty passage (passage supplémentaire)
    is_penalty = request.args.get("penalty", "false").lower() == "true"
    joker_player = request.args.get("joker_player", "")
    joker_name = request.args.get("joker_name", "Joker C - Passage supplémentaire")

    # Check if this is a physical penalty (double-penalite joker OR wrong answer)
    is_physical_penalty = (
        request.args.get("physical_penalty", "false").lower() == "true"
    )
    penalty_exercise = request.args.get("penalty_exercise", "")
    penalty_reps = request.args.get("penalty_reps", "")

    # Check if this physical penalty is due to wrong answer
    is_wrong_answer = (
        request.args.get("wrong_answer", "false").lower() == "true"
    )
    actual_next_destination = None

    # Si c'est une pénalité physique pour mauvaise réponse, récupérer la destination
    if is_physical_penalty and is_wrong_answer and os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                wrong_answer_penalty_data = game_setup.get("wrong_answer_penalty", {})
                if wrong_answer_penalty_data:
                    actual_next_destination = wrong_answer_penalty_data.get(
                        "actual_next_destination", f"/bracelet?team={team}"
                    )
                    # Nettoyer le flag après lecture
                    game_setup.pop("wrong_answer_penalty", None)
                    with open(GAME_SETUP_FILE, "w", encoding="utf-8") as fw:
                        json.dump(game_setup, fw, ensure_ascii=False, indent=2)
        except:
            pass

    # Legacy: Check if this is old-style wrong answer penalty with timer
    is_wrong_answer_penalty = (
        request.args.get("wrong_answer_penalty", "false").lower() == "true"
    )
    penalty_duration = 20

    # Map exercise name to display title
    penalty_titles = {
        "gainage": "Position de gainage",
        "squat": "Squat",
        "parcours": "Parcours de pénalité",
        "genoux": "Montée de genoux",
        "jumpingjacks": "Jumping Jacks",
        "pompes": "Pompes",
    }
    penalty_title = penalty_titles.get(penalty_exercise, penalty_exercise)

    # Parcours text
    parcours_texts = {
        "1": "Premier parcours",
        "2": "Deuxième parcours",
        "3": "Troisième parcours",
        "4": "Quatrième parcours",
        "5": "Cinquième parcours",
        "6": "Sixième parcours",
        "7": "Septième parcours",
        "8": "Huitième parcours",
        "9": "Neuvième parcours",
        "10": "Dixième parcours",
    }
    parcours_text = parcours_texts.get(parcours_num, f"Parcours {parcours_num}")

    # Load team data based on which team
    avatar_id = "1"
    team_name = "Équipe rouge"
    player_name = "Joueur"

    if team == "red":
        if os.path.exists(RED_TEAM_FILE):
            try:
                with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                    team_data = json.load(f)
                    avatar_id = team_data.get("avatar", "1")
                    team_name = team_data.get("team_name", "Équipe rouge")
            except:
                pass
    else:
        if os.path.exists(BLUE_TEAM_FILE):
            try:
                with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                    team_data = json.load(f)
                    avatar_id = team_data.get("avatar", "2")
                    team_name = team_data.get("team_name", "Équipe bleue")
            except:
                pass

    # Get current player from game_setup
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                players = game_setup.get(f"{team}_players", [])
                player_index = game_setup.get(f"{team}_current_player_index", 0)
                if players and player_index < len(players):
                    player_name = players[player_index]
                elif players:
                    player_name = players[0]
        except:
            pass

    # Get game setup data for duration mode display
    duration_mode = "passages"
    total_etapes = 8
    current_etape = int(parcours_num)
    team_score = 0
    target_score = 10
    game_time_minutes = 32

    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                duration_mode = game_setup.get("durationMode", "passages")
                total_etapes = game_setup.get("passagesCount", 8)
                target_score = game_setup.get("reponsesCount", 10)
                game_time_minutes = game_setup.get("gameTime", 32)
        except:
            pass

    # Get team score from game-management.json
    game_management_file = os.path.join(DATA_DIR, "game-management.json")
    if os.path.exists(game_management_file):
        try:
            with open(game_management_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
                team_score = game_data.get(f"{team}_score", 0)
        except:
            pass

    return render_template(
        "lancement.html",
        team=team,
        parcours_text=parcours_text,
        avatar_id=avatar_id,
        team_name=team_name,
        player_name=player_name,
        current_etape=current_etape,
        total_etapes=total_etapes,
        is_penalty=is_penalty,
        joker_player=joker_player,
        joker_name=joker_name,
        duration_mode=duration_mode,
        team_score=team_score,
        target_score=target_score,
        game_time_minutes=game_time_minutes,
        is_physical_penalty=is_physical_penalty,
        penalty_exercise=penalty_exercise,
        penalty_title=penalty_title,
        penalty_reps=penalty_reps,
        is_wrong_answer_penalty=is_wrong_answer_penalty,
        is_wrong_answer=is_wrong_answer,
        penalty_duration=penalty_duration,
        actual_next_destination=actual_next_destination,
    )


@app.route("/prison")
def prison():
    """Page prison affichant le timer de pénalité"""
    # Get parameters
    team = request.args.get("team", "red")
    player_name = request.args.get("player", None)
    joker_used_by = request.args.get("joker_used_by", None)
    joker_team = request.args.get("joker_team", None)
    wrong_answer = request.args.get("wrong_answer", "false") == "true"
    reason = None  # Sera construit à partir des infos du joker
    actual_next_destination = None  # Destination après la prison (pour wrong_answer)

    # Si c'est une prison pour mauvaise réponse, récupérer les infos
    if wrong_answer and os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                wrong_answer_prison = game_setup.get("wrong_answer_prison", {})
                if wrong_answer_prison:
                    player_name = wrong_answer_prison.get("player", "Joueur")
                    actual_next_destination = wrong_answer_prison.get(
                        "actual_next_destination", "/bracelet?team=red"
                    )
                    reason = "il/elle a mal répondu à la question"
                    # Nettoyer le flag après lecture
                    game_setup.pop("wrong_answer_prison", None)
                    with open(GAME_SETUP_FILE, "w", encoding="utf-8") as fw:
                        json.dump(game_setup, fw, ensure_ascii=False, indent=2)
        except:
            pass

    # Si pas de nom de joueur fourni, récupérer le joueur actuel depuis game_setup
    if not player_name:
        if os.path.exists(GAME_SETUP_FILE):
            try:
                with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                    game_setup = json.load(f)
                    players = game_setup.get(f"{team}_players", [])
                    player_index = game_setup.get(f"{team}_current_player_index", 0)
                    if players and player_index < len(players):
                        player_name = players[player_index]
                    elif players:
                        player_name = players[0]
            except:
                pass
        if not player_name:
            player_name = "Joueur"

    # Construire le message de raison si pas déjà défini (cas joker)
    if not reason:
        if joker_used_by and joker_team:
            team_label = "l'équipe rouge" if joker_team == "red" else "l'équipe bleue"
            reason = f"{joker_used_by} de {team_label} a utilisé le Joker Prison"
        else:
            # Fallback si les infos du joker ne sont pas disponibles
            opponent_team = "l'équipe bleue" if team == "red" else "l'équipe rouge"
            reason = f"un joueur de {opponent_team} a utilisé le Joker Prison"

    # Load team data
    avatar_id = "1"
    team_name = "Équipe Rouge"
    players = []

    if team == "red":
        if os.path.exists(RED_TEAM_FILE):
            try:
                with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                    team_data = json.load(f)
                    avatar_id = team_data.get("avatar", "1")
                    team_name = team_data.get("team_name", "Équipe Rouge")
                    # Get players list
                    for i in range(1, 6):
                        p = team_data.get(f"joueur_{i}")
                        if p:
                            players.append(p)
            except:
                pass
    else:
        if os.path.exists(BLUE_TEAM_FILE):
            try:
                with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                    team_data = json.load(f)
                    avatar_id = team_data.get("avatar", "2")
                    team_name = team_data.get("team_name", "Équipe Bleue")
                    # Get players list
                    for i in range(1, 6):
                        p = team_data.get(f"joueur_{i}")
                        if p:
                            players.append(p)
            except:
                pass

    # Load prison time from game setup
    prison_time = 30
    sport = "basketball"
    mode = "sport-collectif"
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                prison_time = game_setup.get("prisonTime", 30)
                sport = game_setup.get("sport", "basketball")
                mode = game_setup.get("mode", "sport-collectif")
        except:
            pass

    # Count players on terrain (all except the one in prison)
    total_players = len(players) if players else 5
    players_on_terrain = total_players - 1

    return render_template(
        "prison.html",
        team=team,
        team_name=team_name,
        avatar_id=avatar_id,
        player_name=player_name,
        reason=reason,
        prison_time=prison_time,
        sport=sport,
        mode=mode,
        players=players,
        players_on_terrain=players_on_terrain,
        total_players=total_players,
        joker_used_by=joker_used_by,
        wrong_answer=wrong_answer,
        actual_next_destination=actual_next_destination,
    )


@app.route("/bracelet")
def bracelet():
    """Page bracelet affichant l'image plein écran avec le score"""
    # Get team from query parameter (red or blue)
    team = request.args.get("team", "red")

    # Load game management data for scores
    game_management_file = os.path.join(DATA_DIR, "game-management.json")
    red_score = 0
    blue_score = 0

    if os.path.exists(game_management_file):
        try:
            with open(game_management_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
                red_score = game_data.get("red_score", 0)
                blue_score = game_data.get("blue_score", 0)
        except:
            pass

    # Load game mode and current passage
    mode = "sport-collectif"
    current_passage = 1
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                mode = game_setup.get("mode", "sport-collectif")
                current_passage = game_setup.get("current_passage", 1)
        except:
            pass

    return render_template(
        "bracelet.html",
        team=team,
        red_score=red_score,
        blue_score=blue_score,
        mode=mode,
        current_passage=current_passage,
    )


@app.route("/joueurs-inactifs")
def joueurs_inactifs():
    # Load team data
    red_avatar_id = "1"
    blue_avatar_id = "2"

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team_data = json.load(f)
                red_avatar_id = red_team_data.get("avatar", "1")
        except:
            pass

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team_data = json.load(f)
                blue_avatar_id = blue_team_data.get("avatar", "2")
        except:
            pass

    # Load sport, players and penalty from game setup
    sport = "basketball"
    red_players = []
    blue_players = []
    penalty_per_player = 3  # Default value
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                red_players = game_setup.get("red_players", [])
                blue_players = game_setup.get("blue_players", [])
                penalty_per_player = game_setup.get("penalty", 3)
        except:
            pass

    # Load game-management events to find players who have answered questions
    game_mgmt_file = os.path.join(DATA_DIR, "game-management.json")
    players_who_answered = {"red": set(), "blue": set()}
    penalty_already_applied = False

    if os.path.exists(game_mgmt_file):
        try:
            with open(game_mgmt_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
                penalty_already_applied = game_data.get("penalty_applied", False)
                events = game_data.get("events", [])
                for event in events:
                    team = event.get("team")
                    player = event.get("player")
                    action = event.get("action", "")
                    # Check if this is a question event (not joker, not match start, not penalty)
                    if team in ["red", "blue"] and "Question" in action:
                        players_who_answered[team].add(player)
        except:
            pass

    # If penalty already applied, show empty list
    inactive_players = []
    red_inactive_count = 0
    blue_inactive_count = 0

    if not penalty_already_applied:
        # Find inactive players (those who haven't answered any question)
        for player in red_players:
            if player not in players_who_answered["red"]:
                inactive_players.append({"name": player, "team": "red"})
                red_inactive_count += 1

        for player in blue_players:
            if player not in players_who_answered["blue"]:
                inactive_players.append({"name": player, "team": "blue"})
                blue_inactive_count += 1

    # Calculate penalty per team
    red_penalty = red_inactive_count * penalty_per_player
    blue_penalty = blue_inactive_count * penalty_per_player
    total_penalty_display = red_penalty + blue_penalty  # For display purposes

    return render_template(
        "joueurs-inactifs.html",
        red_avatar_id=red_avatar_id,
        blue_avatar_id=blue_avatar_id,
        sport=sport,
        inactive_players=inactive_players,
        penalty_per_player=penalty_per_player,
        red_penalty=red_penalty,
        blue_penalty=blue_penalty,
        red_inactive_count=red_inactive_count,
        blue_inactive_count=blue_inactive_count,
        penalty_already_applied=penalty_already_applied,
    )


@app.route("/activate-penalty", methods=["POST"])
def activate_penalty():
    try:
        data = request.get_json()
        penalty_per_player = data.get("penalty_per_player", 3)
        inactive_players = data.get("inactive_players", [])
        current_time = data.get("current_time", "00 : 00")

        # Load game management data
        game_mgmt_file = os.path.join(DATA_DIR, "game-management.json")
        game_data = {"red_score": 0, "blue_score": 0, "events": []}

        if os.path.exists(game_mgmt_file):
            with open(game_mgmt_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)

        # Count inactive players per team
        red_inactive_count = sum(1 for p in inactive_players if p.get("team") == "red")
        blue_inactive_count = sum(1 for p in inactive_players if p.get("team") == "blue")

        # Subtract 3 points per inactive player per team
        red_penalty = red_inactive_count * penalty_per_player
        blue_penalty = blue_inactive_count * penalty_per_player

        if red_inactive_count > 0:
            game_data["red_score"] = max(
                0, game_data.get("red_score", 0) - red_penalty
            )
        if blue_inactive_count > 0:
            game_data["blue_score"] = max(
                0, game_data.get("blue_score", 0) - blue_penalty
            )

        # Add one penalty event per inactive player
        for player in inactive_players:
            penalty_event = {
                "time": current_time,
                "team": player.get("team", "all"),
                "player": player.get("name", "Inconnu"),
                "action": "Pénalité joueur inactif",
                "result": f"-{penalty_per_player} pts",
                "result_class": "penalty",
            }
            game_data["events"].append(penalty_event)

        # Mark penalty as applied
        game_data["penalty_applied"] = True

        # Save updated data
        with open(game_mgmt_file, "w", encoding="utf-8") as f:
            json.dump(game_data, f, indent=2, ensure_ascii=False)

        return jsonify({"success": True, "message": "Penalty applied"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/game-intro")
def game_intro():
    mode = ""
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                mode = game_setup.get("mode", "")
        except:
            pass
    is_bonus = request.args.get("bonus", "false") == "true"
    return render_template("game-intro.html", mode=mode, is_bonus=is_bonus)


@app.route("/game-knowledge")
def game_knowledge():
    # Get question ID and theme from query parameters
    question_id = request.args.get("questionId", type=int)
    question_theme = request.args.get("theme", type=str)
    # Check if we should skip the joker popup (used after theme joker)
    skip_joker_popup = request.args.get("skipJokerPopup", "false").lower() == "true"
    # Check if this is a bonus question (no jokers allowed)
    is_bonus = request.args.get("bonus", "false").lower() == "true"

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

    # Load game setup for level and themes
    level_name = ""
    selected_themes = []
    game_mode = "sport-collectif"
    duration_mode = "passages"
    game_time_minutes = 32
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                level_name = game_setup.get("level", "")
                selected_themes = game_setup.get("themes", [])
                game_mode = game_setup.get("mode", "sport-collectif")
                duration_mode = game_setup.get("durationMode", "passages")
                game_time_minutes = game_setup.get("gameTime", 32)
        except:
            level_name = ""
            selected_themes = []

    # Load question by ID and theme from new system
    question = None
    if question_id and question_theme:
        all_questions = load_all_questions()
        # Lookup by BOTH id and theme to handle duplicate IDs across theme files
        question = next(
            (
                q
                for q in all_questions
                if q.get("id") == question_id and q.get("theme") == question_theme
            ),
            None,
        )
        print(f"Looking up question: ID={question_id}, theme={question_theme}")
        if question:
            print(f"Found question: {question.get('question', '')[:80]}...")
        else:
            print(
                f"Question not found with ID={question_id} and theme={question_theme}"
            )
    elif question_id:
        # Fallback: lookup by ID only (for backward compatibility)
        all_questions = load_all_questions()
        question = next((q for q in all_questions if q.get("id") == question_id), None)

        # Verify the question is actually a knowledge type
        if question and question.get("gameType") != "knowledge":
            print(
                f"Warning: Question {question_id} is not a knowledge type, it's {question.get('gameType')}"
            )
            question = None

    # If no valid question found, get a random knowledge question from selected themes and level
    if not question:
        all_questions = load_all_questions()

        # Load used questions from game_setup
        used_questions = []
        if os.path.exists(GAME_SETUP_FILE):
            try:
                with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                    gs = json.load(f)
                    used_questions = gs.get("used_questions", [])
            except:
                pass

        # Filter by gameType=knowledge, matching themes and level, exclude used questions
        # Use composite key (theme_id) to avoid conflicts between themes with same question IDs
        knowledge_questions = [
            q
            for q in all_questions
            if q.get("gameType") == "knowledge"
            and q.get("theme") in selected_themes
            and q.get("level") == level_name
            and f"{q.get('theme')}_{q.get('id')}" not in used_questions
        ]

        if knowledge_questions:
            question = random.choice(knowledge_questions)

            # Mark question as used (composite key to handle same IDs across themes)
            used_questions.append(f"{question.get('theme')}_{question.get('id')}")
            if os.path.exists(GAME_SETUP_FILE):
                try:
                    with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                        gs = json.load(f)
                    gs["used_questions"] = used_questions
                    with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                        json.dump(gs, f, ensure_ascii=False, indent=2)
                except:
                    pass
        else:
            return (
                f"No knowledge questions available for themes {selected_themes} and level {level_name}",
                404,
            )

    if not question:
        return "No question available", 404

    # Get all available options
    all_options = question.get("options", [])
    correct_answer_data = question.get("correctAnswer", 0)

    # Handle correctAnswer being either int or list
    # Convert to list for uniform handling
    if isinstance(correct_answer_data, list):
        correct_answer_indices = correct_answer_data
    else:
        correct_answer_indices = [correct_answer_data]

    # Get the correct answer texts
    correct_answers = [
        all_options[idx] for idx in correct_answer_indices
        if idx < len(all_options)
    ]

    # Use all options (no level-based filtering for now)
    final_options = all_options.copy()

    # Always shuffle the options to randomize order
    random.shuffle(final_options)

    # Find the indices of all correct answers in the shuffled list
    correct_answer_indices_shuffled = [
        final_options.index(answer) for answer in correct_answers
    ]

    # Get team parameter
    team = request.args.get("team", "red")

    # Load jokers and duel points from game setup
    jokers = []
    duel_points = 3
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                all_jokers = game_setup.get("jokers", [])
                duel_points = game_setup.get("duelPoints", 3)
                # Filter out jokers already used by this team
                team_jokers_used = game_setup.get(f"{team}_jokers_used", [])
                jokers = [j for j in all_jokers if j not in team_jokers_used]
        except:
            jokers = []

    # Load actual scores from game-management.json
    game_management_file = os.path.join(DATA_DIR, "game-management.json")
    red_score = 0
    blue_score = 0
    if os.path.exists(game_management_file):
        try:
            with open(game_management_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
                red_score = game_data.get("red_score", 0)
                blue_score = game_data.get("blue_score", 0)
        except:
            pass

    return render_template(
        "game-knowledge.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=red_score,
        blue_score=blue_score,
        question_image=question.get("image"),
        question_text=question.get("question"),
        options=final_options,
        correctAnswer=correct_answer_indices_shuffled,
        level=level_name,
        answer_time=get_answer_time(),
        jokers=jokers,
        question_theme=question.get("theme"),
        question_id=question.get("id"),
        skip_joker_popup=skip_joker_popup,
        is_bonus=is_bonus,
        team=team,
        duel_points=duel_points,
        game_mode=game_mode,
        duration_mode=duration_mode,
        game_time_minutes=game_time_minutes,
        question=question,
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
        answer_time=get_answer_time(),
    )


@app.route("/game-link")
def game_link():
    """Page de jeu de connexion (relier les éléments)"""
    # Get question parameters
    question_id = request.args.get("questionId", type=int)
    question_theme = request.args.get("theme", "")
    team = request.args.get("team", "red")
    skip_joker_popup = request.args.get("skipJokerPopup", "false") == "true"
    is_bonus = request.args.get("bonus", "false") == "true"

    # Load team data and scores
    red_avatar = "1"
    blue_avatar = "1"
    red_score = 0
    blue_score = 0

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            pass

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            pass

    # Load scores from game_setup
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                red_score = game_setup.get("red_score", 0)
                blue_score = game_setup.get("blue_score", 0)
        except:
            pass

    # Load question from theme file
    question = None
    if question_id and question_theme:
        theme_file = os.path.join(CONTENT_DIR, f"{question_theme}.json")
        if os.path.exists(theme_file):
            try:
                with open(theme_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    questions = data.get("questions", [])
                    for q in questions:
                        if q.get("id") == question_id and q.get("gameType") == "gameLink":
                            question = q
                            break
            except:
                pass

    if not question:
        return "Question non trouvée", 404

    # Get left and right items (support both camelCase and snake_case)
    left_items = question.get("leftItems", question.get("left_items", [])).copy()
    right_items = question.get("rightItems", question.get("right_items", [])).copy()
    correct_pairs = question.get("correctPairs", question.get("correct_pairs", []))

    # Shuffle items
    random.shuffle(left_items)
    random.shuffle(right_items)

    # Load jokers for current team and game mode
    jokers = []
    game_mode = "sport-collectif"
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                game_mode = game_setup.get("mode", "sport-collectif")
                all_jokers = ["theme", "team", "double-point", "double-prison", "switch", "indice"]
                used_jokers = game_setup.get(f"{team}_jokers_used", [])
                jokers = [j for j in all_jokers if j not in used_jokers]
        except:
            pass

    return render_template(
        "game-link.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=red_score,
        blue_score=blue_score,
        question_text=question.get("question", ""),
        question_id=question_id,
        question_theme=question_theme,
        left_items=left_items,
        right_items=right_items,
        correct_pairs=correct_pairs,
        answer_time=get_answer_time(),
        jokers=jokers,
        team=team,
        skip_joker_popup=skip_joker_popup,
        is_bonus=is_bonus,
        game_mode=game_mode,
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
        answer_time=get_answer_time(),
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
        answer_time=get_answer_time(),
    )


@app.route("/game-fillBlanks")
def game_fillBlanks():
    """Page de jeu de remplissage de trous (équations chimiques, etc.)"""
    # Get question ID and theme from query parameters
    question_id = request.args.get("questionId", type=int)
    question_theme = request.args.get("theme", type=str)
    skip_joker_popup = request.args.get("skipJokerPopup", "false").lower() == "true"
    is_bonus = request.args.get("bonus", "false").lower() == "true"
    team = request.args.get("team", "red")

    # Load red and blue team data
    red_avatar = "1"
    blue_avatar = "1"

    if os.path.exists(RED_TEAM_FILE):
        try:
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_avatar = red_data.get("avatar", "1")
        except:
            pass

    if os.path.exists(BLUE_TEAM_FILE):
        try:
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_avatar = blue_data.get("avatar", "1")
        except:
            pass

    # Load game setup for game mode
    game_mode = "sport-collectif"
    jokers = []
    duel_points = 3
    duration_mode = "questions"
    game_time_minutes = 32
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                game_mode = game_setup.get("mode", "sport-collectif")
                all_jokers = game_setup.get("jokers", [])
                team_jokers_used = game_setup.get(f"{team}_jokers_used", [])
                jokers = [j for j in all_jokers if j not in team_jokers_used]
                duel_points = game_setup.get("duel_points", 3)
                duration_mode = game_setup.get("duration_mode", "questions")
                game_time_minutes = game_setup.get("game_time", 32)
        except:
            pass

    # Load question from theme file
    question = None
    if question_theme and question_id:
        theme_file = os.path.join(CONTENT_DIR, f"{question_theme}.json")
        if os.path.exists(theme_file):
            try:
                with open(theme_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    questions = data.get("questions", [])
                    for q in questions:
                        if q.get("id") == question_id and q.get("gameType") == "fillBlanks":
                            question = q
                            break
            except:
                pass

    if not question:
        return "Question non trouvée", 404

    # Get template and items
    template = question.get("template", "")
    items = question.get("items", [])
    correct_answer = question.get("correctAnswer", [])

    # Shuffle the items
    shuffled_items = items.copy()
    random.shuffle(shuffled_items)

    # Load scores from game-management.json
    game_management_file = os.path.join(DATA_DIR, "game-management.json")
    red_score = 0
    blue_score = 0
    if os.path.exists(game_management_file):
        try:
            with open(game_management_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
                red_score = game_data.get("red_score", 0)
                blue_score = game_data.get("blue_score", 0)
        except:
            pass

    return render_template(
        "game-fillBlanks.html",
        red_avatar=red_avatar,
        blue_avatar=blue_avatar,
        red_score=red_score,
        blue_score=blue_score,
        question_image=question.get("image"),
        question_text=question.get("question"),
        template=template,
        shuffled_items=shuffled_items,
        correct_answer=correct_answer,
        answer_time=get_answer_time(),
        jokers=jokers,
        skip_joker_popup=skip_joker_popup,
        is_bonus=is_bonus,
        team=team,
        game_mode=game_mode,
        question_theme=question_theme,
        question_id=question_id,
        duel_points=duel_points,
        duration_mode=duration_mode,
        game_time_minutes=game_time_minutes,
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
        answer_time=get_answer_time(),
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


@app.route("/get-current-player")
def get_current_player():
    """Récupère le joueur actuel pour une équipe donnée"""
    try:
        team = request.args.get("team", "red")

        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"error": "Game setup not found"}), 404

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        players = game_setup.get(f"{team}_players", [])
        player_index = game_setup.get(f"{team}_current_player_index", 0)
        current_round = game_setup.get("current_round", 1)
        total_rounds = game_setup.get("total_rounds", 1)

        if players and player_index < len(players):
            current_player = players[player_index]
        elif players:
            current_player = players[0]
        else:
            current_player = f"Joueur {team.capitalize()}"

        return jsonify(
            {
                "success": True,
                "player": current_player,
                "player_index": player_index,
                "current_round": current_round,
                "total_rounds": total_rounds,
                "all_players": players,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/get-red-team")
def get_red_team():
    """Récupère les données de l'équipe rouge"""
    try:
        if os.path.exists(RED_TEAM_FILE):
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_team = json.load(f)
                # Build players array from joueur_1, joueur_2, etc.
                players = []
                for i in range(1, 11):
                    player = red_team.get(f"joueur_{i}")
                    if player:
                        players.append(player)
                red_team["players"] = players
                return jsonify(red_team)
        else:
            return jsonify({"players": []}), 404
    except Exception as e:
        return jsonify({"error": str(e), "players": []}), 500


@app.route("/get-blue-team")
def get_blue_team():
    """Récupère les données de l'équipe bleue"""
    try:
        if os.path.exists(BLUE_TEAM_FILE):
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_team = json.load(f)
                # Build players array from joueur_1, joueur_2, etc.
                players = []
                for i in range(1, 11):
                    player = blue_team.get(f"joueur_{i}")
                    if player:
                        players.append(player)
                blue_team["players"] = players
                return jsonify(blue_team)
        else:
            return jsonify({"players": []}), 404
    except Exception as e:
        return jsonify({"error": str(e), "players": []}), 500


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


@app.route("/init-game", methods=["POST"])
def init_game():
    """Initialise le match: tracking des jokers par équipe et event de début"""
    try:
        # Charger game_setup existant
        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"success": False, "error": "Game setup not found"}), 404

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        # Charger les joueurs des deux équipes
        red_players = []
        blue_players = []

        if os.path.exists(RED_TEAM_FILE):
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                # Récupérer les joueurs (format joueur_1, joueur_2, etc.)
                for i in range(1, 11):  # Support jusqu'à 10 joueurs
                    player = red_data.get(f"joueur_{i}")
                    if player:
                        red_players.append(player)

        if os.path.exists(BLUE_TEAM_FILE):
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                for i in range(1, 11):
                    player = blue_data.get(f"joueur_{i}")
                    if player:
                        blue_players.append(player)

        # Si pas de joueurs définis, mettre des valeurs par défaut
        if not red_players:
            red_players = ["Joueur Rouge 1", "Joueur Rouge 2"]
        if not blue_players:
            blue_players = ["Joueur Bleu 1", "Joueur Bleu 2"]

        # Calculer le nombre de tours = min des joueurs entre les deux équipes
        total_rounds = min(len(red_players), len(blue_players))

        # Ajouter les champs de tracking
        game_setup["current_team"] = "red"
        game_setup["red_jokers_used"] = []
        game_setup["blue_jokers_used"] = []
        game_setup["double_points_active"] = None
        game_setup["prison_pending"] = None
        game_setup["passage_pending"] = (
            None  # Pour mode relais-biathlon (joker Passage en plus)
        )
        game_setup["red_players"] = red_players
        game_setup["blue_players"] = blue_players
        game_setup["red_current_player_index"] = 0
        game_setup["blue_current_player_index"] = 0
        game_setup["current_round"] = 1
        game_setup["total_rounds"] = total_rounds
        game_setup["current_passage"] = 1  # Pour mode relais-biathlon
        game_setup["used_questions"] = []  # Liste des IDs de questions déjà posées

        # Sauvegarder game_setup
        with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
            json.dump(game_setup, f, ensure_ascii=False, indent=2)

        # Charger les noms des équipes (déjà chargés plus haut)
        red_team_name = "Rouge"
        blue_team_name = "Bleue"
        if os.path.exists(RED_TEAM_FILE):
            with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                red_data = json.load(f)
                red_team_name = red_data.get("team_name", "Rouge")
        if os.path.exists(BLUE_TEAM_FILE):
            with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                blue_data = json.load(f)
                blue_team_name = blue_data.get("team_name", "Bleue")

        # Créer game-management.json avec l'event de début
        game_management_file = os.path.join(DATA_DIR, "game-management.json")
        game_mode = game_setup.get("mode", "sport-collectif")
        start_result = (
            "🏃 Parcours en cours"
            if game_mode == "relais-biathlon"
            else "🎯 Match en cours"
        )
        game_management_data = {
            "red_score": 0,
            "blue_score": 0,
            "events": [
                {
                    "time": "00:00",
                    "team": "both",
                    "player": f"{red_team_name} vs {blue_team_name}",
                    "action": "Début du match",
                    "result": start_result,
                    "result_class": "neutral",
                }
            ],
        }

        with open(game_management_file, "w", encoding="utf-8") as f:
            json.dump(game_management_data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Game initialized"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-goal", methods=["POST"])
def save_goal():
    """Sauvegarde un but/panier/essai marqué par un joueur"""
    try:
        data = request.get_json()
        team = data.get("team", "red")
        player_name = data.get("player_name", "Joueur")
        current_time = data.get("current_time", "00:00")

        # Charger game_setup pour obtenir le sport et sportPoints
        sport = "basketball"
        sport_points = 1
        if os.path.exists(GAME_SETUP_FILE):
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                sport_points = game_setup.get("sportPoints", 1)

        # Action selon le sport
        sport_actions = {
            "basketball": "Panier",
            "rugby": "Essai",
            "ultimate": "Point",
            "handball": "But",
            "football": "But",
            "hockey": "But",
        }
        action = sport_actions.get(sport, "Point")

        # Charger et mettre à jour game-management.json
        game_management_file = os.path.join(DATA_DIR, "game-management.json")
        if os.path.exists(game_management_file):
            with open(game_management_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)
        else:
            game_data = {"red_score": 0, "blue_score": 0, "events": []}

        # Mettre à jour le score
        score_key = f"{team}_score"
        game_data[score_key] = game_data.get(score_key, 0) + sport_points

        # Ajouter l'event
        event = {
            "time": current_time,
            "team": team,
            "player": player_name,
            "action": action,
            "result": f"+{sport_points} pts",
            "result_class": "points",
        }
        game_data["events"].append(event)

        # Sauvegarder
        with open(game_management_file, "w", encoding="utf-8") as f:
            json.dump(game_data, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "success": True,
                "red_score": game_data.get("red_score", 0),
                "blue_score": game_data.get("blue_score", 0),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/save-question-result", methods=["POST"])
def save_question_result():
    """Sauvegarde le résultat d'une question et retourne la prochaine destination"""
    try:
        data = request.get_json()
        team = data.get("team", "red")
        correct = data.get("correct", False)
        base_points = data.get("points", 3)
        joker_used = data.get("joker_used")
        question_theme = data.get("question_theme", "Question")
        player_name = data.get("player_name")  # Peut être None
        current_time = data.get("current_time", "00:00")
        is_bonus = data.get("is_bonus", False)  # Mode bonus
        time_up = data.get("time_up", False)  # Temps écoulé (mode relais-biathlon time)

        # Charger game_setup pour vérifier double_points
        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        # Toujours récupérer le joueur actuel depuis game_setup (ignorer la valeur par défaut "Joueur")
        players = game_setup.get(f"{team}_players", [])
        player_index = game_setup.get(f"{team}_current_player_index", 0)
        if players and player_index < len(players):
            player_name = players[player_index]
        elif players:
            player_name = players[0]
        else:
            player_name = player_name or "Joueur"

        # En mode bonus, utiliser les bonus_points (priorité sur le mode de jeu)
        if is_bonus:
            base_points = game_setup.get("bonus_points", 3)
        else:
            # En mode relais-biathlon (hors bonus), 1 point par bonne réponse
            game_mode = game_setup.get("mode", "sport-collectif")
            if game_mode == "relais-biathlon":
                base_points = 1

        game_mode = game_setup.get("mode", "sport-collectif")

        # Calculer les points
        points = base_points if correct else 0

        # Appliquer le joker double-point immédiatement si utilisé pour cette question
        if correct and joker_used == "double-point":
            points = points * 2

        # Si joker utilisé, l'ajouter à la liste des jokers utilisés par l'équipe
        if joker_used:
            jokers_used_key = f"{team}_jokers_used"
            if jokers_used_key not in game_setup:
                game_setup[jokers_used_key] = []
            if joker_used not in game_setup[jokers_used_key]:
                game_setup[jokers_used_key].append(joker_used)

            # Si joker prison, marquer l'adversaire pour prison avec les infos du joueur qui l'a utilisé
            if joker_used == "double-prison":
                opponent = "blue" if team == "red" else "red"
                game_setup["prison_pending"] = {
                    "team": opponent,
                    "joker_used_by": player_name,
                    "joker_team": team,
                }

            # Si joker double-passage (mode relais-biathlon), marquer l'adversaire pour passage supplémentaire
            if joker_used == "double-passage":
                opponent = "blue" if team == "red" else "red"
                game_setup["passage_pending"] = {
                    "team": opponent,
                    "joker_used_by": player_name,
                    "joker_team": team,
                }

            # Si joker double-penalite (mode relais-biathlon), marquer l'adversaire pour pénalité physique
            if joker_used == "double-penalite":
                opponent = "blue" if team == "red" else "red"
                game_setup["penalite_pending"] = {
                    "team": opponent,
                    "joker_used_by": player_name,
                    "joker_team": team,
                }

        # Sauvegarder game_setup
        with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
            json.dump(game_setup, f, ensure_ascii=False, indent=2)

        # Charger et mettre à jour game-management.json
        game_management_file = os.path.join(DATA_DIR, "game-management.json")
        with open(game_management_file, "r", encoding="utf-8") as f:
            game_data = json.load(f)

        # Mettre à jour le score
        score_key = f"{team}_score"
        game_data[score_key] = game_data.get(score_key, 0) + points

        # Ajouter l'event pour le joker si utilisé
        if joker_used:
            joker_names = {
                "double-prison": "Joker Prison",
                "double-point": "Joker Double Points",
                "double-passage": "Joker Passage en plus",
                "double-penalite": "Joker Double Pénalité",
                "theme": "Joker Thème",
                "switch": "Joker Switch",
                "indice": "Joker Indice",
                "team": "Joker Team",
            }
            joker_event = {
                "time": current_time,
                "team": team,
                "player": player_name,
                "action": joker_names.get(joker_used, f"Joker {joker_used}"),
                "result": "🃏",
                "result_class": "joker",
            }
            game_data["events"].append(joker_event)

        # Ajouter l'event pour la question
        result_text = f"+{points} pts" if correct else "0 pts"
        result_class = "correct" if correct else "incorrect"
        action_text = (
            "Question Bonus" if is_bonus else f"Question {question_theme.capitalize()}"
        )
        event = {
            "time": current_time,
            "team": team,
            "player": player_name,
            "action": action_text,
            "result": result_text,
            "result_class": result_class,
        }
        game_data["events"].append(event)

        # Sauvegarder game-management.json
        with open(game_management_file, "w", encoding="utf-8") as f:
            json.dump(game_data, f, ensure_ascii=False, indent=2)

        # Mode bonus: premier qui répond correctement gagne
        # Rouge passe en premier, si correct → fin, sinon bleu passe
        if is_bonus:
            if team == "red":
                if correct:
                    # Rouge a répondu correctement → Rouge gagne, fin du bonus
                    game_setup["bonus_round_active"] = False
                    game_setup["bonus_points"] = None
                    next_destination = "/game-end"
                else:
                    # Rouge a répondu incorrectement → Bleu passe
                    next_destination = "/bracelet?team=blue&bonus=true"
            else:
                # Après blue (correct ou non), round bonus terminé
                game_setup["bonus_round_active"] = False
                game_setup["bonus_points"] = None
                next_destination = "/game-end"

            # Sauvegarder game_setup
            with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                json.dump(game_setup, f, ensure_ascii=False, indent=2)

            return jsonify(
                {
                    "success": True,
                    "next_destination": next_destination,
                    "red_score": game_data.get("red_score", 0),
                    "blue_score": game_data.get("blue_score", 0),
                    "is_bonus": True,
                }
            )

        # Mode relais-biathlon: logique spécifique
        if game_mode == "relais-biathlon":
            current_passage = game_setup.get("current_passage", 1)
            red_score = game_data.get("red_score", 0)
            blue_score = game_data.get("blue_score", 0)
            duration_mode = game_setup.get("durationMode", "passages")

            # Vérifier les conditions de fin (après que blue ait joué)
            game_ended = False
            if team == "blue":
                if duration_mode == "passages":
                    # Nombre de passages atteint
                    passages_count = game_setup.get("passagesCount", 10)
                    if current_passage >= passages_count:
                        game_ended = True

                elif duration_mode == "reponses":
                    # Un des scores atteint la limite de points
                    reponses_count = game_setup.get("reponsesCount", 10)
                    if red_score >= reponses_count or blue_score >= reponses_count:
                        game_ended = True

                elif duration_mode == "time":
                    # Le frontend envoie time_up=true quand le temps est écoulé
                    if time_up:
                        game_ended = True

            if game_ended:
                actual_next_destination = "/game-management"
            elif team == "red":
                # Après red, c'est au tour de blue
                actual_next_destination = "/bracelet?team=blue"
            else:
                # Après blue, passage suivant avec red
                game_setup["current_passage"] = current_passage + 1

                # Passer au joueur suivant pour chaque équipe (avec cycling)
                red_players = game_setup.get("red_players", [])
                blue_players = game_setup.get("blue_players", [])
                red_index = game_setup.get("red_current_player_index", 0)
                blue_index = game_setup.get("blue_current_player_index", 0)

                game_setup["red_current_player_index"] = (
                    (red_index + 1) % len(red_players) if red_players else 0
                )
                game_setup["blue_current_player_index"] = (
                    (blue_index + 1) % len(blue_players) if blue_players else 0
                )

                actual_next_destination = "/bracelet?team=red"

            # Si mauvaise réponse, aller d'abord à la pénalité physique
            if not correct:
                penalties = game_setup.get("penalties", ["gainage"])
                parcours = game_setup.get("parcours", "motricite")
                random_penalty = random.choice(penalties) if penalties else "gainage"

                # Define reps/duration based on parcours type (same as check-penalite)
                penalty_info = {
                    "gainage": {
                        "motricite": "Durée de 10 s",
                        "urbain": "Durée de 20 s",
                    },
                    "squat": {
                        "motricite": "Durée de 10 s",
                        "urbain": "Durée de 20 s",
                    },
                    "parcours": {
                        "motricite": "Temps du parcours",
                        "urbain": "Temps du parcours",
                    },
                    "genoux": {
                        "motricite": "Durée de 10 s",
                        "urbain": "Durée de 20 s",
                    },
                    "jumpingjacks": {
                        "motricite": "15 répétitions",
                        "urbain": "30 répétitions",
                    },
                    "pompes": {
                        "motricite": "5 répétitions",
                        "urbain": "10 répétitions",
                    },
                }
                penalty_reps = penalty_info.get(random_penalty, {}).get(parcours, "")

                # Fallback si pas de reps trouvé
                if not penalty_reps:
                    penalty_reps = "10 répétitions" if parcours == "urbain" else "5 répétitions"

                # Ajouter un event de pénalité pour mauvaise réponse
                penalty_event = {
                    "time": current_time,
                    "team": team,
                    "player": player_name,
                    "action": "Mauvaise réponse",
                    "result": "Pénalité",
                    "result_class": "penalty",
                }
                game_data["events"].append(penalty_event)

                # Re-sauvegarder game-management.json avec l'event de pénalité
                with open(game_management_file, "w", encoding="utf-8") as f:
                    json.dump(game_data, f, ensure_ascii=False, indent=2)

                # Sauvegarder la vraie destination pour après la pénalité
                game_setup["wrong_answer_penalty"] = {
                    "team": team,
                    "player": player_name,
                    "actual_next_destination": actual_next_destination,
                }

                # Utiliser le même format que physical_penalty
                next_destination = (
                    f"/lancement?team={team}&physical_penalty=true"
                    f"&penalty_exercise={quote(random_penalty)}"
                    f"&penalty_reps={quote(penalty_reps)}"
                    f"&wrong_answer=true"
                )
            else:
                next_destination = actual_next_destination

            # Sauvegarder game_setup
            with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                json.dump(game_setup, f, ensure_ascii=False, indent=2)

            return jsonify(
                {
                    "success": True,
                    "next_destination": next_destination,
                    "red_score": red_score,
                    "blue_score": blue_score,
                    "current_passage": game_setup.get("current_passage", 1),
                    "game_ended": game_ended,
                }
            )

        # Mode sport-collectif: récupérer les infos de tour et joueurs
        current_round = game_setup.get("current_round", 1)
        total_rounds = game_setup.get("total_rounds", 1)
        red_players = game_setup.get("red_players", [])
        blue_players = game_setup.get("blue_players", [])

        # Déterminer la prochaine destination (alternance red/blue)
        if team == "red":
            # Après red, c'est au tour de blue
            next_team = "blue"
            actual_next_destination = f"/bracelet?team={next_team}"
        else:
            # Après blue, le round est terminé
            # Passer au joueur suivant pour chaque équipe (avec cycling)
            red_index = game_setup.get("red_current_player_index", 0)
            blue_index = game_setup.get("blue_current_player_index", 0)

            # Incrémenter les index (avec modulo pour cycler)
            game_setup["red_current_player_index"] = (
                (red_index + 1) % len(red_players) if red_players else 0
            )
            game_setup["blue_current_player_index"] = (
                (blue_index + 1) % len(blue_players) if blue_players else 0
            )
            game_setup["current_round"] = current_round + 1

            # Vérifier si tous les rounds sont terminés
            if current_round >= total_rounds:
                # Match terminé, retour à game-management
                actual_next_destination = "/game-management"
            else:
                # Round suivant, équipe rouge commence
                next_team = "red"
                actual_next_destination = f"/bracelet?team={next_team}"

        # Si mauvaise réponse, aller d'abord en prison
        if not correct:
            prison_time = game_setup.get("penalty", 3)  # Durée de prison = penalty
            game_setup["wrong_answer_prison"] = {
                "team": team,
                "player": player_name,
                "prison_time": prison_time,
                "actual_next_destination": actual_next_destination,
            }

            # Ajouter un event de pénalité pour mauvaise réponse
            penalty_event = {
                "time": current_time,
                "team": team,
                "player": player_name,
                "action": "Mauvaise réponse",
                "result": "Prison",
                "result_class": "penalty",
            }
            game_data["events"].append(penalty_event)

            # Re-sauvegarder game-management.json avec l'event de pénalité
            with open(game_management_file, "w", encoding="utf-8") as f:
                json.dump(game_data, f, ensure_ascii=False, indent=2)

            next_destination = f"/prison?team={team}&wrong_answer=true"
        else:
            next_destination = actual_next_destination

        # Sauvegarder game_setup avec les index mis à jour
        with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
            json.dump(game_setup, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "success": True,
                "next_destination": next_destination,
                "red_score": game_data.get("red_score", 0),
                "blue_score": game_data.get("blue_score", 0),
                "current_round": game_setup.get("current_round", 1),
                "total_rounds": total_rounds,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/check-prison")
def check_prison():
    """Vérifie si une équipe doit aller en prison"""
    try:
        team = request.args.get("team", "")

        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"prison_pending": False})

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        prison_data = game_setup.get("prison_pending")

        # Gérer le nouveau format (dict) et l'ancien format (string)
        if isinstance(prison_data, dict):
            prison_pending = prison_data.get("team") == team
            joker_used_by = prison_data.get("joker_used_by") if prison_pending else None
            joker_team = prison_data.get("joker_team") if prison_pending else None
        else:
            prison_pending = prison_data == team
            joker_used_by = None
            joker_team = None

        # Clear prison_pending if it was for this team
        if prison_pending:
            game_setup["prison_pending"] = None
            with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                json.dump(game_setup, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "prison_pending": prison_pending,
                "joker_used_by": joker_used_by,
                "joker_team": joker_team,
            }
        )
    except Exception as e:
        return jsonify({"prison_pending": False, "error": str(e)})


@app.route("/check-passage")
def check_passage():
    """Vérifie si une équipe doit effectuer un passage supplémentaire (mode relais-biathlon)"""
    try:
        team = request.args.get("team", "")

        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"passage_pending": False})

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        passage_data = game_setup.get("passage_pending")

        # Gérer le format dict
        if isinstance(passage_data, dict):
            passage_pending = passage_data.get("team") == team
            joker_used_by = (
                passage_data.get("joker_used_by") if passage_pending else None
            )
            joker_team = passage_data.get("joker_team") if passage_pending else None
        else:
            passage_pending = passage_data == team
            joker_used_by = None
            joker_team = None

        # Clear passage_pending if it was for this team
        if passage_pending:
            game_setup["passage_pending"] = None
            with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                json.dump(game_setup, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "passage_pending": passage_pending,
                "joker_used_by": joker_used_by,
                "joker_team": joker_team,
            }
        )
    except Exception as e:
        return jsonify({"passage_pending": False, "error": str(e)})


@app.route("/check-penalite")
def check_penalite():
    """Vérifie si une équipe doit effectuer une pénalité physique (mode relais-biathlon)"""
    try:
        team = request.args.get("team", "")

        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"penalite_pending": False})

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        penalite_data = game_setup.get("penalite_pending")

        # Gérer le format dict
        if isinstance(penalite_data, dict):
            penalite_pending = penalite_data.get("team") == team
            joker_used_by = (
                penalite_data.get("joker_used_by") if penalite_pending else None
            )
            joker_team = penalite_data.get("joker_team") if penalite_pending else None
        else:
            penalite_pending = penalite_data == team
            joker_used_by = None
            joker_team = None

        # Get penalty exercise info if pending
        penalty_exercise = None
        penalty_reps = None
        if penalite_pending:
            # Get configured penalties and parcours type
            penalties = game_setup.get("penalties", [])
            parcours = game_setup.get("parcours", "motricite")

            if penalties:
                # Choose random penalty from configured ones
                penalty_exercise = random.choice(penalties)

                # Define reps/duration based on parcours type
                penalty_info = {
                    "gainage": {
                        "motricite": "Durée de 10 s",
                        "urbain": "Durée de 20 s",
                    },
                    "squat": {"motricite": "Durée de 10 s", "urbain": "Durée de 20 s"},
                    "parcours": {
                        "motricite": "Temps du parcours",
                        "urbain": "Temps du parcours",
                    },
                    "genoux": {"motricite": "Durée de 10 s", "urbain": "Durée de 20 s"},
                    "jumpingjacks": {
                        "motricite": "15 répétitions",
                        "urbain": "30 répétitions",
                    },
                    "pompes": {
                        "motricite": "5 répétitions",
                        "urbain": "10 répétitions",
                    },
                }
                penalty_reps = penalty_info.get(penalty_exercise, {}).get(parcours, "")

            # Clear penalite_pending
            game_setup["penalite_pending"] = None
            with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                json.dump(game_setup, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "penalite_pending": penalite_pending,
                "joker_used_by": joker_used_by,
                "joker_team": joker_team,
                "penalty_exercise": penalty_exercise,
                "penalty_reps": penalty_reps,
            }
        )
    except Exception as e:
        return jsonify({"penalite_pending": False, "error": str(e)})


@app.route("/remove-joker", methods=["POST"])
def remove_joker():
    """Marque un joker comme utilisé par une équipe"""
    try:
        data = request.get_json()
        joker_to_remove = data.get("joker")
        team = data.get("team", "red")  # Équipe qui utilise le joker

        if not joker_to_remove:
            return jsonify({"success": False, "error": "No joker specified"}), 400

        # Charger les données existantes
        if os.path.exists(GAME_SETUP_FILE):
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
        else:
            return (
                jsonify({"success": False, "error": "Game setup file not found"}),
                404,
            )

        # Ajouter le joker à la liste des jokers utilisés par l'équipe
        team_jokers_key = f"{team}_jokers_used"
        team_jokers_used = game_setup.get(team_jokers_key, [])

        if joker_to_remove not in team_jokers_used:
            team_jokers_used.append(joker_to_remove)
            game_setup[team_jokers_key] = team_jokers_used

            # Sauvegarder
            with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                json.dump(game_setup, f, ensure_ascii=False, indent=2)

            return jsonify(
                {
                    "success": True,
                    "message": f"Joker {joker_to_remove} marked as used by {team}",
                }
            )
        else:
            return jsonify(
                {
                    "success": True,
                    "message": f"Joker {joker_to_remove} already used by {team}",
                }
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def load_all_questions():
    """Helper function to load all questions from content directory JSON files"""
    question_files = [
        "chimie.json",
        "francais.json",
        "geographie.json",
        "histoire.json",
        "math.json",
        "svt.json",
    ]

    all_questions = []

    # Load questions from each file in content directory
    for filename in question_files:
        filepath = os.path.join(CONTENT_DIR, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    questions = data.get("questions", [])
                    all_questions.extend(questions)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                continue

    return all_questions


@app.route("/get-random-question")
def get_random_question():
    """
    Load a random question based on game setup configuration.
    Filters by: themes and level only (any gameType).
    Excludes questions already used in this game session.
    Returns the question data along with gameType for routing.
    """
    try:
        # Load game setup
        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"success": False, "error": "Game setup not found"}), 404

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        selected_themes = game_setup.get("themes", [])
        selected_level = game_setup.get("level", "")
        used_questions = game_setup.get("used_questions", [])

        if not selected_themes:
            return jsonify({"success": False, "error": "No themes selected"}), 400

        # Load all questions
        all_questions = load_all_questions()

        if not all_questions:
            return jsonify({"success": False, "error": "No questions available"}), 404

        # Filter questions by theme and level only (any gameType)
        # Use composite key (theme_id) to avoid conflicts between themes with same question IDs
        filtered_questions = [
            q
            for q in all_questions
            if q.get("theme") in selected_themes
            and q.get("level") == selected_level
            and f"{q.get('theme')}_{q.get('id')}" not in used_questions
        ]

        if not filtered_questions:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"No questions found for themes {selected_themes} and level {selected_level}",
                    }
                ),
                404,
            )

        # Select random question
        question = random.choice(filtered_questions)
        game_type = question.get("gameType", "knowledge")

        # Mark question as used (composite key to handle same IDs across themes)
        used_questions.append(f"{question.get('theme')}_{question.get('id')}")
        game_setup["used_questions"] = used_questions
        with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
            json.dump(game_setup, f, ensure_ascii=False, indent=2)

        # Return question data with gameType for routing
        return jsonify(
            {
                "success": True,
                "gameType": game_type,
                "question": question,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/get-question-by-id")
def get_question_by_id():
    """
    Load a specific question by ID from all question files.
    Used by game pages to load the selected question.
    """
    try:
        question_id = request.args.get("id", type=int)
        if question_id is None:
            return jsonify({"success": False, "error": "No question ID provided"}), 400

        # Load all questions
        all_questions = load_all_questions()

        # Find question by ID
        question = next((q for q in all_questions if q.get("id") == question_id), None)

        if not question:
            return jsonify({"success": False, "error": "Question not found"}), 404

        return jsonify({"success": True, "question": question})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/get-available-themes", methods=["POST"])
def get_available_themes():
    """
    Get list of ALL available themes (excluding current theme) for theme joker selection.
    Expects: currentTheme in request body
    Returns: List of all available themes (all 6 themes minus current)
    """
    try:
        data = request.get_json()
        current_theme = data.get("currentTheme")

        print(f"DEBUG get-available-themes - Current theme received: '{current_theme}'")

        # All available themes in the game (must match theme field in JSON files)
        all_themes = ["chimie", "francais", "geographie", "histoire", "math", "svt"]

        # Get all themes except current one
        available_themes = [t for t in all_themes if t != current_theme]

        print(f"DEBUG get-available-themes - All themes: {all_themes}")
        print(f"DEBUG get-available-themes - Available themes: {available_themes}")

        if not available_themes:
            return (
                jsonify({"success": False, "error": "No other themes available"}),
                400,
            )

        return jsonify({"success": True, "themes": available_themes})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/apply-theme-joker", methods=["POST"])
def apply_theme_joker():
    """
    Theme joker: Get a new question from a specific chosen theme.
    Expects: selectedTheme, currentGameType in request body
    Returns: New question from the selected theme
    """
    try:
        data = request.get_json()
        selected_theme = data.get("selectedTheme")
        current_game_type = data.get("currentGameType", "knowledge")

        print("\n" + "=" * 70)
        print("APPLY THEME JOKER - BACKEND DEBUG")
        print("=" * 70)
        print(f"Request JSON: {data}")
        print(f"Selected theme: '{selected_theme}'")
        print(f"Selected theme type: {type(selected_theme)}")
        print(f"Selected theme repr: {repr(selected_theme)}")
        print(f"Current game type: '{current_game_type}'")

        if not selected_theme:
            return (
                jsonify({"success": False, "error": "Selected theme not provided"}),
                400,
            )

        # Load game setup
        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"success": False, "error": "Game setup not found"}), 404

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        selected_level = game_setup.get("level", "")
        used_questions = game_setup.get("used_questions", [])
        print(f"DEBUG - Selected level: {selected_level}")

        # Load all questions
        all_questions = load_all_questions()
        print(f"\nTotal questions loaded: {len(all_questions)}")

        # Show sample of actual theme values in questions
        sample_themes = set(q.get("theme") for q in all_questions[:50])
        print(f"Sample themes in loaded questions: {sample_themes}")
        print(f"\nFiltering criteria:")
        print(f"  theme == '{selected_theme}' (type: {type(selected_theme)})")
        print(f"  level == '{selected_level}'")
        print(f"  gameType == '{current_game_type}'")

        # Filter by: selected theme, same level, ANY gameType, exclude used questions
        # Use composite key (theme_id) to avoid conflicts between themes with same question IDs
        filtered_questions = [
            q
            for q in all_questions
            if q.get("theme") == selected_theme
            and q.get("level") == selected_level
            and f"{q.get('theme')}_{q.get('id')}" not in used_questions
        ]

        print(f"\nFiltering results:")
        print(
            f"  Questions with theme=='{selected_theme}': {len([q for q in all_questions if q.get('theme') == selected_theme])}"
        )
        print(
            f"  Questions with level=='{selected_level}': {len([q for q in all_questions if q.get('level') == selected_level])}"
        )
        print(f"  Final filtered questions: {len(filtered_questions)}")
        if filtered_questions:
            print(
                f"  Sample filtered themes: {[q.get('theme') for q in filtered_questions[:3]]}"
            )

        if not filtered_questions:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"No questions available for theme {selected_theme}",
                    }
                ),
                404,
            )

        # Select random question
        question = random.choice(filtered_questions)
        print(f"\nSelected question:")
        print(f"  ID: {question.get('id')}")
        print(f"  Theme: '{question.get('theme')}'")
        print(f"  Level: '{question.get('level')}'")
        print(f"  GameType: '{question.get('gameType')}'")
        print(f"  Question text: {question.get('question', '')[:80]}...")
        print("=" * 70 + "\n")

        # Mark question as used (composite key to handle same IDs across themes)
        used_questions.append(f"{question.get('theme')}_{question.get('id')}")
        game_setup["used_questions"] = used_questions
        with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
            json.dump(game_setup, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "success": True,
                "question": question,
                "questionId": question.get("id"),
                "theme": question.get("theme"),
                "gameType": question.get("gameType", "knowledge"),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/apply-switch-joker", methods=["POST"])
def apply_switch_joker():
    """
    Switch joker: Get a different question from the SAME theme.
    Expects: currentTheme, currentQuestionId, gameType in request body
    Returns: New question from the same theme (excluding current question)
    """
    try:
        data = request.get_json()
        current_theme = data.get("currentTheme")
        current_question_id = data.get("currentQuestionId")
        game_type = data.get("gameType", "knowledge")

        print("\n" + "=" * 70)
        print("APPLY SWITCH JOKER - BACKEND DEBUG")
        print("=" * 70)
        print(f"Current theme: '{current_theme}'")
        print(f"Current question ID: {current_question_id}")
        print(f"Game type: '{game_type}'")

        if not current_theme:
            return (
                jsonify({"success": False, "error": "Current theme not provided"}),
                400,
            )

        # Load game setup
        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"success": False, "error": "Game setup not found"}), 404

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        selected_level = game_setup.get("level", "")
        used_questions = game_setup.get("used_questions", [])
        print(f"Selected level: '{selected_level}'")

        # Load all questions
        all_questions = load_all_questions()
        print(f"Total questions loaded: {len(all_questions)}")

        # Filter by: SAME theme, same level, ANY gameType, exclude used questions
        # Use composite key (theme_id) to avoid conflicts between themes with same question IDs
        filtered_questions = [
            q
            for q in all_questions
            if q.get("theme") == current_theme
            and q.get("level") == selected_level
            and f"{q.get('theme')}_{q.get('id')}" not in used_questions
        ]

        print(f"\nFiltering results:")
        print(
            f"  Questions with same theme: {len([q for q in all_questions if q.get('theme') == current_theme])}"
        )
        print(
            f"  Questions with same level: {len([q for q in all_questions if q.get('level') == selected_level])}"
        )
        print(f"  Excluding used questions: {len(used_questions)} already used")
        print(f"  Final filtered questions: {len(filtered_questions)}")

        if not filtered_questions:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Pas d'autre question disponible pour ce thème",
                    }
                ),
                404,
            )

        # Select random question
        question = random.choice(filtered_questions)
        print(f"\nSelected question:")
        print(f"  ID: {question.get('id')}")
        print(f"  Theme: '{question.get('theme')}'")
        print(f"  Question: {question.get('question', '')[:80]}...")
        print("=" * 70 + "\n")

        # Mark question as used (composite key to handle same IDs across themes)
        used_questions.append(f"{question.get('theme')}_{question.get('id')}")
        game_setup["used_questions"] = used_questions
        with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
            json.dump(game_setup, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "success": True,
                "question": question,
                "questionId": question.get("id"),
                "theme": question.get("theme"),
                "gameType": question.get("gameType", "knowledge"),
            }
        )

    except Exception as e:
        print(f"Error in apply_switch_joker: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
