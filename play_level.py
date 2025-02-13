import pygame
from utils import Player, Map, Level, Bomb, Player_Bomb, Blop, Enemy
from gameplay import tick_and_explode_all_bombs, blit_background_under_entities, remove_dead_enemies, player_died, generate_level, game_won
from screen_misc import start_pause, game_over_screen, game_won_screen

def play_level(level_data):

    clock = pygame.time.Clock()
    still_playing = True
    on_pause = False

    level = generate_level(level_data)

    m = level.map
    m.reset(level.array)

    player = Player(40, 40)
    
    level.array[1][1] = player

    while still_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                still_playing = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    on_pause = not on_pause
                    if on_pause == False:
                        m.reset(level.array)
            
        if on_pause:
            start_pause(m)
        else:
                
            blit_background_under_entities(level,m,player)
            tick_and_explode_all_bombs(level,m)
            

            
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
                
            still_playing = player_died(player, still_playing)
            if level.finished:
                still_playing = False
                
            game_won(player,level)
        pygame.display.update()

        clock.tick(60)  # limits FPS to 60

    go_to_main_menu = False

    if not level.finished:
        while not go_to_main_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
            go_to_main_menu = game_over_screen(m)
            pygame.display.update()

            clock.tick(60)
        return False
            
            
    else:
        while not go_to_main_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
            go_to_main_menu = game_won_screen(m)
            pygame.display.update()

            clock.tick(60)
        return True