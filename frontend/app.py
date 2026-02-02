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
    # Charger les données de fin de match
    GAME_END_FILE = os.path.join(DATA_DIR, "game-end.json")

    if os.path.exists(GAME_END_FILE):
        try:
            with open(GAME_END_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return render_template("game-end.html", data=data)
        except Exception as e:
            print(f"Erreur lors du chargement de game-end.json: {e}")

    # Données par défaut si le fichier n'existe pas
    default_data = {
        "final_score": {"red_team": 0, "blue_team": 0, "winner": "blue"},
        "teams": {
            "red": {"name": "Équipe rouge", "avatar": "1", "players": []},
            "blue": {"name": "Équipe bleue", "avatar": "2", "players": []},
        },
        "mvp": {
            "red": {
                "player": "Joueur",
                "avatar": "1",
                "stats": {"points_scored": 0, "duels_won": 0, "jokers_used": 0},
            },
            "blue": {
                "player": "Joueur",
                "avatar": "2",
                "stats": {"points_scored": 0, "duels_won": 0, "jokers_used": 0},
            },
        },
        "duels": [],
        "questions": [],
        "penalties": [],
        "jokers": {"red": [], "blue": []},
        "game_info": {
            "mode": "sport-collectif",
            "sport": "basketball",
            "level": "Cycle 4",
            "duration": "00:00",
            "themes": [],
        },
    }

    return render_template("game-end.html", data=default_data)


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
        "10": "Dixième parcours"
    }
    parcours_text = parcours_texts.get(parcours_num, f"Parcours {parcours_num}")

    # Load team data based on which team
    avatar_id = "1"
    team_name = "Équipe rouge"
    player_name = "Joueur"
    players = []

    if team == "red":
        if os.path.exists(RED_TEAM_FILE):
            try:
                with open(RED_TEAM_FILE, "r", encoding="utf-8") as f:
                    team_data = json.load(f)
                    avatar_id = team_data.get("avatar", "1")
                    team_name = team_data.get("team_name", "Équipe rouge")
                    players = team_data.get("players", [])
            except:
                pass
    else:
        if os.path.exists(BLUE_TEAM_FILE):
            try:
                with open(BLUE_TEAM_FILE, "r", encoding="utf-8") as f:
                    team_data = json.load(f)
                    avatar_id = team_data.get("avatar", "2")
                    team_name = team_data.get("team_name", "Équipe bleue")
                    players = team_data.get("players", [])
            except:
                pass

    # Get current player (based on parcours number)
    parcours_index = int(parcours_num) - 1
    if players and parcours_index < len(players):
        player_name = players[parcours_index].get("name", players[parcours_index]) if isinstance(players[parcours_index], dict) else players[parcours_index]
    elif players:
        player_name = players[0].get("name", players[0]) if isinstance(players[0], dict) else players[0]

    # Get total etapes from game setup
    total_etapes = 8
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                total_etapes = game_setup.get("passages", 8)
        except:
            pass

    current_etape = int(parcours_num)

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
        joker_name=joker_name
    )


