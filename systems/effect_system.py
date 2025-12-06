from panda3d.core import CardMaker, TransparencyAttrib, LVecBase4f
from game_config import (
    SHAKE_INTENSITY, SHAKE_DURATION,
    RED_FILTER_INTENSITY, RED_FILTER_DURATION
)
import random

class EffectSystem:
    def __init__(self, game):
        self.game = game
        self.red_filter = self._create_red_filter()
        self.red_filter.setAlphaScale(0.0)

    def _create_red_filter(self):
        cm = CardMaker("red_filter")
        cm.setFrameFullscreenQuad()
        node = self.game.render2d.attachNewNode(cm.generate())
        node.setColor(LVecBase4f(1, 0, 0, RED_FILTER_INTENSITY))
        node.setTransparency(TransparencyAttrib.MAlpha)
        return node

    def start_screen_shake(self):
        self.shake_start = globalClock.getFrameTime()
        self.game.taskMgr.add(self._shake_task, "shakeTask")

    def _shake_task(self, task):
        elapsed = globalClock.getFrameTime() - self.shake_start
        if elapsed >= SHAKE_DURATION:
            self.game.camera.setPos(self.game.camera_system.original_pos)
            return task.done
        decay = 1.0 - (elapsed / SHAKE_DURATION)
        intensity = SHAKE_INTENSITY * decay
        offset = (random.uniform(-intensity, intensity),
                  random.uniform(-intensity, intensity),
                  0)
        self.game.camera.setPos(self.game.camera_system.original_pos + offset)
        return task.cont

    def show_red_filter(self):
        self.red_filter.setAlphaScale(RED_FILTER_INTENSITY)
        self.game.taskMgr.doMethodLater(
            RED_FILTER_DURATION,
            self._hide_red_filter,
            "hideRedFilter"
        )

    def _hide_red_filter(self, task):
        self.red_filter.setAlphaScale(0.0)
        return task.done