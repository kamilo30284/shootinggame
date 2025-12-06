# core/input_handler.py
class InputHandler:
    def __init__(self, game):
        self.game = game
        self.key_map = {"left": False, "right": False}

    def bind_inputs(self):
        self.game.accept("arrow_left", self.set_key, ["left", True])
        self.game.accept("arrow_left-up", self.set_key, ["left", False])
        self.game.accept("arrow_right", self.set_key, ["right", True])
        self.game.accept("arrow_right-up", self.set_key, ["right", False])
        self.game.accept("enter", self.game.task_manager.restart_game)
        self.game.accept("escape", self.game.userExit)

    def set_key(self, key, value):
        self.key_map[key] = value
        self.game.player.update_texture()