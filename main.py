#!/usr/bin/env python3
"""Punto de entrada del juego."""

from core.game_base import ShootingGame

if __name__ == "__main__":
    game = ShootingGame()
    game.run()