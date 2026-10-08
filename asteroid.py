import pygame
from circleshape import CircleShape

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