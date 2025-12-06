from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

from game_config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
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
        # Configuración de ventana
        loadPrcFileData("", f"win-size {WINDOW_WIDTH} {WINDOW_HEIGHT}")
        loadPrcFileData("", f"window-title {WINDOW_TITLE}")
        loadPrcFileData("", "win-fixed-size 1")
        
        ShowBase.__init__(self)
        self.disableMouse()

        # Sistemas y entidades (inversión de dependencias: los sistemas reciben referencias)
        self.state = GameState(self)
        self.input_handler = InputHandler(self)
        self.sprite_factory = SpriteFactory(self)
        self.player = Player(self)
        self.camera_system = CameraSystem(self)
        self.effect_system = EffectSystem(self)
        self.ui_system = UISystem(self)
        self.task_manager = TaskManager(self)

        # Iniciar
        self.taskMgr.add(self.update, "update")
        self.input_handler.bind_inputs()

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