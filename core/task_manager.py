from game_config import (
    SHOT_INTERVAL, ENEMY_SPAWN_INTERVAL, BONUS_SPAWN_INTERVAL,
    PLAYER_START_X, PLAYER_START_Y, ENEMY_SPAWN_Y, BONUS_SPAWN_POSITIONS
)
from entities.shot import Shot
from entities.enemy import Enemy
from entities.bonus import Bonus
import random

class TaskManager:
    def __init__(self, game):
        self.game = game
        self.shots = []
        self.enemies = []
        self.bonuses = []
        self.explosions = []
        self._schedule_tasks()

    def _schedule_tasks(self):
        self.game.taskMgr.doMethodLater(SHOT_INTERVAL, self._auto_shoot, "autoShootTask")
        self.game.taskMgr.doMethodLater(ENEMY_SPAWN_INTERVAL, self._spawn_enemy, "spawnEnemyTask")
        self.game.taskMgr.doMethodLater(BONUS_SPAWN_INTERVAL, self._spawn_bonus, "spawnBonusTask")

    def _auto_shoot(self, task):
        if not self.game.state.game_over:
            shot = Shot(
                self.game,
                self.game.player.node.getX(),
                self.game.player.node.getY(),
                self.game.player.current_shot_scale
            )
            self.shots.append(shot)
        return task.again

    def _spawn_enemy(self, task):
        if self.game.state.game_over:
            return task.done
        enemy = Enemy.random_spawn(self.game)
        self.enemies.append(enemy)
        return task.again

    def _spawn_bonus(self, task):
        if self.game.state.game_over:
            return task.done
        x = random.choice(BONUS_SPAWN_POSITIONS)
        bonus = Bonus(self.game, x, ENEMY_SPAWN_Y)
        self.bonuses.append(bonus)
        return task.again

    def update_entities(self, dt):
        for shot in self.shots[:]:
            if not shot.update(dt):
                self._remove(shot, self.shots)
        for enemy in self.enemies[:]:
            if not enemy.update(dt):
                self._remove(enemy, self.enemies)
        for bonus in self.bonuses[:]:
            if not bonus.update(dt):
                self._remove(bonus, self.bonuses)
        for explosion in self.explosions[:]:
            if not explosion.update(dt):
                self._remove(explosion, self.explosions)

    def check_collisions(self):
        from systems.collision_system import CollisionSystem
        CollisionSystem.check(self)

    def _remove(self, obj, container):
        if obj in container:
            obj.destroy()
            container.remove(obj)

    def add_explosion(self, explosion):
        self.explosions.append(explosion)

    def restart_game(self):
        for container in [self.shots, self.enemies, self.bonuses, self.explosions]:
            for obj in container[:]:
                self._remove(obj, container)
        self.game.state.reset()
        self.game.player.reset()
        self.game.taskMgr.remove("autoShootTask")
        self.game.taskMgr.remove("spawnEnemyTask")
        self.game.taskMgr.remove("spawnBonusTask")
        self._schedule_tasks()
        self.game.ui_system.reset_ui()