# ============================# DIFFICULTY LEVELS CONFIGURATION# ============================# Level 1: Easy
EASY_LEVEL = {
    "name": "EASY",
    "player_life": 5,
    "enemy_spawn_interval": 1.5,
    "game_duration": 60.0 # seconds
}# Level 2: Normal
NORMAL_LEVEL = {
    "name": "NORMAL",
    "player_life": 3,
    "enemy_spawn_interval": 1.0,
    "game_duration": 45.0
}# Level 3: Hard
HARD_LEVEL = {
    "name": "HARD",
    "player_life": 1,
    "enemy_spawn_interval": 0.5,
    "game_duration": 30.0
}

DIFFICULTY_LEVELS = {
    "EASY": EASY_LEVEL,
    "NORMAL": NORMAL_LEVEL,
    "HARD": HARD_LEVEL
}

# ============================#
# LEVEL SELECTION (MOVED HERE)
# ============================#
CURRENT_DIFFICULTY_KEY = "NORMAL"
CURRENT_LEVEL = DIFFICULTY_LEVELS.get(CURRENT_DIFFICULTY_KEY, NORMAL_LEVEL)


# Configuraciones restantes (las mantengo sin cambios)

# Game timings and speeds
GAME_DURATION = CURRENT_LEVEL["game_duration"]
SHOT_INTERVAL = 0.5
ENEMY_SPAWN_INTERVAL = CURRENT_LEVEL["enemy_spawn_interval"]
PLAYER_SPEED = 12.0
SHOT_SPEED = 30.0
EXPLOSION_DURATION = 0.5
EXPLOSION_SPEED = 5.0
BONUS_SPAWN_INTERVAL = 10.0

# Screen shake parameters
SHAKE_INTENSITY = 0.5
SHAKE_DURATION = 0.4

# Red filter parameters
RED_FILTER_INTENSITY = 0.4
RED_FILTER_DURATION = 0.3

# Screen / game area bounds and positions
LEFT_BOUND = -3.5
RIGHT_BOUND = 3.5
PLAYER_START_X = 0.0
PLAYER_START_Y = -10.0
ENEMY_SPAWN_Y = 26.0

# Calculate bonus spawn positions
TOTAL_WIDTH = RIGHT_BOUND - LEFT_BOUND
BONUS_SPAWN_POSITIONS = [
    LEFT_BOUND + (TOTAL_WIDTH * 0.25),
    LEFT_BOUND + (TOTAL_WIDTH * 0.75)
]

# Camera settings (third-person view)
CAMERA_DISTANCE = 10.0
CAMERA_HEIGHT = 10.0
CAMERA_LOOK_AT_OFFSET = 10.0

# Scales for sprites
PLAYER_SCALE = 2.0
SHOT_SCALE = 0.6
EXPLOSION_SCALE = 0.5
EXPLOSION_SCALE_MULTIPLIER = 1.1
BONUS_SCALE = 5.0

# Bonus parameters
BONUS_STARTING_VALUE = -5
BONUS_MAX_VALUE = 10
BONUS_MIN_VALUE = BONUS_STARTING_VALUE
BONUS_SPEED = 3.0
BONUS_TRANSPARENCY = 0.6

# Window configuration parameters
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 750
WINDOW_TITLE = "Panda3D Shooting Game"

# Asset file paths
CHARACTER_IDLE_IMAGE = "assets/character_idle.png"
CHARACTER_LEFT_IMAGE = "assets/character_left.png"
CHARACTER_RIGHT_IMAGE = "assets/character_right.png"
SHOT_IMAGE = "assets/shot.png"
EXPLOSION_IMAGE = "assets/explosion.png"
BONUS_POSITIVE_IMAGE = "assets/bonus_positive.png"
BONUS_NEGATIVE_IMAGE = "assets/bonus_negative.png"
BACKGROUND_IMAGE = "assets/background.png"

# Background parameters
BACKGROUND_POS_X = 0.0
BACKGROUND_POS_Y = -3.0
BACKGROUND_SCALE = 12

# Enemy types configuration
ENEMY_TYPES = {
    1: {"hp": 1,  "speed": 15.0 / 4, "scale": 1.0, "image": "assets/enemy2.png"},
    2: {"hp": 2,  "speed": 12.0 / 4, "scale": 1.2, "image": "assets/enemy2.png"},
    3: {"hp": 6,  "speed": 9.0 / 5,  "scale": 1.4, "image": "assets/enemy3.png"},
    4: {"hp": 8, "speed": 6.0 / 5,  "scale": 1.7, "image": "assets/enemy.png"},
}

# Enemy spawn probabilities (45%, 25%, 20%, 10%)
ENEMY_SPAWN_PROB = [0.45, 0.25, 0.20, 0.10]

# Player configuration
PLAYER_STARTING_LIFE = CURRENT_LEVEL["player_life"]

HIGH_SCORE_FILE = "highscores.json"
MAX_HIGH_SCORES = 5