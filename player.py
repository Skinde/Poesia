import pygame
class actor:
    relative_x_position = 50
    relative_y_position = 50
    current_frame = 0
    speed_x = 0
    speed_y = 0
    max_y_speed = 5
    max_x_speed = 5
    current_animation = None
    current_surface = None
    width = 0 
    height = 0
    source_surface = None
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
        
        

    

        
class player(actor):
    health = 100.0
    speed = 1.0
    stamina = 100.0

    