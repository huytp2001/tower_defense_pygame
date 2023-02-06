import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test")

map_cols = 20
map_rows = 15
tile_size = 40
spawn_point = [1,0]
map =   [   
            1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
            1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,
            1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,
            1,1,1,1,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,
            1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,
            1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,
            1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,
            1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,
            1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,1,
            1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,
            1,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,
            1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,
            1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        ]

def get_tilemap(x, y):
    return map[y*map_cols+x]    

def set_tilemap(x,y,val):
    map[y*map_cols+x] = val

def getX_tilemap(index):
    return int(index%map_cols)

def getY_tilemap(index):
    return int(index/map_cols)

class Map:
    def __init__(self):
        self.surface = pygame.Surface((map_cols * tile_size, map_rows * tile_size))
        self.path_len = 0
        self.moving_queue = []
        self.createSurface()
        self.find_enemy_path()

    def createSurface(self):
        self.surface.fill((0,0,0))
        for x in range(len(map)):
            if map[x] == 0:
                pygame.draw.rect(self.surface, (255,255,255), (getX_tilemap(x) * tile_size, getY_tilemap(x) * tile_size, tile_size, tile_size))
                self.path_len += 1

    def find_path(self, tile):
        try:
            if get_tilemap(tile[0]+1, tile[1]) == 0:
                set_tilemap(tile[0], tile[1], 2)
                return [[tile[0]+1, tile[1]], "right"]
        except:
            pass
        try:
            if get_tilemap(tile[0]-1, tile[1]) == 0:
                set_tilemap(tile[0], tile[1], 2)
                return [[tile[0]-1, tile[1]], "left"]
        except:
            pass
        try:
            if get_tilemap(tile[0], tile[1]+1) == 0:
                set_tilemap(tile[0], tile[1], 2)
                return [[tile[0], tile[1]+1], "down"]
        except:
            pass
        try:
            if get_tilemap(tile[0], tile[1]-1) == 0:
                set_tilemap(tile[0], tile[1], 2)
                return [[tile[0], tile[1]-1], "up"]
        except:
            pass

    def find_enemy_path(self):
        enemy_path = [spawn_point]
        for x in range(self.path_len-1):
            [next_path, moving] = self.find_path(enemy_path[len(enemy_path)-1])
            enemy_path.append(next_path)
            self.moving_queue.append(moving)

    def draw_surface(self, screen, pos):
        screen.blit(self.surface, pos)

class Enemy:
    def __init__(self, max_hp):
        self.step_index = 0
        self.surface = pygame.Surface((tile_size, tile_size))
        self.posX = spawn_point[0]*tile_size + tile_size/2
        self.posY = spawn_point[1]*tile_size + tile_size/2
        self.moving_counter = 0
        self.max_hp = max_hp
        self.hp = max_hp
        
    def update(self, moving_queue): 
        if moving_queue[self.step_index] == "down":
            self.posY += 1
        if moving_queue[self.step_index] == "up":
            self.posY -= 1
        if moving_queue[self.step_index] == "left":
            self.posX -= 1
        if moving_queue[self.step_index] == "right":
            self.posX += 1
        if self.moving_counter >= tile_size:
            self.step_index += 1
            self.moving_counter = 0
        self.moving_counter += 1
        
    def draw(self, screen):
        size_scale = 1
        if self.hp >= self.max_hp*0.7:
            size_scale = 1
        elif self.hp >= self.max_hp*0.4:
            size_scale = 0.7
        elif self.hp >= 0:
            size_scale = 0.4
        else:
            pass
        pygame.draw.circle(screen, (255,0,0), (self.posX, self.posY), (tile_size/3)*size_scale)

class EnemyManager:
    def __init__(self, moving_queue):
        self.enemyContainer = list()
        self.moving_queue = moving_queue
        self.spawnCounter = 0

    def spawnEnemy(self, cooldown):
        if self.spawnCounter == 0:       
            newEnemy = Enemy(200)
            self.enemyContainer.append(newEnemy)
            self.spawnCounter = cooldown

    def update(self, screen):
        if self.spawnCounter > 0:
            self.spawnCounter -= 1
        for enemy in self.enemyContainer:
            try:
                if enemy.hp <= 0:
                    self.enemyContainer.remove(enemy)    
                enemy.update(self.moving_queue) 
                enemy.draw(screen)
            except IndexError:
                self.enemyContainer.remove(enemy)

