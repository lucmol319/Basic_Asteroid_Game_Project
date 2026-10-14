"""
This module defines the Shot class, which represents a shot fired by the player in the game.
The Shot class inherits from the CircleShape class and is responsible for updating its
position based on its velocity and drawing itself on the screen."""
import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, SHOT_RADIUS)

    # Override its draw and update methods, just like you did in the Asteroid class.
    def update(self, dt: float) -> None:
        # Implement the logic to update the shot's position based on its velocity and the delta time
        self.position += self.velocity * dt
        if self.is_off_screen():
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.position.x), int(self.position.y)),
            self.radius,
            0
        )