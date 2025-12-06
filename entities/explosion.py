from game_config import EXPLOSION_DURATION, EXPLOSION_SPEED, PLAYER_START_Y, EXPLOSION_IMAGE, EXPLOSION_SCALE_MULTIPLIER

class Explosion:
    def __init__(self, game, x, y, scale):
        self.game = game
        self.node = self.game.sprite_factory.create_sprite(
            self.game.loader.loadTexture(EXPLOSION_IMAGE),
            x, y, scale
        )
        self.node.setPythonTag("speed", EXPLOSION_SPEED)
        self.start_time = globalClock.getFrameTime()
        self.duration = EXPLOSION_DURATION

    def update(self, dt):
        self.node.setY(self.node.getY() - EXPLOSION_SPEED * dt)
        elapsed = globalClock.getFrameTime() - self.start_time
        alive = elapsed < self.duration and self.node.getY() >= PLAYER_START_Y - 10
        if not alive:
            self.destroy()
        return alive

    def destroy(self):
        self.node.removeNode()