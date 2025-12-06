from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from game_config import PLAYER_STARTING_LIFE

class UISystem:
    def __init__(self, game):
        self.game = game
        self._create_ui()

    def _create_ui(self):
        self.timer_text = self._text("Time: 0", (0.05, -0.08), align=TextNode.ALeft)
        self.win_text = self._text("Wins: 0", (-0.05, -0.08), align=TextNode.ARight)
        self.life_text = self._text(f"Life: {PLAYER_STARTING_LIFE}", (0.05, -0.16), align=TextNode.ALeft)
        self.status_text = self._text("", (0, 0), scale=0.1, fg=(1, 0, 0, 1))

    def _text(self, txt, pos, scale=0.08, fg=(1,1,1,1), align=TextNode.ACenter):
        parent = self.game.a2dTopLeft if align == TextNode.ALeft else self.game.a2dTopRight
        return OnscreenText(
            text=txt, pos=pos, scale=scale, fg=fg, align=align, parent=parent
        )

    def update_ui(self):
        elapsed = globalClock.getRealTime() - self.game.state.start_time
        self.timer_text.setText(f"Time: {elapsed:.1f}")

    def update_life_text(self, life):
        self.life_text.setText(f"Life: {life}")

    def show_win_message(self, stage):
        self.win_text.setText(f"Wins: {self.game.state.win_count}")
        self.status_text.setText(f"You Win! Stage {stage} starting soon...")

    def show_lose_message(self):
        self.status_text.setText("Game Over! Press Enter to restart.")

    def reset_ui(self):
        self.timer_text.setText("Time: 0")
        self.status_text.setText("")
        self.life_text.setText(f"Life: {PLAYER_STARTING_LIFE}")