class Tower:
    def __init__(self, pos, atk):
        self.pos = pos
        self.atk = atk
        self.attackable_tile = list()
        self.find_attackable_tile()
        self.atk_cooldown = 100
        self.atk_counter = 0
        self.beam_cooldown = 10
        self.beam_counter = 0
        self.last_enemy_pos = list()
        self.shoot_sound = pygame.mixer.Sound("shoot.mp3")

    def get_tilemap(self, x, y):
        return map[y*self.map_cols+x]    
    
    def set_tilemap(self, x,y,val):
        map[y*self.map_cols+x] = val

    def find_attackable_tile(self):
        try:
            if get_tilemap(self.pos[0] - 1, self.pos[1]) == 2:
                self.attackable_tile.append([self.pos[0] - 1, self.pos[1]])
            if get_tilemap(self.pos[0] + 1, self.pos[1]) == 2:
                self.attackable_tile.append([self.pos[0] + 1, self.pos[1]])
            if get_tilemap(self.pos[0], self.pos[1] - 1) == 2:
                self.attackable_tile.append([self.pos[0], self.pos[1] - 1])
            if get_tilemap(self.pos[0], self.pos[1] + 1) == 2:
                self.attackable_tile.append([self.pos[0], self.pos[1] + 1])
            if get_tilemap(self.pos[0] - 1, self.pos[1] - 1) == 2:
                self.attackable_tile.append([self.pos[0] - 1, self.pos[1] - 1])
            if get_tilemap(self.pos[0] + 1, self.pos[1] - 1) == 2:
                self.attackable_tile.append([self.pos[0] + 1, self.pos[1] - 1])
            if get_tilemap(self.pos[0] - 1, self.pos[1] + 1) == 2:
                self.attackable_tile.append([self.pos[0] - 1, self.pos[1] + 1])
            if get_tilemap(self.pos[0] + 1, self.pos[1] + 1) == 2:
                self.attackable_tile.append([self.pos[0] + 1, self.pos[1] + 1])
        except IndexError:
            pass
    def detect_enemy(self, enemyContainer):
        for enemy in enemyContainer:
            if [int(enemy.posX/tile_size), int(enemy.posY/tile_size)] in self.attackable_tile:
                if self.atk_counter == 0:
                    pygame.mixer.Sound.play(self.shoot_sound)
                    enemy.hp -= self.atk
                    self.last_enemy_pos = [enemy.posX, enemy.posY]
                    self.atk_counter = self.atk_cooldown
                    self.beam_counter = self.beam_cooldown


    def update(self, enemyContainer):
        self.detect_enemy(enemyContainer)
        if self.atk_counter > 0:
            self.atk_counter -= 1
        if self.beam_counter > 0:
            pygame.draw.line(screen, (0,0,255), (self.pos[0]*tile_size+tile_size/2, self.pos[1]*tile_size+tile_size/2), (self.last_enemy_pos[0], self.last_enemy_pos[1]), 5)
            self.beam_counter -= 1
        pygame.draw.circle(screen, (0,255,0), (self.pos[0]*tile_size+tile_size/2, self.pos[1]*tile_size+tile_size/2), tile_size/3)


myMap = Map()

myEnemyManager = EnemyManager(myMap.moving_queue)

towerContainer = list()

running = True
pause = False
clock = pygame.time.Clock()

placeTowerFlag = False
destroyTowerFlag = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                placeTowerFlag = True
            if event.key == pygame.K_d:
                destroyTowerFlag = True
            if event.key == pygame.K_SPACE:
                pause = not pause
    
    if not pause:
        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[2]:
            myEnemyManager.spawnEnemy(20)

        if placeTowerFlag:
            mouse = pygame.mouse.get_pos()
            if get_tilemap(int(mouse[0]/tile_size), int(mouse[1]/tile_size)) == 1:
                newTower = Tower([int(mouse[0]/tile_size), int(mouse[1]/tile_size)], 10)
                set_tilemap(int(mouse[0]/tile_size), int(mouse[1]/tile_size), 3)
                towerContainer.append(newTower)
            placeTowerFlag = False

        if destroyTowerFlag:
            mouse = pygame.mouse.get_pos()
            if get_tilemap(int(mouse[0]/tile_size), int(mouse[1]/tile_size)) == 3:
                for tower in towerContainer:
                    if [tower.pos[0], tower.pos[1]] == [int(mouse[0]/tile_size), int(mouse[1]/tile_size)]:
                        towerContainer.remove(tower)
                        set_tilemap(int(mouse[0]/tile_size), int(mouse[1]/tile_size), 1)
            destroyTowerFlag = False

        myEnemyManager.spawnEnemy(15)

        screen.fill((255, 255, 255))

        myMap.draw_surface(screen, (0,0))

        myEnemyManager.update(screen)

        for tower in towerContainer:
            tower.update(myEnemyManager.enemyContainer)

    pygame.display.update()
    clock.tick(120)

pygame.quit()


