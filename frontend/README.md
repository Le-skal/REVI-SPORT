# Révi'Sport - Frontend Application

## 📋 Overview

Révi'Sport is a Flask-based web application for managing sports team compositions with interactive player naming and avatar selection. The application features a responsive design optimized for 600x1024px portrait displays.

## 🗂️ Project Structure

```
frontend/
├── app.py                      # Flask application with routes
├── requirements.txt            # Python dependencies
├── data/                       # JSON data storage (cleared on app start)
│   ├── red_team_names.json    # Red team player names
│   ├── red_team_avatar.json   # Red team avatar selection
│   ├── blue_team_names.json   # Blue team player names
│   └── blue_team_avatar.json  # Blue team avatar selection
├── static/
│   ├── css/                   # Stylesheets
│   │   ├── style.css          # Global styles
│   │   ├── loading.css        # Loading page animation
│   │   ├── home.css           # Home page styles
│   │   ├── mode.css           # Mode selection page
│   │   ├── sport.css          # Sport selection page
│   │   ├── basketball.css     # Basketball composition page
│   │   ├── nom_red_basketball.css
│   │   ├── nom_blue_basketball.css
│   │   ├── avatar_red_basketball.css
│   │   └── avatar_blue_basketball.css
│   ├── img/                   # Images organized by page
│   │   ├── back.png           # Back button icon
│   │   ├── logo.png           # App logo
│   │   ├── basketball.png     # Loading animation basketball
│   │   ├── mode/              # Mode selection images
│   │   ├── sport/             # Sport selection images
│   │   ├── basketball/        # Basketball page images
│   │   ├── avatars/           # Avatar images (btn_avatar1-16.png)
│   │   ├── nom_red_basketball/
│   │   └── nom_blue_basketball/
│   └── js/                    # JavaScript files (currently unused)
└── templates/                 # HTML templates
    ├── loading.html           # Splash screen with animation
    ├── home.html              # Logo and progress bar
    ├── mode.html              # Mode selection
    ├── sport.html             # Sport selection
    ├── basketball.html        # Team composition display
    ├── nom_red_basketball.html
    ├── nom_blue_basketball.html
    ├── avatar_red_basketball.html
    └── avatar_blue_basketball.html
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Flask 2.3.2

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

## 🎮 Application Flow

### Complete User Journey

```
1. Loading (/)
   └─> Animated basketball bounce (2.5s)
   
2. Home (/home)
   └─> Logo + progress bar (auto-redirect)
   
3. Mode Selection (/mode)
   └─> Choose game mode
   
4. Sport Selection (/sport)
   └─> Select Basketball
   
5. Basketball Composition (/basketball)
   ├─> Name Red Team → /nom_red_basketball
   │   ├─> Enter 5 player names
   │   ├─> Saves to red_team_names.json
   │   └─> Choose Avatar → /avatar_red_basketball
   │       ├─> Select from 16 avatars
   │       ├─> Saves to red_team_avatar.json
   │       └─> Returns to /basketball (red team displayed)
   │
   └─> Name Blue Team → /nom_blue_basketball
       ├─> Enter 5 player names
       ├─> Saves to blue_team_names.json
       └─> Choose Avatar → /avatar_blue_basketball
           ├─> Select from 16 avatars
           ├─> Saves to blue_team_avatar.json
           └─> Returns to /basketball (both teams displayed)
