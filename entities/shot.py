from game_config import SHOT_SPEED, ENEMY_SPAWN_Y, SHOT_IMAGE

class Shot:
    def __init__(self, game, x, y, scale):
        self.game = game
        self.node = self.game.sprite_factory.create_sprite(
            self.game.loader.loadTexture(SHOT_IMAGE),
            x, y, scale
        )

    def update(self, dt):
        self.node.setY(self.node.getY() + SHOT_SPEED * dt)
        return self.node.getY() <= ENEMY_SPAWN_Y + 5

    def destroy(self):
        self.node.removeNode()