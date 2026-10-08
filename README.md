Setup and run the project

On Windows, install uv from PowerShell if it is not already installed:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Add the folder containing uv.exe to PATH—not the uv.exe file itself.

Open PowerShell in the project directory and sync the locked dependencies. This creates or refreshes the Windows `.venv`; do not copy a virtual environment from WSL or create a second environment with `python -m venv`.

```powershell
uv sync
uv run python -c "import pygame; print(pygame.version.ver)"
uv run main.py
```

No manual activation is required when using `uv run`. In VS Code, the workspace is configured to use `.venv\Scripts\python.exe` so Pylance resolves the same installed packages.

For Linux or macOS, install uv with `curl -LsSf https://astral.sh/uv/install.sh | sh`, then run the same `uv sync` and `uv run` commands from the project directory.

Problem 1:
The triangle player moves as normal but leaves afterimages as it moves
The asteroids can touch the afterimage in the center where the player is at the beginning to end the game, even if the player has moved elsewhere
That is because the player hitbox won't move even if the player is moving.

Solution 1:
The collision check was constructing a new player every frame, adding more player sprites at the starting position.
It now checks collisions against the single player instance, so the hitbox follows the moving player and the extra trails should stop.
Create new Player object
player = Player(x, y)
Change collision check to use the Player object instead of creating a new one each time
if asteroid.collides_with(player):

Problem 2:
The weapon on the ship is overpowered as it spammed bullets

Solution 2:
Implement a shoot cooldown to limit fire rate to one shot every 0.3 seconds

In our game, bullets:
Are small circles
Move at a constant speed in a straight line
Split up asteroids when they collide with them
Are spawned by player input (spacebar) and move in the direction the player is facing

Ideas:
Add a scoring system
Implement multiple lives and respawning
Add an explosion effect for the asteroids
Add acceleration to the player movement
Make the objects wrap around the screen instead of disappearing
Add a background image
Create different weapon types
Make the asteroids lumpy instead of perfectly round
Make the ship have a triangular hit box instead of a circular one
Add a shield power-up
Add a speed power-up
Add bombs that can be dropped
Make asteroids bounce off each other