from game_config import (
    BONUS_STARTING_VALUE, BONUS_SCALE, BONUS_SPEED, BONUS_TRANSPARENCY,
    BONUS_MAX_VALUE, RIGHT_BOUND, LEFT_BOUND,
    BONUS_POSITIVE_IMAGE, BONUS_NEGATIVE_IMAGE,
    PLAYER_START_Y
)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

class Bonus:
    def __init__(self, game, x, y, value=BONUS_STARTING_VALUE):
        self.game = game
        self.value = value
        texture = (
            self.game.loader.loadTexture(BONUS_POSITIVE_IMAGE)
            if value >= 0 else
            self.game.loader.loadTexture(BONUS_NEGATIVE_IMAGE)
        )
        horiz_scale = RIGHT_BOUND - LEFT_BOUND
        self.node = self.game.sprite_factory.create_sprite(
            texture, x, y, BONUS_SCALE, BONUS_TRANSPARENCY
        )
        self.node.setScale(horiz_scale, BONUS_SCALE, BONUS_SCALE)
        self.node.setPythonTag("speed", BONUS_SPEED)

        self.text = OnscreenText(
            text=str(value),
            scale=0.2,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            mayChange=True,
            parent=self.node
        )
        self.text.setPos(0, -0.06)
        self.text.setBin('fixed', 1)
        self.text.setDepthTest(False)
        self.text.setDepthWrite(False)

    def update(self, dt):
        self.node.setY(self.node.getY() - BONUS_SPEED * dt)
        y = self.node.getY()
        if y <= PLAYER_START_Y:
            if abs(self.node.getX() - self.game.player.node.getX()) < 1.0:
                self.game.player.apply_bonus_effect(self.value)
            self.destroy()
            return False
        return y >= PLAYER_START_Y - 10

    def upgrade(self):
        self.value = min(self.value + 1, BONUS_MAX_VALUE)
        tex = (
            self.game.loader.loadTexture(BONUS_POSITIVE_IMAGE)
            if self.value >= 0 else
            self.game.loader.loadTexture(BONUS_NEGATIVE_IMAGE)
        )
        self.node.setTexture(tex)
        self.text.setText(str(self.value))

    def destroy(self):
        if self.text:
            self.text.destroy()
        self.node.removeNode()