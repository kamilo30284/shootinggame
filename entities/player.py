from game_config import (
    PLAYER_START_X, PLAYER_START_Y, PLAYER_SCALE, PLAYER_SPEED,
    LEFT_BOUND, RIGHT_BOUND,
    CHARACTER_IDLE_IMAGE, CHARACTER_LEFT_IMAGE, CHARACTER_RIGHT_IMAGE,
    SHOT_INTERVAL, SHOT_SCALE,
    BONUS_MIN_VALUE, BONUS_MAX_VALUE
)

class Player:
    def __init__(self, game):
        self.game = game
        self.textures = {
            "idle": self.game.loader.loadTexture(CHARACTER_IDLE_IMAGE),
            "left": self.game.loader.loadTexture(CHARACTER_LEFT_IMAGE),
            "right": self.game.loader.loadTexture(CHARACTER_RIGHT_IMAGE),
        }
        self.node = self.game.sprite_factory.create_sprite(
            self.textures["idle"], PLAYER_START_X, PLAYER_START_Y, PLAYER_SCALE
        )
        self.reset()

    def reset(self):
        self.node.setPos(PLAYER_START_X, PLAYER_START_Y, 0)
        self.node.setTexture(self.textures["idle"])
        self.current_shot_interval = SHOT_INTERVAL
        self.current_shot_scale = SHOT_SCALE

    def update(self, dt):
        keys = self.game.input_handler.key_map
        dx = (keys["right"] - keys["left"]) * PLAYER_SPEED * dt
        new_x = self.node.getX() + dx
        self.node.setX(max(LEFT_BOUND, min(RIGHT_BOUND, new_x)))

    def update_texture(self):
        keys = self.game.input_handler.key_map
        if keys["left"]:
            self.node.setTexture(self.textures["left"])
        elif keys["right"]:
            self.node.setTexture(self.textures["right"])
        else:
            self.node.setTexture(self.textures["idle"])

    def apply_bonus_effect(self, value):
        t = (value - BONUS_MIN_VALUE) / (BONUS_MAX_VALUE - BONUS_MIN_VALUE)
        modifier = 0.5 + t * 1.5
        self.current_shot_interval = SHOT_INTERVAL / modifier
        self.current_shot_scale = SHOT_SCALE * modifier
        self.game.taskMgr.remove("autoShootTask")
        self.game.taskMgr.doMethodLater(
            self.current_shot_interval,
            self.game.task_manager._auto_shoot,
            "autoShootTask"
        )