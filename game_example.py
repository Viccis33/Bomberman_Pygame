import pygame
from utils import Player, Map, Level, Bomb, Player_Bomb, Blop, Enemy
from gameplay import tick_and_explode_all_bombs, blit_background_under_entities, remove_dead_enemies, player_died

# pygame setup
pygame.init()
# screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
still_playing = True


level = Level(size=(21,15))
level.randomize()

m = level.map
m.reset(level.array)

player = Player(40, 40)
level.enemies = [Enemy(Blop(17*40,13*40)), Enemy(Blop(17*40,11*40))]
for enemy in level.enemies:
    level.array[enemy.entity.y//40][enemy.entity.x//40] = enemy
level.array[1][1] = player

while still_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False
            
    blit_background_under_entities(level,m,player)
    tick_and_explode_all_bombs(level,m)
    
    print(f'Player : '+ str(player.hp))
    for enemy in level.enemies:
        print(f'Enemy : '+ str(enemy.entity.hp))
    
    keys = pygame.key.get_pressed()
    player.move(keys, level.array)   
    player.put_bomb(keys, level)
    player.bomb_slots = max(player.bomb_slots, player.max_bomb_slots - len(level.bombs))
    if player.bomb_cooldown >0:
        player.bomb_cooldown -= 1 
    if player.damage_cooldown >0:
        player.damage_cooldown -= 1 
    
    for enemy in level.enemies:
        enemy.entity.move_random(level.array)    
        if enemy.entity.damage_cooldown >0:
            enemy.entity.damage_cooldown -= 1 
        
    remove_dead_enemies(level)
    
    if player.damage_cooldown%20<=10:
        m.screen.blit(player.img, player.pos)  
    for enemy in level.enemies:
        if enemy.entity.damage_cooldown%20<=10:
            m.screen.blit(enemy.entity.img, enemy.entity.pos)
        
    player_died(player, still_playing)
            
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()