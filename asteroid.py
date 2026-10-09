import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    # Draw the asteroid on a given surface
    def draw(self, surface: pygame.Surface) -> None:
        """
            Override the draw() method to draw the asteroid using the pygame.draw.circle function. It accepts:
            - The "surface" to draw on (the screen object)
            - The color of the circle ("white")
            - Its own position as the center
            - Its own radius
            - The width of the line to draw the circle (use LINE_WIDTH from constants.py)
            """
        from constants import LINE_WIDTH
        pygame.draw.circle(
            surface,
            "white",
            (int(self.position.x), int(self.position.y)),
            int(self.radius),
            LINE_WIDTH,
        )

    # Override the update() method so that it moves in a straight line at constant speed.
    # On each frame, it should add (self.velocity * dt) to its position (get self.velocity from its parent class, CircleShape).
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        """
        Split the asteroid into two smaller asteroids if its radius is greater than ASTEROID_MIN_RADIUS.
        Otherwise, just destroy it.
        """
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        velocity1 = self.velocity.rotate(angle)
        velocity2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2