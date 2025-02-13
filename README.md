                            -----   Bomberman   -----

Hi everyone, in this repo you will find a bomberman game using pygame.

Here is a quick summary of the files:

    open_screen.py launches level selection

    levels are stored in data/levels.json

    utils.py contains the different classes such as player, enemy, level, map, blocks

    gameplay.py contains essential functions that are called a lot when playing

    play_level.py contains the fundamental logic of the game

    an example of a game is available on game_example.py


There are some fixes that can be addressed, notably:
    _ A fixed window size for the level selection screen so it doesn't change after a level completion.
    _ Prohibition of destroyable blocks on enemy spawn cells
    _ Fix the animation of explosion
    _ Comments in the code :D

Coming up features:
    _ Different possibilities to end a level:
        _ Activating Prysms in a delimited time
        _ Attaining a cell
    _ Monsters respawning
    _ New monsters and with different mechanics and AI
    _ BGM and SFX
    _ Destroyable blocks in the levels metadata (not randomized)
    _ Non-rectangle maps
    _ Upgrades of the player depending on loot
    _ Local multiplayer mode with an online mode later

nice journey