"""
Explosion effect for the game.
This module defines the Explosion class, which represents an explosion effect in the game.
"""
import random
import pygame

class Explosion(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.AbstractGroup, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(*self.containers)
        self.duration = 0.5
        self.lifetime = self.duration
        self.particles: list[tuple[pygame.Vector2, pygame.Vector2]] = []
        self.particle_radius = max(2, int(radius / 10))

        for _ in range(12):
            direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
            speed = random.uniform(radius * 1.5, radius * 4)
            self.particles.append(
                (pygame.Vector2(x, y), direction * speed)
            )

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return

        for position, velocity in self.particles:
            position += velocity * dt
            velocity *= max(0, 1 - dt * 2)

    def draw(self, surface: pygame.Surface) -> None:
        progress = self.lifetime / self.duration
        color = (255, int(80 + 150 * progress), int(30 + 20 * progress))
        particle_radius = max(1, int(self.particle_radius * progress))

        for position, _ in self.particles:
            pygame.draw.circle(
                surface,
                color,
                (int(position.x), int(position.y)),
                particle_radius,
            )
