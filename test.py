map_cols = 10
map_rows = 5
map =   [   
            1,0,1,1,1,1,1,1,1,1,
            1,0,1,0,0,0,0,0,0,1,
            1,0,1,0,1,1,1,1,0,1,
            1,0,0,0,1,0,0,0,0,1,
            1,1,1,1,1,0,1,1,1,1
        ]

def get_tilemap(x, y):
    return map[y*map_cols+x]    
    
def set_tilemap(x,y,val):
    map[y*map_cols+x] = val

def getX_tilemap(index):
    return int(index%map_cols)

def getY_tilemap(index):
    return int(index/map_cols)

path_len = 0
for x in range(len(map)):
    if map[x] == 0:
        path_len += 1

def find_path(tile):
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

enemy_path = [[1,0]]
moving_stack = []
for x in range(path_len-1):
    [next_path, moving] = find_path(enemy_path[len(enemy_path)-1])
    enemy_path.append(next_path)
    moving_stack.append(moving)

print(moving_stack)


