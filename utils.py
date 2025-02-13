import pygame
import random
from os import listdir
from os.path import join, isfile


def number_sign(number):
    if number >0: return 1
    elif number == 0: return 0
    return -1

class Player():
    def __init__(self, pos_x, pos_y, img_path = "img/roublard_creature.png", bomb_slots = 6, hp=3, speed=5) -> None:
        self.x = pos_x
        self.y = pos_y
        self.pos = (self.x,self.y)
        
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (40, 40))
        
        self.speed = speed
        self.x_vel = 0
        self.y_vel = 0
        self.move_timer = 0
        self.bomb_cooldown = 0
        self.damage_cooldown = 0
        
        self.hp = hp
        self.max_bomb_slots = bomb_slots
        self.bomb_slots = bomb_slots
        
    
    def move(self, keys_pressed, level_array):
        #check if the player is already moving
        if self.move_timer >0:
            if self.move_timer<1+40//self.speed:
                self.x += self.x_vel
                self.y += self.y_vel
                self.move_timer +=1
                self.pos = (self.x,self.y)
                
            if self.move_timer == 1+40//self.speed:
                last_array_y = (self.y//40 - number_sign(self.y_vel))
                last_array_x = (self.x//40 - number_sign(self.x_vel))
                if isinstance(level_array[last_array_y][last_array_x],Player):
                    level_array[last_array_y][last_array_x] = None
                elif isinstance(level_array[last_array_y][last_array_x],Player_Bomb):
                    level_array[last_array_y][last_array_x] = level_array[last_array_y][last_array_x].bomb
                level_array[self.y//40][self.x//40] = self
                self.move_timer = 0
                self.x_vel = 0
                self.y_vel = 0
                
        else:
            if keys_pressed[pygame.K_z]:
                if level_array[self.y//40-1][self.x//40] is None:
                    self.y_vel = -self.speed
                    self.move_timer +=1
            elif keys_pressed[pygame.K_s]:
                if level_array[self.y//40+1][self.x//40] is None:
                    self.y_vel = +self.speed
                    self.move_timer +=1
            elif keys_pressed[pygame.K_d]:
                if level_array[self.y//40][self.x//40+1] is None:
                    self.x_vel = +self.speed
                    self.move_timer +=1
            elif keys_pressed[pygame.K_q]:
                if level_array[self.y//40][self.x//40-1] is None:
                    self.x_vel = -self.speed
                    self.move_timer +=1
                
    def put_bomb(self, keys_pressed, level):
        if  keys_pressed[pygame.K_SPACE] and self.bomb_slots >0 and not isinstance(level.array[self.y//40][self.x//40], Bomb) and self.bomb_cooldown==0:
            self.bomb_cooldown = 8
            self.bomb_slots -=1
            new_bomb = Bomb(self.x//40*40, self.y//40*40)
            level.array[self.y//40][self.x//40] = Player_Bomb(self,new_bomb)
            level.bombs.append(new_bomb)
            

class Map():
    def __init__(self, background_path = 'img/gazon.png', array = None, resolution = (1280, 720)) -> None:
        
        self.array = array
        if self.array is not None:
            self.res = (len(array[0]*40, len(array*40)))
        else:
            self.res = resolution
        
        self.screen = pygame.display.set_mode(resolution)
        self.bg = pygame.image.load(background_path).convert()
        self.bg = pygame.transform.scale(self.bg, (40, 40))
        self.size = (self.res[0]//40, self.res[1]//40)
        
    def reset(self, objects):
        for i in range(self.res[0]//40):
            for j in range(self.res[1]//40):
                if objects[j][i] is None:
                    self.screen.blit(self.bg, (40*i, 40*j))
                else:
                    self.screen.blit(self.bg, (40*i, 40*j))
                    self.screen.blit(objects[j][i].img, (40*i, 40*j))
        
                
class Hard_block():
    def __init__(self,image_path = "img/indestructible.png") -> None:
            
        self.img = pygame.image.load(image_path).convert()
        self.img = pygame.transform.scale(self.img, (40, 40))
        
class Destroyable_block():
    def __init__(self,image_path = "img/destructible_1.png", def_image_path = "img/destructible_def_1.png") -> None:
            
        self.img = pygame.image.load(image_path).convert()
        self.img = pygame.transform.scale(self.img, (40, 40))
        self.img_destroyed = pygame.image.load(def_image_path).convert()
        self.img_destroyed = pygame.transform.scale(self.img_destroyed, (40, 40))
        
class Level():
    def __init__(self, map = None, enemies = None, prysms = None, size = (32,18), win_condition = "enemies") -> None:
            
        if map is None:
            self.size = size
            self.map = Map(resolution= (size[0]*40, size[1]*40))
            self.array = []
            for j in range(size[1]):
                self.array.append([None]*size[0])
            
            for j in range(size[1]):
                for i in range(size[0]):
                    if i == 0 or j == 0 or i == size[0]-1 or j == size[1] - 1 or (i%2 == 0 and j%2 ==0):
                        self.array[j][i]= Hard_block()
            
        else:
            self.map = map
            self.size = self.map.size
            if map.array is not None:
                self.array = map.array
            else:
                self.array = []
                for j in range(size[1]):
                    self.array.append([None]*size[0])
                
                for j in range(size[1]):
                    for i in range(size[0]):
                        if i == 0 or j == 0 or i == size[0]-1 or j == size[1] - 1 or (i%2 == 0 and j%2 ==0):
                            self.array[j][i]= Hard_block()
        
        
        
        self.bombs = []
        if enemies is None:
            self.enemies = []
        else : 
            self.enemies = enemies
        if prysms is None:
            self.prysms = []
        else : 
            self.prysms = prysms
        
        
        self.finished = False
        self.win_condition = win_condition
                    
    def randomize(self):
        for k in range(self.size[0]*self.size[1]//5):
            i = random.randint(1,self.size[0]-1)
            j = random.randint(1,self.size[1]-1)
            if self.array[j][i] == None:
                self.array[j][i] = Destroyable_block()
                

class Bomb():
    def __init__(self,pos_x, pos_y, img_path = 'img/bomb_1.png', deflagration_imgs = 'img/deflagration_1/', size = 3, damage = 2, timer1 = 180, timer2= 240) -> None:
        self.x = pos_x
        self.y = pos_y
        self.tick = 0
        self.timer1 = timer1
        self.timer2 = timer2
        self.size = size
        self.damage = damage
        self.exploded = False
        
        self.explosion = []
        self.destroyed_blocks = []
        
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (40, 40))
        deflagration_paths = [join(deflagration_imgs, f) for f in listdir(deflagration_imgs) if isfile(join(deflagration_imgs, f))]
        self.def_img = {}
        for dp in deflagration_paths:
            self.def_img[dp[len(deflagration_imgs):len(dp)-4]] = pygame.transform.scale(pygame.image.load(dp).convert_alpha(), (40, 40))
             
    def explode(self, level):
        self.exploded = True
        level_array = level.array
        destroyed = []
        explosion = []
        explosion.append((self.def_img['Centre'],self.x//40, self.y//40))
        
        y = self.y//40
        x = self.x//40
        
        if isinstance(level_array[y][x], Player_Bomb):
            if level_array[y][x].player.damage_cooldown==0:
                level_array[y][x].player.hp -= self.damage
                level_array[y][x].player.damage_cooldown = 120
        
        
        #haut
        direction = self.def_img['Vertical']
        k = 0
        while k<self.size:
            k+=1
            if k == self.size:
                direction = self.def_img['Haut']

                
            if isinstance(level_array[y-k][x], Destroyable_block):
                explosion.append((level_array[y-k][x].img_destroyed,x, y-k))
                destroyed.append((y-k,x))
                k+= self.size
                
            elif isinstance(level_array[y-k][x], Player):
                if level_array[y-k][x].damage_cooldown==0:
                    level_array[y-k][x].hp -= self.damage
                    level_array[y-k][x].damage_cooldown = 120
                explosion.append((direction,x, y-k))
                
            elif isinstance(level_array[y-k][x], Enemy):
                if level_array[y-k][x].entity.damage_cooldown==0:
                    level_array[y-k][x].entity.hp -= self.damage
                    level_array[y-k][x].entity.damage_cooldown = 90
                explosion.append((direction,x, y-k))
            
            elif isinstance(level_array[y-k][x], Hard_block):
                k+= self.size
            
            elif isinstance(level_array[y-k][x], Bomb):
                new_bomb = level_array[y-k][x]
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
            
            elif isinstance(level_array[y-k][x], Player_Bomb):
                new_bomb = level_array[y-k][x].bomb
                if level_array[y-k][x].player.damage_cooldown==0:
                    level_array[y-k][x].player.hp -= self.damage
                    level_array[y-k][x].player.damage_cooldown = 120
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
            
            else:
                explosion.append((direction, x, y-k))
                
            

            
        #bas
        direction = self.def_img['Vertical']
        k = 0
        while k<self.size:
            k+=1
            if k == self.size:
                direction = self.def_img['Bas']
            
                
            if isinstance(level_array[y+k][x], Destroyable_block):
                explosion.append((level_array[y+k][x].img_destroyed,x, y+k))
                destroyed.append((y+k,x))
                k+= self.size
                
            elif isinstance(level_array[y+k][x], Player):
                if level_array[y+k][x].damage_cooldown==0:
                    level_array[y+k][x].hp -= self.damage
                    level_array[y+k][x].damage_cooldown = 120
                explosion.append((direction,x, y+k))
            
            elif isinstance(level_array[y+k][x], Enemy):
                if level_array[y+k][x].entity.damage_cooldown==0:
                    level_array[y+k][x].entity.hp -= self.damage
                    level_array[y+k][x].entity.damage_cooldown = 90
                explosion.append((direction,x, y+k))
                
            elif isinstance(level_array[y+k][x], Hard_block):
                k+= self.size
                
            elif isinstance(level_array[y+k][x], Bomb):
                new_bomb = level_array[y+k][x]
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
                    
            elif isinstance(level_array[y+k][x], Player_Bomb):
                new_bomb = level_array[y+k][x].bomb
                if level_array[y+k][x].player.damage_cooldown==0:
                    level_array[y+k][x].player.hp -= self.damage
                    level_array[y+k][x].player.damage_cooldown = 120
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
            else:
                explosion.append((direction, x, y+k))
                
            
        
              
        #Droite
        direction = self.def_img['Horizontal']
        k = 0
        while k<self.size:
            k+=1
            if k == self.size:
                direction = self.def_img['Droite']

            
                
            if isinstance(level_array[y][x+k], Destroyable_block):
                explosion.append((level_array[y][x+k].img_destroyed,x+k, y))
                destroyed.append((y,x+k))
                k+= self.size
                
            elif isinstance(level_array[y][x+k], Player):
                if level_array[y][x+k].damage_cooldown==0:
                    level_array[y][x+k].hp -= self.damage
                    level_array[y][x+k].damage_cooldown = 120
                explosion.append((direction,x+k, y))
                
            elif isinstance(level_array[y][x+k], Enemy):
                if level_array[y][x+k].entity.damage_cooldown==0:
                    level_array[y][x+k].entity.hp -= self.damage
                    level_array[y][x+k].entity.damage_cooldown = 90
                explosion.append((direction,x+k, y))
            
            elif isinstance(level_array[y][x+k], Hard_block):
                k+= self.size
                
            elif isinstance(level_array[y][x+k], Bomb):
                new_bomb = level_array[y][x+k]
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
                    
            elif isinstance(level_array[y][x+k], Player_Bomb):
                new_bomb = level_array[y][x+k].bomb
                if level_array[y][x+k].player.damage_cooldown==0:
                    level_array[y][x+k].player.hp -= self.damage
                    level_array[y][x+k].player.damage_cooldown = 120
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
                    
            else:
                explosion.append((direction, x+k, y))
                
            
                
        #Gauche
        direction = self.def_img['Horizontal']
        k = 0
        while k<self.size:
            k+=1
            if k == self.size:
                direction = self.def_img['Gauche']
                
            
            if isinstance(level_array[y][x-k], Destroyable_block):
                explosion.append((level_array[y][x-k].img_destroyed,x-k, y))
                destroyed.append((y,x-k))
                k+= self.size
                
            elif isinstance(level_array[y][x-k], Player):
                if level_array[y][x-k].damage_cooldown==0:
                    level_array[y][x-k].hp -= self.damage
                    level_array[y][x-k].damage_cooldown = 120
                explosion.append((direction,x-k, y))
            
            elif isinstance(level_array[y][x-k], Enemy):
                if level_array[y][x-k].entity.damage_cooldown==0:
                    level_array[y][x-k].entity.hp -= self.damage
                    level_array[y][x-k].entity.damage_cooldown = 90
                explosion.append((direction,x-k, y))
            
            elif isinstance(level_array[y][x-k], Hard_block):
                k+= self.size
                
            elif isinstance(level_array[y][x-k], Bomb):
                new_bomb = level_array[y][x-k]
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
                
            elif isinstance(level_array[y][x-k], Player_Bomb):
                new_bomb = level_array[y][x-k].bomb
                if level_array[y][x-k].player.damage_cooldown==0:
                    level_array[y][x-k].player.hp -= self.damage
                    level_array[y][x-k].player.damage_cooldown = 120
                if not new_bomb.exploded:
                    new_bomb.explode(level)
                    new_bomb.tick = new_bomb.timer1
                    
            else:
                explosion.append((direction, x-k, y))
                
             
        

        self.explosion = explosion
        self.destroyed_blocks = destroyed


class Player_Bomb():
    def __init__(self, player, bomb) -> None:
        self.player = player
        self.bomb = bomb


class Blop():
    def __init__(self, pos_x, pos_y, img_path = 'img/blop_reinette.png', damage = 2, move_cooldown=90, hp=4, speed=2) -> None:
        self.x = pos_x
        self.y = pos_y
        self.pos = (self.x,self.y)
        
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (40, 40))
        
        self.speed = speed
        self.x_vel = 0
        self.y_vel = 0
        self.move_timer = 0
        self.damage_cooldown = 0 #damage it takes
        self.damage = damage #damage when it attacks
        self.move_cooldown = move_cooldown
        self.current_move_cooldown = 0
        
        self.hp = hp
        
    
    def move_random(self, level_array):
        #check if the player is already moving
        if self.move_timer >0:
            if self.move_timer<1+40//self.speed:
                self.x += self.x_vel
                self.y += self.y_vel
                self.move_timer +=1
                self.pos = (self.x,self.y)
                
            if self.move_timer == 1+40//self.speed:
                last_array_y = (self.y//40 - number_sign(self.y_vel))
                last_array_x = (self.x//40 - number_sign(self.x_vel))
                if isinstance(level_array[last_array_y][last_array_x], Enemy):
                    if level_array[last_array_y][last_array_x].entity == self:
                        level_array[last_array_y][last_array_x] = None
                level_array[self.y//40][self.x//40] = Enemy(self)
                self.move_timer = 0
                self.x_vel = 0
                self.y_vel = 0
                
        else:
            if self.current_move_cooldown > 0:
                self.current_move_cooldown -=1
            else:
                possible_directions = [(0,0), (0,-1), (0,1), (1,0), (-1,0)]
                
                if level_array[self.y//40-1][self.x//40] is None:
                    possible_directions.append((0,-1))
                elif level_array[self.y//40+1][self.x//40] is None:
                    possible_directions.append((0,1))
                elif level_array[self.y//40][self.x//40+1] is None:
                    possible_directions.append((1,0))
                elif level_array[self.y//40][self.x//40-1] is None:
                    possible_directions.append((-1,0))
                
                dir_x,dir_y = random.choice(possible_directions)
                if dir_x != 0 or dir_y !=0:
                    if level_array[self.y//40 + dir_y][self.x//40 + dir_x] is None:
                        self.y_vel = dir_y * self.speed
                        self.x_vel = dir_x * self.speed
                        self.move_timer +=1
                    elif isinstance(level_array[self.y//40 + dir_y][self.x//40 + dir_x],Player):
                        level_array[self.y//40 + dir_y][self.x//40 + dir_x].hp -= self.damage
                        level_array[self.y//40 + dir_y][self.x//40 + dir_x].damage_cooldown = 120
                        self.move_timer +=1
                    self.current_move_cooldown = random.randint(self.move_cooldown - self.move_cooldown//4, self.move_cooldown + self.move_cooldown//4)
            
class Enemy():
    def __init__(self, entity) -> None:
        self.entity = entity
        self.x = entity.x
        self.y = entity.y
        self.img = entity.img