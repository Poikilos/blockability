import sys
import os
import YAMLObject
game = None
widthy = 800
heighty = 640
dead = False
half_widthy = int(widthy / 2)
half_heighty = int(heighty / 2)

DISPLAY = (widthy, heighty)

class BABlock:
    tileset_path = None
    name = None
    tileset_cell_loc = None
    properties = None
    gravity_vec = None
    yo = None
    def __init__(self):
        pass
    
    def load_yml(yml_path):
        self.yo = YAMLObject()
        self.yo.loadYAML(yml_path)
        

class BAChunk:
    top_right_global_pos = None
    
    def __init__(self):
        self.top_right_global_pos = (0,0)

#levels = list()
chunks = list()

tileset_images = list()
tileset_block_width = 32
tileset_block_height = 32

materials = None
visibles = None
level_index = 0
player = None
camera = None
minimap_block_size = (3.0, 3.0)
door_wood_open_sound = None
door_wood_close_sound = None

#def goto_level(dest_level_index, from_index = None, is_door = True):
#    if is_door:
#        if door_wood_open_sound is not None:
#            door_wood_open_sound.play()
#    load_level(levels[dest_level_index], dest_level_index, from_index, is_door)
world = None

def warp(chunk_index, pos):
    load_chunk(chunk_index)
    set_player_pos(pos)

class BAGame:
    _players = list()
    _data_path = None
    _blocks = 
    _worlds = list()
    _images_path = None
    _tilesets_path = None
    
    def __init__(self, data_path, images_path):
        self._data_path = data_path
        self._images_path = os.path.join(self._data_path,"images")
        self._worlds_path = os.path.join(self._data_path, "worlds")
        self._tilesets_path = os.path.join(self._data_path, "tilesets")
        #NOTE: world name should be changed later (normally using load_world)
    
class BAWorld:
    name = None
    camera = None
    _data_path = None
    _story = None

    _world_path = None
    _chunks_path = None
    _block_size = None
    
    def __init__(self, bgame):
        global world_luid
        self._data_path = data_path  #os.path.join(".","data")
        self._worlds_path = os.path.join(self._data_path, "worlds")
        #NOTE: world name should be changed later (normally using load_world)
        self.name = "story"+str(story_luid)
        story_luid += 1
    
    def _load_world(self, name):
        self.name = name
        self._world_path = os.path.join(self._worlds_path, name)
        self._chunks_path = os.path.join(self._world_path, "chunks")
    
    def _load_chunk_at(pos):
        #can accept a float pos (whole number is block location)
        block_pos = (int(pos[0]), int(pos[1]))
        chunk_loc = (block_pos[0]/self._block_size, block_pos[1]/self._block_size)
        self._load_chunk_folder(os.path.join(self._chunks_path, str(chunk_loc[0])+","+str(chunk_loc[1]))
        
    def _load_chunk_folder(folder_path):
        yml_path = os.path.join(folder_path, "chunk.yml")

    def set_player_pos(pos):
        if player is not None:
            if player.sprite is not None:
                player.sprite.set_position(pos)

def main():
    global cameraX, cameraY, screen, dead, levels
    global visibles, materials, level_index, player, camera, tileset_images
    global minimap_surface, minimap_block_size
    global door_wood_open_sound, door_wood_close_sound
    try:
        pygame.mixer.music.load(os.path.join('data',"117818__oatmealcrunch__a2backw.ogg"))
        pygame.mixer.music.play(-1)
        door_wood_open_sound = pygame.mixer.Sound(os.path.join('data','door-wood-open.wav'))  #load sound
        door_wood_close_sound = pygame.mixer.Sound(os.path.join('data','door-wood-close.wav'))  #load sound
    except:
        print("Problem loading sound files in "+os.path.join(os.getcwd(),"data"))
        #raise UserWarning, "could not load or play soundfiles in folder"+os.getcwd()

    up = down = left = right = running = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#3090C7"))
    visibles = pygame.sprite.Group()
    player = Player(64, 64)
    materials = []

    tileset_image = pygame.image.load(os.path.join('data',"DungeonCrawl_ProjectUtumnoTileset.png"))
    tileset_image.convert_alpha()
    tileset_images.append(tileset_image)
    print("loaded tileset")
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                                          E",
        "P                         PPPPPP   PPPPP  PP",
        "P                 PPPP                     P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P        PPPP                              P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    levels.append(level)
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "B                                          P",
        "PP                                         P",
        "P       PPP                         PPP    P",
        "P                                          P",
        "P                  PPPP                    P",
        "P                                          P",
        "P                                          P",
        "P                                  PPPP    P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                        PPPPP             P",
        "P                                          P",
        "P                                          P",
        "P                  PPPP                    P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    levels.append(level)
    
    
    load_level(levels[level_index], level_index, is_door=False)
    
    playing = True
    while playing:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                playing = False
                
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    #pygame.quit()
                    #sys.exit()
                    playing = False
                    print("pressed K_ESCAPE")
                elif e.key == K_w or e.key == K_UP:
                    up = True
                elif e.key == K_s or e.key == K_DOWN:
                    down = True
                elif e.key == K_a or e.key == K_LEFT:
                    left = True
                elif e.key == K_d or e.key == K_RIGHT:
                    right = True
                elif e.key == K_SPACE:
                    running = True
                    
            elif e.type == KEYUP:
                if e.key == K_w or e.key == K_UP:
                    up = False
                elif e.key == K_s or e.key == K_DOWN:
                    down = False
                elif e.key == K_a or e.key == K_LEFT:
                    left = False
                elif e.key == K_d or e.key == K_RIGHT:
                    right = False
        
        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        activate_event = player.update(up, down, left, right, running, materials)
        if activate_event >= 0:
            if activate_event == 0:
                goto_level(0, from_index = level_index)
            if activate_event == 1:
                goto_level(1, from_index = level_index)
            else:
                print("unknown event "+str(activate_event))
        for e in visibles:
            screen.blit(e.image, camera.apply(e))
        if minimap_surface is not None:
            #minimap_surface.fill((0,0,0,0))
            minimap_surface.fill((0,0,0,0))
            for e in visibles:
                col=int(e.rect.left/32)
                row=int(e.rect.top/32)
                minimap_surface.fill((255,255,255,255),((col*minimap_block_size[0], row*minimap_block_size[1]),(minimap_block_size[0],minimap_block_size[1])))
                #minimap_surface.set_at( (col,row) , (255,255,255,255) )
            minimap_surface.set_alpha(128)
            screen.blit(minimap_surface, (0,0))
        else:
            print("Missing minimap surface")

        #pygame.display.update()
        clock.tick(60)
        pygame.display.flip()
    print("finished main")
    
    

#This is the class that controls where the scrolling stops for the player
class Camera(object):
    def __init__(self, camera_func, widthy, heighty):
        self.camera_func = camera_func
        #the width and height of the level, we want to stop scrolling at the edges of the level
        self.state = Rect(0, 0, widthy, heighty)

    #Method to re-calculate the position on the screen to apply the scrolling
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    #Update camera position once per loop
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def average_color_of_surface(s):
    color0 = 0
    color1 = 0
    color2 = 0
    deepcolor0 = 0
    deepcolor1 = 0
    deepcolor2 = 0
    #deepcolor3 = 0
    x = -1
    y = -1
    try:
        if s is not None:
            thisRect = s.get_rect()
            divisor = float(thisRect.width * thisRect.height)
            for y in range(0,thisRect.height):
                for x in range(0,thisRect.width):
                    thisColor = s.get_at((x,y))
                    deepcolor0 += thisColor[0]
                    deepcolor1 += thisColor[1]
                    deepcolor2 += thisColor[2]
            color0 = int(float(deepcolor0) / divisor + .5)
            color1 = int(float(deepcolor1) / divisor + .5)
            color2 = int(float(deepcolor2) / divisor + .5)
    except:
        print("Could not finish average_color_of_surface"+str(sys.exc_info())+" {location:("+str(x)+","+str(y)+")}")
    result = (color0, color1, color2)
    return result
#We just take the position of our target, and add half total screen size.
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+half_widthy, -t+half_heighty, w, h)

