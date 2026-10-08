import pygame
from constants import LINE_WIDTH

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        """
        To draw the player, override the draw method of CircleShape.
        Call pygame.draw.polygon(). It takes as inputs:
        The screen object
        A color (use "white")
        A list of points (use the list returned by a call to the self.triangle() function)
        A line width (use the one in your constants.py file)
        """
        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            self.triangle(),
            LINE_WIDTH
        )

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        # pass

    # Check for collisions. It should take another circle shape as a parameter (aside from self of course) and return True or False.
    def collides_with(self, other: "CircleShape") -> bool:
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)