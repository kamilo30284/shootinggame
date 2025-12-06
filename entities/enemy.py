from game_config import ENEMY_TYPES, ENEMY_SPAWN_PROB, PLAYER_START_Y, ENEMY_SPAWN_Y, LEFT_BOUND, RIGHT_BOUND
import random

class Enemy:
    def __init__(self, game, x, y, etype):
        config = ENEMY_TYPES[etype]
        self.game = game
        self.node = self.game.sprite_factory.create_sprite(
            self.game.loader.loadTexture(config["image"]),
            x, y, config["scale"]
        )
        self.node.setPythonTag("hp", config["hp"])
        self.node.setPythonTag("speed", config["speed"])
        self.etype = etype

    @classmethod
    def random_spawn(cls, game):
        etype = random.choices(list(ENEMY_TYPES.keys()), ENEMY_SPAWN_PROB)[0]
        x = random.uniform(LEFT_BOUND, RIGHT_BOUND)
        return cls(game, x, ENEMY_SPAWN_Y, etype)

    def update(self, dt):
        speed = self.node.getPythonTag("speed")
        self.node.setY(self.node.getY() - speed * dt)
        if self.node.getY() <= PLAYER_START_Y:
            if abs(self.node.getX() - self.game.player.node.getX()) < 1.0:
                self.game.state.take_damage()
                return False
            if self.node.getY() < PLAYER_START_Y:
                return False
        return True

    def destroy(self):
        self.node.removeNode()