@app.route("/prison")
def prison():
    """Page prison affichant le timer de pénalité"""
    # Get parameters
    team = request.args.get("team", "red")
    player_name = request.args.get("player", "Joueur")
    reason = request.args.get("reason", "mauvaise réponse")

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
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                prison_time = game_setup.get("prisonTime", 30)
                sport = game_setup.get("sport", "basketball")
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
        players=players,
        players_on_terrain=players_on_terrain,
        total_players=total_players
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

    return render_template(
        "bracelet.html",
        team=team,
        red_score=red_score,
        blue_score=blue_score
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

    # Load sport and penalty from game setup
    sport = "basketball"
    penalty_points = 3
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                sport = game_setup.get("sport", "basketball")
                penalty_points = game_setup.get("penalty", 3)
        except:
            pass

    # Load inactive players data
    inactive_file = os.path.join(DATA_DIR, "joueurs-inactifs.json")
    inactive_players = []

    if os.path.exists(inactive_file):
        try:
            with open(inactive_file, "r", encoding="utf-8") as f:
                inactive_data = json.load(f)
                # Get inactive players with team info
                red_inactive = inactive_data.get("red_team", {}).get(
                    "inactive_players", []
                )
                blue_inactive = inactive_data.get("blue_team", {}).get(
                    "inactive_players", []
                )
                # Create list with player name and team
                for player in red_inactive:
                    inactive_players.append({"name": player, "team": "red"})
                for player in blue_inactive:
                    inactive_players.append({"name": player, "team": "blue"})
        except:
            pass

    return render_template(
        "joueurs-inactifs.html",
        red_avatar_id=red_avatar_id,
        blue_avatar_id=blue_avatar_id,
        sport=sport,
        inactive_players=inactive_players,
        penalty_points=penalty_points,
    )


@app.route("/activate-penalty", methods=["POST"])
def activate_penalty():
    try:
        data = request.get_json()
        penalty_points = data.get("penalty_points", 0)
        inactive_players = data.get("inactive_players", [])
        current_time = data.get("current_time", "00 : 00")

        # Load game management data
        game_mgmt_file = os.path.join(DATA_DIR, "game-management.json")
        game_data = {"red_score": 0, "blue_score": 0, "events": []}

        if os.path.exists(game_mgmt_file):
            with open(game_mgmt_file, "r", encoding="utf-8") as f:
                game_data = json.load(f)

        # Check which teams have inactive players
        has_red_inactive = any(p.get("team") == "red" for p in inactive_players)
        has_blue_inactive = any(p.get("team") == "blue" for p in inactive_players)

        # Subtract penalty only from teams with inactive players
        if has_red_inactive:
            game_data["red_score"] = max(
                0, game_data.get("red_score", 0) - penalty_points
            )
        if has_blue_inactive:
            game_data["blue_score"] = max(
                0, game_data.get("blue_score", 0) - penalty_points
            )

        # Add one penalty event per inactive player
        for player in inactive_players:
            penalty_event = {
                "time": current_time,
                "team": player.get("team", "all"),
                "player": player.get("name", "Inconnu"),
                "action": "Pénalité joueur inactif",
                "result": f"-{penalty_points} pts",
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
    mode = ''
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                mode = game_setup.get('mode', '')
        except:
            pass
    is_bonus = request.args.get('bonus', 'false') == 'true'
    return render_template("game-intro.html", mode=mode, is_bonus=is_bonus)


@app.route("/game-knowledge")
def game_knowledge():
    # Get question ID and theme from query parameters
    question_id = request.args.get("questionId", type=int)
    question_theme = request.args.get("theme", type=str)
    # Check if we should skip the joker popup (used after theme joker)
    skip_joker_popup = request.args.get("skipJokerPopup", "false").lower() == "true"

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
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                level_name = game_setup.get("level", "")
                selected_themes = game_setup.get("themes", [])
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
        # Filter by gameType=knowledge, matching themes and level (strict)
        knowledge_questions = [
            q
            for q in all_questions
            if q.get("gameType") == "knowledge"
            and q.get("theme") in selected_themes
            and q.get("level") == level_name
        ]

        if knowledge_questions:
            question = random.choice(knowledge_questions)
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
    # For knowledge questions, it should be an int (index)
    # For link/order questions, it might be a list
    if isinstance(correct_answer_data, list):
        # If it's a list, take the first element or default to 0
        correct_answer_index = correct_answer_data[0] if correct_answer_data else 0
    else:
        correct_answer_index = correct_answer_data

    correct_answer = (
        all_options[correct_answer_index]
        if correct_answer_index < len(all_options)
        else all_options[0]
    )

    # Use all options (no level-based filtering for now)
    final_options = all_options.copy()

    # Always shuffle the options to randomize order
    random.shuffle(final_options)

    # Find the index of correct answer in the shuffled list
    correct_answer_index = final_options.index(correct_answer)

    # Load jokers from game setup
    jokers = []
    if os.path.exists(GAME_SETUP_FILE):
        try:
            with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
                game_setup = json.load(f)
                jokers = game_setup.get("jokers", [])
        except:
            jokers = []

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
        level=level_name,
        answer_time=get_answer_time(),
        jokers=jokers,
        question_theme=question.get("theme"),
        question_id=question.get("id"),
        skip_joker_popup=skip_joker_popup,
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
        answer_time=get_answer_time(),
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


@app.route("/remove-joker", methods=["POST"])
def remove_joker():
    """Retire un joker de la liste des jokers disponibles dans game_setup.json"""
    try:
        # Récupérer le joker à retirer
        data = request.get_json()
        joker_to_remove = data.get("joker")

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

        # Retirer le joker de la liste
        jokers = game_setup.get("jokers", [])
        if joker_to_remove in jokers:
            jokers.remove(joker_to_remove)
            game_setup["jokers"] = jokers

            # Sauvegarder
            with open(GAME_SETUP_FILE, "w", encoding="utf-8") as f:
                json.dump(game_setup, f, ensure_ascii=False, indent=2)

            return jsonify(
                {"success": True, "message": f"Joker {joker_to_remove} removed"}
            )
        else:
            return jsonify({"success": False, "error": "Joker not found in setup"}), 404

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
    Filters by: themes, level, and gameType.
    Returns the question data along with gameType for routing.
    """
    try:
        # Get optional gameType parameter (defaults to "knowledge")
        requested_game_type = request.args.get("gameType", "knowledge")

        # Load game setup
        if not os.path.exists(GAME_SETUP_FILE):
            return jsonify({"success": False, "error": "Game setup not found"}), 404

        with open(GAME_SETUP_FILE, "r", encoding="utf-8") as f:
            game_setup = json.load(f)

        selected_themes = game_setup.get("themes", [])
        selected_level = game_setup.get("level", "")

        if not selected_themes:
            return jsonify({"success": False, "error": "No themes selected"}), 400

        # Load all questions
        all_questions = load_all_questions()

        if not all_questions:
            return jsonify({"success": False, "error": "No questions available"}), 404

        # Filter questions by theme, level, AND gameType (strict - no fallback)
        filtered_questions = [
            q
            for q in all_questions
            if q.get("theme") in selected_themes
            and q.get("level") == selected_level
            and q.get("gameType") == requested_game_type
        ]

        if not filtered_questions:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"No {requested_game_type} questions found for themes {selected_themes} and level {selected_level}",
                    }
                ),
                404,
            )

        # Select random question
        question = random.choice(filtered_questions)
        game_type = question.get("gameType", requested_game_type)

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

        # Filter by: selected theme, same level, same gameType
        filtered_questions = [
            q
            for q in all_questions
            if q.get("theme") == selected_theme
            and q.get("level") == selected_level
            and q.get("gameType") == current_game_type
        ]

        print(f"\nFiltering results:")
        print(
            f"  Questions with theme=='{selected_theme}': {len([q for q in all_questions if q.get('theme') == selected_theme])}"
        )
        print(
            f"  Questions with level=='{selected_level}': {len([q for q in all_questions if q.get('level') == selected_level])}"
        )
        print(
            f"  Questions with gameType=='{current_game_type}': {len([q for q in all_questions if q.get('gameType') == current_game_type])}"
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

        return jsonify(
            {
                "success": True,
                "question": question,
                "questionId": question.get("id"),
                "theme": question.get("theme"),
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
        print(f"Selected level: '{selected_level}'")

        # Load all questions
        all_questions = load_all_questions()
        print(f"Total questions loaded: {len(all_questions)}")

        # Filter by: SAME theme, same level, same gameType, but DIFFERENT id
        filtered_questions = [
            q
            for q in all_questions
            if q.get("theme") == current_theme
            and q.get("level") == selected_level
            and q.get("gameType") == game_type
            and q.get("id") != current_question_id
        ]

        print(f"\nFiltering results:")
        print(
            f"  Questions with same theme: {len([q for q in all_questions if q.get('theme') == current_theme])}"
        )
        print(
            f"  Questions with same level: {len([q for q in all_questions if q.get('level') == selected_level])}"
        )
        print(
            f"  Questions with same gameType: {len([q for q in all_questions if q.get('gameType') == game_type])}"
        )
        print(f"  Excluding current question ID: {current_question_id}")
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

        return jsonify(
            {
                "success": True,
                "question": question,
                "questionId": question.get("id"),
                "theme": question.get("theme"),
            }
        )

    except Exception as e:
        print(f"Error in apply_switch_joker: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
