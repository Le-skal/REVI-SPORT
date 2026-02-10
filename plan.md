# Plan de refonte du flow - Mode Sport Collectif

## Objectif
Créer un flow fonctionnel pour la démo ce soir en mode sport collectif.

---

## POINTS CRITIQUES À NE PAS OUBLIER

### 1. Scores et Events toujours à jour
- Les points doivent être enregistrés dans `game-management.json` après CHAQUE question
- Ajouter une ligne d'event à chaque action (début match, bonne réponse, mauvaise réponse, joker utilisé)
- Les scores affichés sur TOUTES les pages (game-management, bracelet, game-knowledge) doivent être synchronisés

### 2. Questions filtrées par thèmes sélectionnés
- Les questions doivent UNIQUEMENT venir des thèmes choisis dans game_setup.json
- Vérifier que `/get-random-question` et `/game-knowledge` filtrent bien par `themes[]`
- Bug actuel: tu as choisi histoire+geo mais tu as eu une question de chimie = à corriger!

**BUG IDENTIFIÉ:**
Dans `game-intro.html` ligne 60, on passe seulement `questionId` mais pas `theme`:
```javascript
// ACTUEL (bugué):
window.location.href = `${route}?questionId=${questionId}${bonusParam}`;

// CORRIGÉ:
window.location.href = `${route}?questionId=${questionId}&theme=${data.question.theme}${bonusParam}`;
```
Sans le theme, game-knowledge cherche par ID seul et peut trouver une question d'un autre thème avec le même ID!

---

## Flow actuel
```
recapitulatif → countdown → game-intro → game-knowledge (question)
```

## Flow cible
```
recapitulatif → countdown → game-intro → game-management
                                              ↓ (5 sec auto)
                                         bracelet (red)
                                              ↓ (auto)
                                         game-knowledge (red team question)
                                              ↓ (après réponse)
                                         bracelet (blue)
                                              ↓ (auto)
                                         game-knowledge (blue team question)
                                              ↓ (après réponse)
                                         game-management (retour)
                                              ↓ (repeat...)
```
---

## Étapes d'implémentation

### Étape 1: Structure de données pour le tracking
**Fichier:** `game_setup.json` (ajout de champs)

Ajouter:
```json
{
  "current_team": "red",           // Équipe qui joue actuellement
  "red_jokers_used": [],           // Jokers utilisés par équipe rouge
  "blue_jokers_used": [],          // Jokers utilisés par équipe bleue
  "double_points_active": null,    // "red" ou "blue" si actif
  "prison_pending": null           // "red" ou "blue" si l'adversaire doit aller en prison
}
```

### Étape 2: Modifier game-intro pour rediriger vers game-management
**Fichier:** `game-intro.html`

- Au lieu d'aller vers game-knowledge, rediriger vers `/game-management?start=true`
- Le paramètre `start=true` déclenche l'ajout de l'event "Début du match"

### Étape 3: Modifier game-management pour le flow automatique
**Fichiers:** `game-management.html`, `app.py`

- Si `?start=true`, ajouter event "Début du match" dans game-management.json
- Après 5 secondes, rediriger vers `/bracelet?team=red`

### Étape 4: Modifier bracelet pour rediriger vers la question
**Fichier:** `bracelet.html`

- Après un délai (3-5 sec), rediriger vers `/game-knowledge?team=red` ou `?team=blue`
- Passer le paramètre `team` pour savoir quelle équipe répond

### Étape 5: Modifier game-knowledge pour gérer les équipes
**Fichiers:** `game-knowledge.html`, `app.py`

- Ajouter paramètre `team` pour savoir quelle équipe joue
- Charger les jokers disponibles pour CETTE équipe (pas tous les jokers)
- Après la réponse:
  - Calculer les points (x2 si double_points_active)
  - Si prison joker utilisé, marquer `prison_pending` pour l'adversaire
  - Rediriger vers `/bracelet?team=blue` (ou retour game-management si c'était blue)

### Étape 6: Gérer le joker prison
**Fichiers:** `game-knowledge.html`, `app.py`

- Si `prison_pending` est défini pour l'équipe qui va jouer:
  - Rediriger vers `/prison?team=X` au lieu de la question
  - Après prison, continuer le flow normal

### Étape 7: Gérer le joker double-points
**Fichiers:** `game-knowledge.html`, `app.py`

- Quand une équipe utilise double-points:
  - Sauvegarder `double_points_active: "red"` (ou "blue")
- Quand l'équipe marque des points:
  - Multiplier par 2 si leur joker est actif
  - Désactiver après utilisation

### Étape 8: API pour sauvegarder le résultat d'une question
**Fichier:** `app.py`

Nouvelle route: `POST /save-question-result`
```json
{
  "team": "red",
  "correct": true,
  "points": 3,
  "joker_used": "double-points",  // ou null
  "question_text": "Quelle est la capitale...",
  "player_name": "Joueur 1"
}
```

**Actions:**
- Met à jour `game-management.json`:
  - `red_score` ou `blue_score` += points
  - Ajoute un event:
    ```json
    {
      "time": "05:23",
      "team": "red",
      "player": "Joueur 1",
      "action": "Question Histoire",
      "result": "+3 pts",
      "result_class": "correct"
    }
    ```
- Met à jour les jokers utilisés par équipe dans `game_setup.json`
- Retourne la prochaine destination + scores actuels

---

## Ordre d'implémentation recommandé

1. **Étape 1** - Structure données (safe, pas de casse)
2. **Étape 2** - Redirect game-intro → game-management
3. **Étape 3** - Event "Début match" + timer 5sec
4. **Étape 4** - Bracelet auto-redirect
5. **Étape 8** - API save-question-result (backend d'abord)
6. **Étape 5** - game-knowledge avec team + flow retour
7. **Étape 7** - Double points
8. **Étape 6** - Joker prison

---

## Questions/Clarifications

1. Le joker "prison" envoie l'adversaire en prison AVANT ou APRÈS sa question?
   - Proposition: AVANT (l'adversaire fait sa pénalité, puis répond à sa question)

2. Durée sur la page bracelet avant la question?
   - Proposition: 3 secondes

3. Après que les 2 équipes ont répondu, retour automatique à game-management?
   - Proposition: Oui, avec les scores mis à jour

4. Les points du sport (3 pour basket, etc.) sont dans game_setup.json?
   - À vérifier

---

## Fichiers impactés

- `frontend/templates/game-intro.html`
- `frontend/templates/game-management.html`
- `frontend/templates/bracelet.html`
- `frontend/templates/game-knowledge.html`
- `frontend/app.py`
- `frontend/data/game_setup.json`
- `frontend/data/game-management.json`

---

**Prêt à commencer? Valide ce plan et on attaque étape par étape.**