#functions to ensure we don't scroll outside of level.
#def complex_camera(camera, target_rect):
#    l, t, _, _ = target_rect
#    _, _, w, h = camera
#    l, t, _, _ = -l+half_widthy, -t+half_heighty, w, h
#    l = min(0, l)                        # stop scrolling at the left edge
#    l = max(-(camera.width-widthy), l)   # stop scrolling at the right edge
#    t = max(-(camera.height-heighty), t) # stop scrolling at the bottom
#    t = min(0, t)                        # stop scrolling at the top
#    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    nav_color = None
    event_index = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        nav_color = (255,255,255,255)

def point_is_in_rect(x, y, rect):
    result = False
    if (x is not None) and (y is not None) and (rect is not None):
        if (x>=rect.left) and (x<rect.right):
            if (y>=rect.top) and (y<rect.bottom):
                result = True
    return result
collide_count = 0

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.stand_r_image = pygame.image.load(os.path.join('data',"turtley-r.png"))
        self.stand_l_image = pygame.image.load(os.path.join('data',"turtley-l.png"))
        self.stand_l_image.convert_alpha()
        self.stand_r_image.convert_alpha()
        self.image = self.stand_r_image
        self.nav_color = average_color_of_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, 64, 64)

    def update(self, up, down, left, right, running, materials):
        activate_event = -1
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
            self.image = self.stand_l_image
        if right:
            self.xvel = 8
            self.image = self.stand_r_image
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        result = self.collide(self.xvel, 0, materials)
        if result >= 0:
            activate_event = result
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        result = self.collide(0, self.yvel, materials)
        if result >= 0:
            activate_event = result
        return activate_event

    def collide(self, xvel, yvel, materials):
        global collide_count
        activate_event = -1
        for p in materials:
            if p.event_index is not None:
                if xvel > 0:
                    try_x = self.rect.right + 1
                    try_y = self.rect.bottom - 1
                    #print("player at "+str(try_x)+","+str(try_y))
                    #print("  event on right at "+str(p.rect.left)+","+str(p.rect.top))
                    #print ("player bottom: "+str(self.rect.bottom)+" block bottom:"+ str(p.rect.bottom))
                    #print ("player right: "+str(self.rect.right)+" block left:"+ str(p.rect.left))
                    if point_is_in_rect(try_x, try_y, p.rect):
                        activate_event = p.event_index
                        #print("activate event")
                elif xvel < 0:
                    try_x = self.rect.left - 1
                    try_y = self.rect.bottom - 1
                    #print("player at "+str(try_x)+","+str(try_y))
                    #print("  event on left at "+str(p.rect.left)+","+str(p.rect.top))
                    if point_is_in_rect(try_x, try_y, p.rect):
                        activate_event = p.event_index
                        #print("activate event")
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    activate_event = p.event_index
                if xvel > 0:
                    self.rect.right = p.rect.left
                    collide_count += 1
                    #print("collide right "+str(collide_count))
                if xvel < 0:
                    self.rect.left = p.rect.right
                    collide_count += 1
                    #print("collide left "+str(collide_count))
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
        return activate_event

