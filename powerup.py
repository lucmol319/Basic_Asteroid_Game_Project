"""
This module defines the PowerUp class, which represents a power-up item in the game.
Power-ups can be collected by the player to gain temporary abilities or enhancements."""
import pygame
from typing import Literal
from circleshape import CircleShape
from constants import POWERUP_LIFETIME_SECONDS

PowerUpType = Literal["shield", "speed", "rapid_fire"]

POWERUP_COLORS = {
    "shield": (80, 180, 255),
    "speed": (80, 255, 120),
    "rapid_fire": (255, 220, 70),
}
POWERUP_SYMBOLS = {
    "shield": "S",
    "speed": "+",
    "rapid_fire": "R",
}


class PowerUp(CircleShape):
    """
    PowerUp class for the game.
    This class represents a power-up item that can be collected by the player to gain temporary abilities or enhancements.
    """
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, powerup_type: PowerUpType) -> None:
        super().__init__(x, y, 14)
        self.powerup_type = powerup_type
        self.lifetime = POWERUP_LIFETIME_SECONDS
        self.font = pygame.font.Font(None, 20)

    def update(self, dt: float) -> None:
        super().update(dt)
        self.lifetime -= dt
        if self.lifetime <= 0 or self.is_off_screen():
            self.kill()

    def draw(self, surface: pygame.Surface) -> None:
        color = POWERUP_COLORS[self.powerup_type]
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, color, center, int(self.radius), 2)
        symbol = self.font.render(
            POWERUP_SYMBOLS[self.powerup_type], True, color
        )
        surface.blit(symbol, symbol.get_rect(center=center))
