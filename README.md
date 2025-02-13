<h1>Bomberman</h1>
Hi everyone, in this repo you will find a bomberman game using pygame.<br/>

<h3>Here is a quick summary of the files:</h3>
<ul>
    <li>open_screen.py launches level selection</li>
    <li>levels are stored in data/levels.json</li>
    <li>utils.py contains the different classes such as player, enemy, level, map, blocks</li>
    <li>gameplay.py contains essential functions that are called a lot when playing</li>
    <li>play_level.py contains the fundamental logic of the game</li>
    <li>an example of a game is available on game_example.py</li>
</ul>

<h3>There are some fixes that can be addressed, notably:</h3>
    <li>A fixed window size for the level selection screen so it doesn't change after a level completion.</li>
    <li>Prohibition of destroyable blocks on enemy spawn cells</li>
    <li>Fix the animation of explosion</li>
    <li>Comments in the code :D</li>

<h3>Coming up features:</h3>
    <li>Different possibilities to end a level:<ul>
        <li>Activating Prysms in a delimited time</li>
        <li>Attaining a cell</li>
        </ul>
    </li>
    <li>Monsters respawning</li>
    <li>New monsters and with different mechanics and AI</li>
    <li>BGM and SFX</li>
    <li>Destroyable blocks in the levels metadata (not randomized)</li>
    <li>Non-rectangle maps</li>
    <li>Upgrades of the player depending on loot</li>
    <li>Local multiplayer mode with an online mode later</li>

nice journey
