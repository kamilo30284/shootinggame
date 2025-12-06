from panda3d.core import CardMaker, TransparencyAttrib

class SpriteFactory:
    def __init__(self, game):
        self.game = game

    def create_sprite(self, texture, x, y, scale=1.0, transparency=1.0):
        cm = CardMaker("sprite")
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        node = self.game.render.attachNewNode(cm.generate())
        node.setTexture(texture)
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setAlphaScale(transparency)
        node.setBillboardPointEye()
        node.setScale(scale)
        node.setPos(x, y, 0)
        return node