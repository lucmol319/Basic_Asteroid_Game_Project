import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

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
    Player.containers = (updatable, drawable) # Player object is in the groups?

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
        
        screen.fill("Black")
        updatable.update(dt) # Update all updatable objects based on the delta time
        # Otherwise we would have to manually update each updatable object individually

        # Draw all drawable objects on the screen
        for sprite in drawable:
            sprite.draw(screen) # re-render each drawable object individually
        pygame.display.flip()
        
        dt = clock.tick(60) / 1000.0

        """
        Iterate over all the objects in your asteroids group.
        Check if any of them collide with the player. If a collision is detected:
        Call log_event("player_hit").
        Print Game over! to the console.
        End the game immediately with sys.exit().
        """
        for asteroid in asteroids:
            if asteroid.collides_with(player): # Check if the asteroid collides with the player
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Add another collision check to the game loop. Loop over each asteroid, and for each asteroid, loop over each shot.
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

if __name__ == "__main__":
    main()