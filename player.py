"""
Player class for the game.
This module defines the Player class, which represents the player-controlled spaceship in the game."""
import pygame
from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_RADIUS, PLAYER_TURN_SPEED,
    PLAYER_SPEED, PLAYER_ACCELERATION, PLAYER_FRICTION, PLAYER_LIVES,
    PLAYER_RESPAWN_INVULNERABILITY_SECONDS, PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS
)

class Player(CircleShape):
    # Call the parent class's constructor, passing in x, y, and the PLAYER_RADIUS
    # Create a new variable in the Player constructor to act as a shot cooldown timer. It should start with a value of 0.
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0 # Create an attribute called rotation, initialized to 0.
        self.shoot_cooldown = 0 # Initialize the shot cooldown timer to 0.
        self.lives = PLAYER_LIVES
        self.invulnerable_timer = 0.0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # It takes one argument dt. Add PLAYER_TURN_SPEED * dt to the player's current rotation.
    def rotate(self, dt: float) -> None:
        # Update the player's rotation based on the turn speed and delta time
        self.rotation += PLAYER_TURN_SPEED * dt

    # Update the player's rotation based on input keys
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        thrust = 0

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_s]:
            thrust -= 1
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            thrust += 1

        if thrust:
            direction = pygame.Vector2(0, 1).rotate(self.rotation)
            self.velocity += direction * PLAYER_ACCELERATION * thrust * dt
            if self.velocity.length() > PLAYER_SPEED:
                self.velocity.scale_to_length(PLAYER_SPEED)
        else:
            self.velocity *= PLAYER_FRICTION ** dt
        
        # Handle the spacebar (pygame.K_SPACE) and call the shoot method when it's pressed
        # When the player tries to shoot:
        # If the current value of the timer is greater than 0, prevent the player from shooting.
        # Otherwise, set the timer equal to PLAYER_SHOOT_COOLDOWN_SECONDS.
        if keys[pygame.K_SPACE]:
            if self.shoot_cooldown <= 0:
                self.shoot()
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        super().update(dt) # Hook the update method into the game loop by calling it on the player object each frame before rendering.
        # Call the parent class's update method to ensure proper behavior.

        # Decrease the shoot cooldown timer by dt each frame
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 8) % 2 == 0:
            return
        super().draw(surface)

    def take_hit(self, spawn_position: pygame.Vector2) -> bool:
        self.lives -= 1
        if self.lives > 0:
            self.position = spawn_position.copy()
            self.velocity.update(0, 0)
            self.rotation = 0
            self.invulnerable_timer = PLAYER_RESPAWN_INVULNERABILITY_SECONDS
        return self.lives == 0

    def shoot(self) -> None:
        """
        This method takes no parameters and does the following:
        - Creates a new Shot at the current position of the player.
        - Sets the shot's .velocity attribute:
        - Start with a pygame.Vector2 of (0, 1).
        - .rotate() the vector in the direction the player is facing.
        - Scale it up (multiply by PLAYER_SHOOT_SPEED) to make it move faster.
        """
        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        shot.velocity = velocity
        return shot