import pygame
from utils import Player, Player_Bomb, Enemy, Level, Blop, Map, Hard_block, Destroyable_block

def tick_and_explode_all_bombs(level, m):
    for bomb in level.bombs:
        if bomb.tick<bomb.timer1:
            m.screen.blit(bomb.img,(bomb.x,bomb.y))
        else:
            if not bomb.exploded:
                bomb.explode(level)
            for deflagration in bomb.explosion:
                m.screen.blit(deflagration[0],(deflagration[1]*40,deflagration[2]*40))
                
        bomb.tick+=1
        if bomb.tick >= bomb.timer2:
            for deflagration in bomb.explosion:
                m.screen.blit(m.bg,(deflagration[1]*40,deflagration[2]*40))
            for block in bomb.destroyed_blocks:
                level.array[block[0]][block[1]] = None
            level.array[bomb.y//40][bomb.x//40] = None
            level.bombs.remove(bomb)
            
def blit_background_under_entities(level,m,player):
    close_cells_player = [((player.x//40 + i)*40, (player.y//40+ j)*40) for i in range(-1,2) for j in range(-1,2) if i == 0 or j==0]
    for cell in close_cells_player:
        if level.array[cell[1]//40][cell[0]//40] is None or isinstance(level.array[cell[1]//40][cell[0]//40], Player):
            m.screen.blit(m.bg,cell)
        if isinstance(level.array[cell[1]//40][cell[0]//40], Player_Bomb):
            new_bomb = level.array[cell[1]//40][cell[0]//40].bomb
            m.screen.blit(m.bg,cell)
            m.screen.blit(new_bomb.img,cell)
            
    close_cells_enemies = [((enemy.entity.x//40 + i)*40, (enemy.entity.y//40+ j)*40) for enemy in level.enemies for i in range(-1,2) for j in range(-1,2) if i == 0 or j==0]
    for cell in close_cells_enemies:
        if level.array[cell[1]//40][cell[0]//40] is None or isinstance(level.array[cell[1]//40][cell[0]//40], Enemy):
            m.screen.blit(m.bg,cell)
            
def remove_dead_enemies(level):
    for enemy in level.enemies:
        entity = enemy.entity
        if entity.hp<=0:
            level.array[entity.y//40][entity.x//40] = None
            level.enemies.remove(enemy)
            
def player_died(player,still_playing):
    if player.hp <=0:
        return False
    return True

# def game_over(still_playing):
#     return False

def game_won(player,level):
    if level.win_condition == "enemies":
        if len(level.enemies) == 0:
            level.finished = True
    else:
        j,i = level.win_condition
        if player.y//40 == j and player.x//40 == i:
            level.finished = True

def generate_level(level_data, randomize_if_no_array = True):
    
    
    resolution = level_data["resolution"]
    win_condition = level_data["win_condition"]
    
    enemies = []
    for enemy in level_data["enemies"]:
        if enemy["name"] == "Blop":
            enemies.append(Enemy(Blop(enemy["x"], enemy["y"]))) 
    
    
    prysms = []
    for prysm in level_data["prysms"]:
        if prysm["name"] == "normal":
            prysms.append(Enemy(Blop(prysm["x"], prysm["y"]))) 
    
        
    array = level_data["array"] 
    if array is not None:
        for cell in array:
            if cell == "hard_block":
                cell = Hard_block()
            elif cell == "destroyable_block":
                cell = Destroyable_block()
        
        for enemy in enemies:
            array[enemy.y][enemy.x] = enemy
        
        for prysm in prysms:
            array[prysm.y][prysm.x] = prysm
            
    if len(enemies) ==0:
        enemies = None
    if len(prysms) ==0:
        prysms = None
        
    if resolution is None:
        resolution = (1280,720)
    level_map = Map(array= array,resolution=resolution)
    level_size = (resolution[0]//40,resolution[1]//40)
    level = Level(map=level_map,enemies = enemies, prysms=prysms, size=level_size)
    if randomize_if_no_array and array is None:
        level.randomize()
    return level
    