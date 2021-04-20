import pygame
import random

class object:
    source_surface = None
    bouncable = False
    hit_boxes = []
    current_surface = None
    width = 0 
    height = 0
    






class scenary(object):
    collidable = True
    seed = 0
    def load_into_surface(surface_name, x, y):
        self.current_surface.blit(self.source_surface, (x,y), (self.image_places[surface_name][0], self.image_places[surface_name][1], self.image_places[surface_name][0] + self.width, self.image_places[surface_name][1] + self.height))

    def __init__(self, image_places, width, height, source, img_format, seed):
        self.source_surface = pygame.image.load(source + '.' + img_format).convert_alpha()
        self.width = width
        self.height = height
        self.image_places = image_places
        #TODO:Read this from config?
        self.current_surface = pygame.Surface((1920, 1080))
        random.seed(seed)


    def render_terrain(self, type, n_of_doors):
        def T1(self, door_configuration):
            room_width = random.randint(1,50)
            room_height = random.randint(1,40)
            load_into_surface("top_left_corner", 0, 0)
            for i in range(room_width):
                load_into_surface("top_wall", self.width*i,0)
        locals()["T"+type]

        
            
            

            
          


class actor(object):
    relative_x_position = 50
    relative_y_position = 50
    collidable = True
    current_frame = 0
    speed_x = 0
    speed_y = 0
    max_y_speed = 5
    max_x_speed = 5
    current_animation = None
    default_animation_name = ""
    #Format is line start_x,start_y,frames
    animation_lines = None
    def __init__(self,width,height, animation_lines, source, img_format, default_animation_name):
        self.source_surface = pygame.image.load(source + '.' + img_format).convert_alpha()
        self.animation_lines = animation_lines
        self.current_animation = default_animation_name
        self.current_surface = pygame.Surface((width,height))
        self.default_animation_name = default_animation_name
        self.width = width
        self.height = height
    def update_maths(self): 
        self.relative_x_position = self.relative_x_position + self.speed_x
        self.relative_y_position = self.relative_y_position + self.speed_y
    def update_graphics(self):
        if self.current_frame >= self.animation_lines[self.current_animation][2]:
            self.current_frame = 0
        self.current_surface.fill((0,0,0,0))
        self.current_surface.blit(self.source_surface, (0, 0), (
            self.animation_lines[self.current_animation][0]+(self.width*self.current_frame),
            self.animation_lines[self.current_animation][1],
            self.animation_lines[self.current_animation][0]+self.width*(self.current_frame+1),
            self.animation_lines[self.current_animation][1]
        ))
        self.current_frame = self.current_frame + 1
        
        

class prop(actor): 
    something_so_python_dosent_fuckint_complain = 1
        
class player(actor):
    health = 100.0
    speed = 1.0
    stamina = 100.0


    