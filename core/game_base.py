from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, CardMaker, TransparencyAttrib
from game_config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    BACKGROUND_IMAGE, BACKGROUND_POS_X, BACKGROUND_POS_Y, BACKGROUND_SCALE
)
from core.game_state import GameState
from core.input_handler import InputHandler
from core.task_manager import TaskManager
from entities.player import Player
from systems.camera_system import CameraSystem
from systems.effect_system import EffectSystem
from systems.ui_system import UISystem
from utils.sprite_factory import SpriteFactory

class ShootingGame(ShowBase):
    def __init__(self):
        loadPrcFileData("", f"win-size {WINDOW_WIDTH} {WINDOW_HEIGHT}")
        loadPrcFileData("", f"window-title {WINDOW_TITLE}")
        loadPrcFileData("", "win-fixed-size 1")
        ShowBase.__init__(self)
        self.disableMouse()

        # ✅ Crear fondo ANTES que cualquier otra cosa (para que quede atrás)
        self._create_background()

        self.state = GameState(self)
        self.input_handler = InputHandler(self)
        self.sprite_factory = SpriteFactory(self)
        self.player = Player(self)
        self.camera_system = CameraSystem(self)
        self.effect_system = EffectSystem(self)
        self.ui_system = UISystem(self)
        self.task_manager = TaskManager(self)

        self.taskMgr.add(self.update, "update")
        self.input_handler.bind_inputs()

    def _create_background(self):
        bg_tex = self.loader.loadTexture(BACKGROUND_IMAGE)
        cm = CardMaker("background")
        cm.setFrame(-1, 1, -1, 1)
        self.background = self.render.attachNewNode(cm.generate())
        self.background.setTexture(bg_tex)
        self.background.setPos(BACKGROUND_POS_X, BACKGROUND_POS_Y, 0)
        self.background.setScale(BACKGROUND_SCALE)
        self.background.setBin("background", 0)
        self.background.setDepthTest(False)
        self.background.setDepthWrite(False)

    def update(self, task):
        if not self.state.game_over:
            dt = globalClock.getDt()
            self.player.update(dt)
            self.camera_system.update()
            self.task_manager.update_entities(dt)
            self.task_manager.check_collisions()
            self.ui_system.update_ui()
            self.state.check_end_conditions()
        return task.cont