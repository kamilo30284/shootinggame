from game_config import PLAYER_START_Y, CAMERA_DISTANCE, CAMERA_HEIGHT, CAMERA_LOOK_AT_OFFSET

class CameraSystem:
    def __init__(self, game):
        self.game = game
        self.original_pos = None
        self.update()

    def update(self):
        player_x = self.game.player.node.getX()
        self.game.camera.setPos(
            player_x,
            PLAYER_START_Y - CAMERA_DISTANCE,
            CAMERA_HEIGHT
        )
        self.game.camera.lookAt(
            player_x,
            PLAYER_START_Y + CAMERA_LOOK_AT_OFFSET,
            0
        )
        self.original_pos = self.game.camera.getPos()