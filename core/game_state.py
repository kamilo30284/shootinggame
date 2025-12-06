from game_config import GAME_DURATION, PLAYER_STARTING_LIFE

class GameState:
    def __init__(self, game):
        self.game = game
        self.reset()

    def reset(self):
        self.game_over = False
        self.last_win = None
        self.start_time = globalClock.getRealTime()
        self.player_life = PLAYER_STARTING_LIFE
        self.win_count = 0
        self.stage = 1

    def take_damage(self):
        self.player_life -= 1
        self.game.ui_system.update_life_text(self.player_life)
        self.game.effect_system.start_screen_shake()
        self.game.effect_system.show_red_filter()
        if self.player_life <= 0:
            self.end_game(win=False)

    def end_game(self, win):
        self.game_over = True
        self.last_win = win
        if win:
            self.win_count += 1
            self.stage += 1
            self.game.ui_system.show_win_message(self.stage)
            self.game.taskMgr.doMethodLater(3.0, self._auto_restart, "auto_restart")
        else:
            self.stage = 1
            self.game.ui_system.show_lose_message()

    def _auto_restart(self, task):
        self.game.task_manager.restart_game()
        return task.done

    def check_end_conditions(self):
        elapsed = globalClock.getRealTime() - self.start_time
        if elapsed >= GAME_DURATION:
            self.end_game(win=True)
        elif self.player_life <= 0:
            self.end_game(win=False)