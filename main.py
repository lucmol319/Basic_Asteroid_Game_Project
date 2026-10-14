import pygame
import random
from constants import POWERUP_DROP_CHANCE, SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from powerup import PowerUp

# pygame.display.set_mode() -> set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print("Starting Asteroids")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Clock
    clock = pygame.time.Clock()
    dt = 0.0

    # Group for updatable and drawable objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    Player.containers = (updatable, drawable) # Player object is in the groups?
    Explosion.containers = (updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)

    # Create a new empty pygame.sprite.Group for the asteroids
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    # Set its static containers field to only the updatable group (it's not drawable, and it's not an asteroid itself)
    AsteroidField.containers = (updatable,)
    
    # After adding the container, create a new AsteroidField object
    AsteroidField()

    # Instantiate the player in the center of the screen
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y) # Player object

    score = 0
    spawn_position = pygame.Vector2(x, y)
    font = pygame.font.Font(None, 32)

    # Set up a new shots group in your main.py initialization code.
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    # Game loop
    while True:
        log_state() # Log the current state of the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                return
        
        updatable.update(dt) # Update all updatable objects based on the delta time

        for asteroid in list(asteroids):
            if (
                player.invulnerable_timer <= 0
                and player.collides_with(asteroid)
            ):
                shield_was_active = player.shield_active
                game_over = player.take_hit(spawn_position)
                if shield_was_active:
                    log_event("shield_blocked")
                else:
                    log_event("player_hit", lives=player.lives)
                if game_over:
                    print("Game over!")
                    return
                break

        for asteroid in list(asteroids):
            for shot in list(shots):
                if asteroid.collides_with(shot):
                    points = asteroid.score_value
                    score += points
                    log_event("asteroid_shot", points=points)
                    Explosion(
                        asteroid.position.x,
                        asteroid.position.y,
                        asteroid.radius,
                    )
                    if random.random() < POWERUP_DROP_CHANCE:
                        powerup_type = random.choice(
                            ("shield", "speed", "rapid_fire")
                        )
                        PowerUp(
                            asteroid.position.x,
                            asteroid.position.y,
                            powerup_type,
                        )
                    asteroid.split()
                    shot.kill()
                    break

        for powerup in list(powerups):
            if player.collides_with(powerup):
                player.collect_powerup(powerup.powerup_type)
                log_event("powerup_collected", powerup=powerup.powerup_type)
                powerup.kill()

        screen.fill("Black")
        for sprite in drawable:
            sprite.draw(screen)

        active_powerups = []
        if player.shield_active:
            active_powerups.append("Shield")
        if player.speed_powerup_timer > 0:
            active_powerups.append(f"Speed {player.speed_powerup_timer:.0f}s")
        if player.rapid_fire_timer > 0:
            active_powerups.append(f"Rapid Fire {player.rapid_fire_timer:.0f}s")
        status = "   ".join(active_powerups)
        hud = font.render(
            f"Score: {score}   Lives: {player.lives}   {status}",
            True,
            "white",
        )
        screen.blit(hud, (20, 20))
        pygame.display.flip()

        dt = clock.tick(60) / 1000.0

if __name__ == "__main__":
    main()