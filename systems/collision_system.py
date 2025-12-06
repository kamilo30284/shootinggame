from game_config import EXPLOSION_SCALE_MULTIPLIER

class CollisionSystem:
    @staticmethod
    def check(task_manager):
        for shot in task_manager.shots[:]:
            shot_pos = shot.node.getPos()
            shot_hit = False

            # Colisión con enemigos
            for enemy in task_manager.enemies[:]:
                if (shot_pos - enemy.node.getPos()).length() < 0.55:
                    hp = enemy.node.getPythonTag("hp") - 1
                    enemy.node.setPythonTag("hp", hp)
                    shot.destroy()
                    task_manager.shots.remove(shot)
                    shot_hit = True

                    if hp <= 0:
                        scale = enemy.node.getScale().x
                        from entities.explosion import Explosion
                        explosion = Explosion(
                            task_manager.game,
                            enemy.node.getX(),
                            enemy.node.getY(),
                            scale * EXPLOSION_SCALE_MULTIPLIER
                        )
                        task_manager.add_explosion(explosion)
                        enemy.destroy()
                        task_manager.enemies.remove(enemy)
                    break

            if shot_hit:
                continue

            # Colisión con bonus
            for bonus in task_manager.bonuses[:]:
                if (shot_pos - bonus.node.getPos()).length() < 2.0:
                    bonus.upgrade()
                    shot.destroy()
                    task_manager.shots.remove(shot)
                    break