```

## 🛣️ Routes

### Page Routes

| Route | Template | Description |
|-------|----------|-------------|
| `/` | `loading.html` | Splash screen with basketball animation |
| `/home` | `home.html` | Logo display with progress bar |
| `/mode` | `mode.html` | Game mode selection |
| `/sport` | `sport.html` | Sport selection (6 options) |
| `/basketball` | `basketball.html` | Team composition display |
| `/nom_red_basketball` | `nom_red_basketball.html` | Red team player naming form |
| `/nom_blue_basketball` | `nom_blue_basketball.html` | Blue team player naming form |
| `/avatar_red_basketball` | `avatar_red_basketball.html` | Red team avatar selection |
| `/avatar_blue_basketball` | `avatar_blue_basketball.html` | Blue team avatar selection |

### API Routes

| Route | Method | Description | Request Body | Response |
|-------|--------|-------------|--------------|----------|
| `/save-red-team` | POST | Save red team player names | `{joueur_1: string, ..., joueur_5: string}` | `{success: boolean}` |
| `/save-red-avatar` | POST | Save red team avatar | `{avatar: string}` | `{success: boolean}` |
| `/save-blue-team` | POST | Save blue team player names | `{joueur_1: string, ..., joueur_5: string}` | `{success: boolean}` |
| `/save-blue-avatar` | POST | Save blue team avatar | `{avatar: string}` | `{success: boolean}` |

## 🎨 Design System

### Screen Dimensions
- **Width:** 600px
- **Height:** 1024px
- **Orientation:** Portrait
- **Border:** 3px gold (#f0c400) for development

### Color Palette

```css
/* Base Colors */
--background: #111117
--primary-gold: #f0c400
--text-white: #ffffff

/* Team Colors */
--red-team: rgb(186, 74, 74)
--blue-team: rgb(74, 128, 186)
```

### Typography
- **Font Family:** Poppins, sans-serif
- **Title Size:** 40% width, 20% margin-top
- **Body Text:** 14-22px depending on context

## 📁 Data Structure

### Team Names JSON
```json
{
  "joueur_1": "PlayerName1",
  "joueur_2": "PlayerName2",
  "joueur_3": "PlayerName3",
  "joueur_4": "PlayerName4",
  "joueur_5": "PlayerName5"
}
```

### Avatar JSON
```json
{
  "avatar": "7"
}
```

## 🔧 Key Features

### 1. Dynamic Team Display
- **Before completion:** Shows clickable "Nommer l'équipe" buttons
- **After completion:** Shows "btn_red_after.png" / "btn_blue_after.png" with player names overlay
- **Non-clickable:** Completed team buttons prevent re-editing

### 2. Avatar Display on Court
- Completed teams show their selected avatar on the basketball court
- Avatars displayed as circular images (50x50px)
- Red team: left side, Blue team: right side
- Border colors match team colors

### 3. Form Validation
- Player naming forms require all 5 fields to be filled
- "Suivant" button only appears when form is complete
- Real-time validation with JavaScript

### 4. Data Persistence Reset
- All JSON files are cleared when loading the root route (`/`)
- Ensures fresh start for each session

## 🎯 Image Naming Conventions

### Avatars
- **Button avatars:** `btn_avatar1.png` to `btn_avatar16.png` (used in selection grid)
- **Display avatars:** `avatar1.png` to `avatar16.png` (used on court display)

### Buttons
- **Red team:** `btn_red.png` (before) → `btn_red_after.png` (after)
- **Blue team:** `btn_blue.png` (before) → `btn_blue_after.png` (after)

### Page-Specific Images
- Organized in subdirectories: `img/basketball/`, `img/mode/`, etc.
- Common pattern: `title.png`, `intro.png`, `field.png`, `suivant.png`

## 🚧 Development Notes

### CSS Organization
- `style.css`: Global styles (screen container, body, common elements)
- Page-specific CSS: Each page has its own stylesheet for modularity
- Hover effects: `transform: scale(1.03-1.05)` for interactive elements

### JavaScript Features
- Form validation in player naming pages
- Fetch API for saving data to backend
- Client-side input validation before submission

## 📝 TODO / Future Improvements

- [ ] Add base.html template for common HTML structure
- [ ] Implement game logic after team setup
- [ ] Add player statistics tracking
- [ ] Create img/common/ for shared UI elements
- [ ] Add comprehensive error handling
- [ ] Implement data persistence option (optional JSON clearing)
- [ ] Add unit tests for routes
- [ ] Document backend integration points

## 🤝 Contributing

When adding new pages:
1. Create HTML template in `templates/`
2. Create page-specific CSS in `static/css/`
3. Add images to `static/img/[page_name]/`
4. Add route in `app.py`
5. Update this README with new route and flow

## 📄 License

[Add your license here]

## 👥 Authors

[Add author information here]

---

**Last Updated:** October 28, 2025
